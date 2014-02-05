import ROOT
import math
from DataFormats.FWLite import Events, Handle

ROOT.TH1.SetDefaultSumw2()

class PATreader() :

  def __init__(self, files, basic_histos, track_histos, vertex_histos, onlineTauPixVtxCollection='onlTausPixVtx2', onlineTauMuVtxCollection='onlTausMuVtx') :

    self.events = Events ( files )
    self.declareHandles()
    self.allEvents         = 0
    self.failinRecoHLT_pix = 0
    self.failinDMHLT_pix   = 0
    self.failinIsoHLT_pix  = 0
    self.failinRecoHLT_mu  = 0
    self.failinDMHLT_mu    = 0
    self.failinIsoHLT_mu   = 0
    self.hasNoOnlineTrk_mu = 0 
    self.hasRegionJet_mu   = 0
    self.hasRegionTrk_mu   = 0
    self.hasRegion_mu      = 0
    self.basic_histos      = basic_histos
    self.track_histos      = track_histos
    self.vertex_histos     = vertex_histos
    self.onlineTauPixVtxCollection = onlineTauPixVtxCollection
    self.onlineTauMuVtxCollection  = onlineTauMuVtxCollection
    self.HLTTausCollections = {
                               'onlTausHPS'     : onlTausHPS    ,
                               'onlTausMuVtx'   : onlTausMuVtx  ,
                               'onlTausDAVtx'   : onlTausDAVtx  ,
                               'onlTausDAVtx2'  : onlTausDAVtx2 ,
                               'onlTausPixVtx'  : onlTausPixVtx ,
                               'onlTausPixVtx2' : onlTausPixVtx2,  
                              }
    
  def looper(self, maxEvents=-1, pickEvents=[], verbose=False) :
        
    for loopId, event in enumerate(self.events):
      
      self.event = event
      
      if maxEvents > 0 : totEvents = maxEvents
      else             : totEvents = self.events.size()
      if maxEvents > 0 and loopId > maxEvents: break
      if loopId%(totEvents/20)==0 : print '=====> \t', round( float(loopId)/float(totEvents)*100., 0) ,'%'
      
      if event.eventAuxiliary().event() not in pickEvents and len(pickEvents)>0 : continue

      self.produceCollections(event, self.handles)

      off_vtx = [ vtx for vtx in offVtx   if self.selectVtx(vtx)                                                                              ] 
      off_tau = [ tau for tau in offTaus  if self.selectKinematics(tau, pt=20., eta=2.3) and self.tauID(tau) and bool(tau.genJet())           ]
      off_mu  = [ mu  for mu  in offMuons if self.selectKinematics(mu , pt=15., eta=2.1) and self.muonID(mu)                                  ]
      veto_mu = [ mu  for mu  in offMuons if self.selectKinematics(mu , pt=15., eta=2.4) and self.muonID(mu, iso_threshold=0.3, fullID=False) ]

      if len(off_vtx)  < 1                                 : continue 
      if len(off_mu)  != 1                                 : continue 
      if len(veto_mu)  > 1                                 : continue 
      if len(off_tau) != 1                                 : continue  
      if abs(off_vtx[0].z()-off_tau[0].vertex().z()) > 0.2 : continue  
      if off_tau[0].charge() * off_mu[0].charge() >= 0     : continue
      if self.deltaR(off_tau[0], off_mu[0]) < 0.5          : continue  
      
      tau = off_tau[0]
      mu  = off_mu [0]

      HLTTausMu  = self.pickHLTTausCollection(self.onlineTauMuVtxCollection)
      HLTTausPix = self.pickHLTTausCollection(self.onlineTauPixVtxCollection)

      onl_tau_mu_vtx  = self.best_matching([tau], HLTTausMu , dR=0.5).values()[0]
      onl_tau_pix_vtx = self.best_matching([tau], HLTTausPix, dR=0.5).values()[0]
      
      tau.onlMu               = onl_tau_mu_vtx
      tau.onlPix              = onl_tau_pix_vtx
      tau.genDM               = self.genDecayMode(self.getGenJetConstituents(tau))
      tau.offlineLeadingTrack = self.checkLeadingTrack(tau)
      if tau.offlineLeadingTrack is False : continue
      tau.onlineLeadingTrack  = self.best_matching([tau.offlineLeadingTrack], [cand for cand in onlPFcandidates if cand.charge()!=0], dR=0.1).values()[0]

      #if abs(onlPixVtx[0].z() - offVtx[0].z()) < 0.2: continue
      
      if verbose :
        print '\nevent', event.eventAuxiliary().event()   
        print 'tau pt', tau.pt(), '\teta', tau.eta(), '\tphi', tau.phi(), '\tcharge', tau.charge(), '\trecoDM', tau.decayMode(), '\tgenDM', tau.genDM   

      self.fillBasicHistos(self.basic_histos,'offTaus',tau)
      self.allEvents += 1

      ## check whether Tau is reconstructed online - MuVtx
      if not onl_tau_mu_vtx :
        self.failinRecoHLT_mu  += 1
      else :
        self.fillBasicHistos(self.basic_histos,'onlTauMu',tau)
        ## check whether Tau has leading track online - MuVtx
        if onl_tau_mu_vtx.tauID('decayModeFinding') < 0.5  :
          self.failinDMHLT_mu    += 1
          TauJetsIter0      = self.doSomethingForFailingEvents( onlJets, tau.onlMu, onlTracks0, onlJetsPreTrk )['caloJetsForTracking']
          FullTrackJetIter0 = [tr for tr in onlTracks0]
          for tr in TauJetsIter0 : FullTrackJetIter0.append(tr)
          if tau.onlineLeadingTrack is not False :  
            self.fillVertexAssociationHistos(self.vertex_histos, 'muVtx_failDMonl_hasOnlTrk', offVtx[0], onlMuVtx[0])
            self.fillTrackHistos(self.track_histos, 'offTrk_failDMonl_hasOnlTrk_mu', tau.offlineLeadingTrack, offVtx[0], onlPixVtx[0], onlMuVtx[0])
            self.fillTrackHistos(self.track_histos, 'onlTrk_failDMonl_hasOnlTrk_mu', tau.onlineLeadingTrack , offVtx[0], onlPixVtx[0], onlMuVtx[0])
          else :
            self.hasNoOnlineTrk_mu += 1
            if self.best_matching([tau.onlMu],TauJetsIter0).values()[0] is not False : self.hasRegionJet_mu += 1 
            if self.best_matching([tau.onlMu],onlTracks0).values()[0]   is not False : self.hasRegionTrk_mu += 1 
            if self.best_matching([tau.onlMu],TauJetsIter0).values()[0] is not False or \
               self.best_matching([tau.onlMu],onlTracks0).values()[0]   is not False : self.hasRegion_mu +=1
            self.fillVertexAssociationHistos(self.vertex_histos, 'muVtx_failDMonl_noOnlTrk', offVtx[0], onlMuVtx[0])
            self.fillTrackHistos(self.track_histos, 'offTrk_failDMonl_noOnlTrk_mu' , tau.offlineLeadingTrack, offVtx[0], onlPixVtx[0], onlMuVtx[0])
        else :
          self.fillVertexAssociationHistos(self.vertex_histos, 'muVtx_passDMonl_hasOnlTrk', offVtx[0], onlMuVtx[0])
          self.fillBasicHistos(self.basic_histos, 'onlTauMuPassingDM',tau) 
        ## check whether Tau is isolated online - MuVtx
        if onl_tau_mu_vtx.tauID('byIsolation') < 0.5 : self.failinIsoHLT_mu   += 1
        else                                         : self.fillBasicHistos(self.basic_histos,'onlTauMuPassingIso',tau)

      ## check whether Tau is reconstructed online - PixVtx
      if not onl_tau_pix_vtx :
        self.failinRecoHLT_pix += 1  
      else :
        self.fillBasicHistos(self.basic_histos,'onlTauPix',tau)
        ## check whether Tau has leading track online - PixVtx      
        if onl_tau_pix_vtx.tauID('decayModeFinding') < 0.5 :
          self.failinDMHLT_pix   += 1
          if tau.onlineLeadingTrack is not False :  
            self.fillVertexAssociationHistos(self.vertex_histos, 'pixVtx_failDMonl_hasOnlTrk', offVtx[0], onlPixVtx[0])
            self.fillTrackHistos(self.track_histos, 'offTrk_failDMonl_hasOnlTrk_pix', tau.offlineLeadingTrack, offVtx[0], onlPixVtx[0], onlMuVtx[0])
            self.fillTrackHistos(self.track_histos, 'onlTrk_failDMonl_hasOnlTrk_pix', tau.onlineLeadingTrack , offVtx[0], onlPixVtx[0], onlMuVtx[0])
          else :
            self.fillVertexAssociationHistos(self.vertex_histos, 'pixVtx_failDMonl_noOnlTrk', offVtx[0], onlPixVtx[0])
            self.fillTrackHistos(self.track_histos, 'offTrk_failDMonl_noOnlTrk_pix', tau.offlineLeadingTrack, offVtx[0], onlPixVtx[0], onlMuVtx[0])
        else :  
          self.fillVertexAssociationHistos(self.vertex_histos, 'pixVtx_passDMonl_hasOnlTrk', offVtx[0], onlPixVtx[0])
          self.fillBasicHistos(self.basic_histos, 'onlTauPixPassingDM',tau)  
        ## check whether Tau is isolated online - PixVtx
        if onl_tau_pix_vtx.tauID('byIsolation') < 0.5 : self.failinIsoHLT_pix  += 1        
        else                                          : self.fillBasicHistos(self.basic_histos,'onlTauPixPassingIso',tau)
      
  def produceCollections(self, event, handles) :
    for key in handles.keys() :
      try :
        handle = handles[key][0]
        label  = handles[key][1]
        event.getByLabel(label,handle)
        globals()[key] = handle.product()
      except :
        pass 

  def declareHandles(self) :

    self.handles = {}

    ## offline
    self.handles[ 'offTaus'        ] = [ Handle('std::vector<pat::Tau>'         ),'selectedTaus'                     ] # default HPS offline tau 
    self.handles[ 'offTaus2'       ] = [ Handle('std::vector<pat::Tau>'         ),'selectedTausFixedCone'            ] # fixed cone offline tau - offline reference most similar to online tau (selectedHltPatTausOnl2NP) 
    self.handles[ 'offMuons'       ] = [ Handle('std::vector<pat::Muon>'        ),'selectedMuons'                    ]
    self.handles[ 'offPFcandidates'] = [ Handle('std::vector<reco::PFCandidate>'),'particleFlow'                     ]
    self.handles[ 'offVtx'         ] = [ Handle('std::vector<reco::Vertex>'     ),'selectedPrimaryVertices'          ]

    ## online
    self.handles[ 'onlTausHPS'     ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausHPS'            ] # HPS at HLT
    self.handles[ 'onlTausMuVtx'   ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausNP'             ] # cone tau with muon-vertex
    self.handles[ 'onlTausDAVtx'   ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausOnlNP'          ] # cone tau with online DA vertex [0]
    self.handles[ 'onlTausDAVtx2'  ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausOnl2NP'         ] # cone tau with highest-weight online DA vertex
    self.handles[ 'onlTausPixVtx'  ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxlNP'          ] # cone tau with pixel vertex [0]
    self.handles[ 'onlTausPixVtx2' ] = [ Handle('std::vector<pat::Tau>'         ),'selectedHltPatTausPxl2NP'         ] # cone tau with closest-in-dZ pixel vertex (use it as a baseline)
    self.handles[ 'onlPFcandidates'] = [ Handle('std::vector<reco::PFCandidate>'),'hltParticleFlowForTaus'           ]
      
    self.handles[ 'onlPixTracks'   ] = [ Handle('std::vector<reco::Track>'      ),'hltPixelTracks'                   ]
    self.handles[ 'onlTracks0'     ] = [ Handle('std::vector<reco::Track>'      ),'hltPFlowTrackSelectionHighPurity' ]
    self.handles[ 'onlTracks1'     ] = [ Handle('std::vector<reco::Track>'      ),'hltIter1Merged'                   ]
    self.handles[ 'onlTracks2'     ] = [ Handle('std::vector<reco::Track>'      ),'hltIter2Merged'                   ]
    self.handles[ 'onlTracks3'     ] = [ Handle('std::vector<reco::Track>'      ),'hltIter3Merged'                   ]
    self.handles[ 'onlTracks'      ] = [ Handle('std::vector<reco::Track>'      ),'hltPFMuonMerging'                 ]
      
    self.handles[ 'onlJets'        ] = [ Handle('std::vector<reco::CaloJet>'    ),'hltAntiKT5CaloJetsPFEt5'          ]
    self.handles[ 'onlJetsPreTrk'  ] = [ Handle('std::vector<reco::TrackJet>'   ),'hltAntiKT5TrackJetsIter0'         ]
    self.handles[ 'onlTrkJets0'    ] = [ Handle('std::vector<reco::TrackJet>'   ),'hltTrackAndTauJetsIter0'          ]
    self.handles[ 'onlTrkJets1'    ] = [ Handle('std::vector<reco::TrackJet>'   ),'hltTrackAndTauJetsIter1'          ]
    self.handles[ 'onlTrkJets2'    ] = [ Handle('std::vector<reco::TrackJet>'   ),'hltTrackAndTauJetsIter2'          ]
    self.handles[ 'onlTrkJets3'    ] = [ Handle('std::vector<reco::TrackJet>'   ),'hltTrackAndTauJetsIter3'          ]
      
    self.handles[ 'onlPixVtx'      ] = [ Handle('std::vector<reco::Vertex>'     ),'hltPixelVertices'                 ]
    self.handles[ 'onlInterVtx'    ] = [ Handle('std::vector<reco::Vertex>'     ),'hltOnlineVerticesAfterIter0'      ]
    self.handles[ 'onlMuVtx'       ] = [ Handle('std::vector<reco::Vertex>'     ),'hltIsoMuonVertex'                 ]

  def selectVtx(self, vtx, ndof=4, max_z=24., max_rho=2.) :
    return vtx.ndof>ndof and abs(vtx.z())<max_z and abs(vtx.position().rho())<max_rho
    
  def selectKinematics(self, particle, pt, eta) :    
    return particle.pt()>pt and abs(particle.eta())<eta 

  def muonID(self, mu, iso_threshold=0.15, fullID=True) :
    if   fullID : id = mu.isGlobalMuon() and mu.isTrackerMuon() and mu.isPFMuon()
    else        : id = mu.isGlobalMuon() 
    isoHandle = mu.pfIsolationR04()
    iso       = ( (isoHandle.sumChargedHadronPt + max(0.,isoHandle.sumNeutralHadronEt + isoHandle.sumPhotonEt - 0.5*isoHandle.sumPUPt) ) / mu.pt() < iso_threshold)  
    return iso and id

  def tauID(self, tau) :
    return tau.tauID('decayModeFinding')                         > 0.5  and \
           tau.tauID('byCombinedIsolationDeltaBetaCorrRaw3Hits') < 1.5  and \
           tau.tauID('againstMuonTight')                         > 0.5  and \
           tau.tauID('againstElectronLoose')                     > 0.5  

  def deltaPhi(self, phi1, phi2):
    PHI = abs(phi1-phi2)
    if (PHI<=math.pi):
      return PHI
    else:
      return 2*math.pi-PHI

  def checkLeadingTrack(self, tau) :
    if tau.leadPFChargedHadrCand().trackRef().isNull() :
      print 'event: ',self.event.eventAuxiliary().event(),'\t good offline Tau leading track has invalid leadPFChargedHadrCand().trackRef()\t SKIPPING' 
      return False
    else :
      return tau.leadPFChargedHadrCand().trackRef()

  def deltaR(self, p1, p2) :
    eta1 = p1.eta()
    phi1 = p1.phi()
    eta2 = p2.eta()
    phi2 = p2.phi()
    deta = eta1-eta2
    dphi = self.deltaPhi(phi1,phi2)
    return math.sqrt(deta*deta + dphi*dphi)

  def best_matching(self, coll1, coll2, dR=0.5) :
    association = {}
    for p1 in coll1 :
      tmp = {p1:False}
      for p2 in coll2 :
        if self.deltaR(p1,p2) < dR :
          dR = self.deltaR(p1,p2)
          tmp = {p1:p2}
      association.update(tmp)
    return association        

  def getGenJetConstituents(self, tau) :
    index = 0
    genJetConstituents = []
    while True :
      if bool(tau.genJet().getGenConstituent(index)) :
        genJetConstituents.append(tau.genJet().getGenConstituent(index))
        index += 1
      else :
        break
    return genJetConstituents 

  def genDecayMode(self, genJetConstituents) :
    pdgIds      = [ abs(constituent.pdgId()) for constituent in genJetConstituents ]
    photons   = pdgIds.count(22 )
    pizeros   = pdgIds.count(111)
    picharged = pdgIds.count(211)
    electrons = pdgIds.count(11 )
    muons     = pdgIds.count(13 )
  
    chargedHads = [ constituent.charge() for constituent in genJetConstituents if constituent.charge() != 0 and abs(constituent.pdgId()) != 11 and abs(constituent.pdgId()) != 13 ]
    neutralHads = [ constituent.charge() for constituent in genJetConstituents if constituent.charge() == 0 and abs(constituent.pdgId()) != 22 ]
  
    if   electrons == 1 or muons == 1           :             ##  leptonic decay
      print 'chargedHads', len(chargedHads)
      print 'neutralHads', len(neutralHads)
      print 'picharged'  , picharged
      print 'pizeros'    , pizeros
      print 'photons'    , photons
      print 'electrons'  , electrons
      print 'muons'      , muons
      return [ -99, 'tau decays into', electrons*'electrons'+muons*'muons'  ]  
    elif len(chargedHads) == 1 and photons == 0 : return [0  , 'oneProng0Pi0'   ]
    elif len(chargedHads) == 1 and photons == 2 : return [1  , 'oneProng1Pi0'   ]
    elif len(chargedHads) == 1 and photons == 4 : return [2  , 'oneProng2Pi0'   ]
    elif len(chargedHads) == 1                  : return [3  , 'oneProngOther'  ]
    elif len(chargedHads) == 3 and photons == 0 : return [10 , 'threeProng0Pi0' ]
    elif len(chargedHads) == 3 and photons == 2 : return [11 , 'threeProng1Pi0' ]
    elif len(chargedHads) == 3                  : return [12 , 'threeProngOther']
    else                                        : 
      print 'chargedHads', len(chargedHads)
      print 'neutralHads', len(neutralHads)
      print 'picharged'  , picharged
      print 'pizeros'    , pizeros
      print 'photons'    , photons
      print 'electrons'  , electrons
      print 'muons'      , muons
      return [ -99, 'bad tau' ]  
      
  def printSummary(self) :
    print 'allEvents         ' ,self.allEvents         
    print 'failinRecoHLT_pix ' ,self.failinRecoHLT_pix 
    print 'failinDMHLT_pix   ' ,self.failinDMHLT_pix   
    print 'failinIsoHLT_pix  ' ,self.failinIsoHLT_pix  
    print 'failinRecoHLT_mu  ' ,self.failinRecoHLT_mu  
    print 'failinDMHLT_mu    ' ,self.failinDMHLT_mu    
    print 'failinIsoHLT_mu   ' ,self.failinIsoHLT_mu   
    print 'hasNoOnlineTrk_mu ' ,self.hasNoOnlineTrk_mu   
    print 'hasRegionJet_mu   ' ,self.hasRegionJet_mu   
    print 'hasRegionTrk_mu   ' ,self.hasRegionTrk_mu   
    print 'hasRegion_mu      ' ,self.hasRegion_mu   

  def fillBasicHistos(self, histos, name, particle) :
    try    : histos[name]['pt'    ].Fill(particle.pt()         )
    except : pass
    try    : histos[name]['gen_pt'].Fill(particle.genJet().pt())
    except : pass
    try    : histos[name]['eta'   ].Fill(particle.eta()        )
    except : pass
    try    : histos[name]['phi'   ].Fill(particle.phi()        )
    except : pass
    try    : histos[name]['charge'].Fill(particle.charge()     )
    except : pass
    try    : histos[name]['recoDM'].Fill(particle.decayMode    )
    except : pass
    try    : histos[name]['genDM' ].Fill(particle.genDM        )
    except : pass

  def fillVertexAssociationHistos(self, histos, name, vtx1, vtx2) :
    try    : histos[name]['dxy(offlineVtx)'].Fill( math.sqrt( (vtx1.x()-vtx2.x())*(vtx1.x()-vtx2.x()) + 
                                                              (vtx1.y()-vtx2.y())*(vtx1.y()-vtx2.y()) ) )
    except : pass
    try    : histos[name]['dz(offlineVtx)' ].Fill( abs(vtx1.z()-vtx2.z()) )
    except : pass
   
  def fillTrackHistos(self, histos, name, track, offvtx, hltpixvtx, hltmuvtx) :
    try    : histos[name]['pt'                        ] .Fill(track.pt()                                     )
    except : pass
    try    : histos[name]['errPtOverPt'               ] .Fill(track.ptError()/track.pt()                     )
    except : pass
    try    : histos[name]['eta'                       ] .Fill(track.eta()                                    )
    except : pass
    try    : histos[name]['phi'                       ] .Fill(track.phi()                                    )
    except : pass
    try    : histos[name]['chi2'                      ] .Fill(track.chi2()                                   )
    except : pass
    try    : histos[name]['ndof'                      ] .Fill(track.ndof()                                   )
    except : pass
    try    : histos[name]['charge'                    ] .Fill(track.charge()                                 )
    except : pass
    try    : histos[name]['normalizedChi2'            ] .Fill(track.normalizedChi2()                         )
    except : pass
    try    : histos[name]['numberOfLostHits'          ] .Fill(track.numberOfLostHits()                       )
    except : pass
    try    : histos[name]['numberOfValidHits'         ] .Fill(track.numberOfValidHits()                      )
    except : pass
    try    : histos[name]['numberOfValidPixelHits'    ] .Fill(track.hitPattern().numberOfValidPixelHits()    )
    except : pass
    try    : histos[name]['pixelLayersWithMeasurement'] .Fill(track.hitPattern().pixelLayersWithMeasurement())
    except : pass
    try    : histos[name]['numberOfValidTrackerHits'  ] .Fill(track.hitPattern().numberOfValidTrackerHits()  )
    except : pass
    try    : histos[name]['dxy(offlineVtx)'           ] .Fill(track.dxy(offvtx.position())                   )
    except : pass
    try    : histos[name]['dz(offlineVtx)'            ] .Fill(track.dz(offvtx.position())                    )
    except : pass
    try    : histos[name]['dxy(hltPixVtx)'            ] .Fill(track.dxy(hltpixvtx.position())                )
    except : pass
    try    : histos[name]['dz(hltPixVtx)'             ] .Fill(track.dz(hltpixvtx.position())                 )
    except : pass
    try    : histos[name]['dxy(hltMuVtx)'             ] .Fill(track.dxy(hltmuvtx.position())                 )
    except : pass
    try    : histos[name]['dz(hltMuVtx)'              ] .Fill(track.dz(hltmuvtx.position())                  )
    except : pass
    try    : histos[name]['dRoffline'                 ] .Fill(deltaR(track,offTau)                           )
    except : pass
    try    : histos[name]['dRonline'                  ] .Fill(deltaR(track,onlTau)                           )
    except : pass
    try    : histos[name]['algo'                      ] .Fill(track.algo()-4                                 )
    except : pass

  def returnBasicHistos(self) :
    return self.basic_histos

  def returnTrackHistos(self) :
    return self.track_histos

  def doSomethingForFailingEvents(self, jetCollection, onlineTau, trackCollection, trackJetCollection) :
    stuff = {}
    caloJetsForTracking = self.filterCaloJetsForTracking(jetCollection, onlineTau, trackCollection, trackJetCollection)
    stuff.update({'caloJetsForTracking':caloJetsForTracking})
    return stuff
  
  def filterCaloJetsForTracking(self, jetCollection, onlineTau, trackCollection, trackJetCollection) :
    '''
    Mimics the filtering applied to calo jets online before using them as regions
    for seeding the tracking
    '''
    jetsForTracking = []
    for jet in onlJets :
      if self.deltaR(jet,onlineTau)>0.5 : continue
      if jet.pt() < 5.        : continue 
      if abs(jet.eta()) > 2.7 : continue
      ptIn  = 0.
      ptOut = 0.
      for tower in jet.getCaloConstituents() :
        try :
          mydR = self.deltaR(tower,jet)
          if   mydR < 0.2 : ptIn  += tower.pt()
          elif mydR < 0.5 : ptOut += tower.pt()      
        except : pass
      try    : frac = ptIn / (ptIn + ptOut)
      except : frac = 0.
      if frac < 0.7 : continue
  
      nmatch   = 0
      nmatchpt = 0.
      for trackJet in trackJetCollection :
        for trk in trackJet.tracks() :
          if trk.isNonnull() and trk.isAvailable() :
            if self.deltaR(trk, jet) < 0.5 :
              nmatch   += 1
              nmatchpt += trk.pt()
      
      if nmatch>0 or nmatchpt>1. : continue
  
      nmatch2   = 0
      nmatchpt2 = 0.
      for trk in trackCollection :
        if self.deltaR(trk, jet) < 0.5 :
          nmatch2 += 1
          nmatchpt2 += trk.pt()
          
      if nmatchpt2 / jet.pt() > 0.3 : continue
      jetsForTracking.append(jet)
    
    return jetsForTracking

  def pickHLTTausCollection(self, collectionName) :
    return self.HLTTausCollections[collectionName]






