import math
import ROOT
from copy import deepcopy as dc

decayModeDict =  { 0  : 'kOneProng0PiZero'  ,
                   1  : 'kOneProng1PiZero'  ,
                   2  : 'kOneProng2PiZero'  ,
                   3  : 'kOneProng3PiZero'  ,
                   4  : 'kOneProngNPiZero'  ,
                   5  : 'kTwoProng0PiZero'  ,
                   6  : 'kTwoProng1PiZero'  ,
                   7  : 'kTwoProng2PiZero'  ,
                   8  : 'kTwoProng3PiZero'  ,
                   9  : 'kTwoProngNPiZero'  ,
                   10 : 'kThreeProng0PiZero',
                   11 : 'kThreeProng1PiZero',
                   12 : 'kThreeProng2PiZero',
                   13 : 'kThreeProng3PiZero',
                   14 : 'kThreeProngNPiZero',
                   15 : 'kRareDecayMode'    }

def deltaPhi(phi1, phi2):
  PHI = abs(phi1-phi2)
  if (PHI<=math.pi):
    return PHI
  else:
    return 2*math.pi-PHI

def deltaR(p1,p2) :
  eta1 = p1.eta()
  phi1 = p1.phi()
  eta2 = p2.eta()
  phi2 = p2.phi()
  deta = eta1-eta2
  dphi = deltaPhi(phi1,phi2)
  return math.sqrt(deta*deta + dphi*dphi)

def best_matching(coll1, coll2, dR=0.5) :
  association = {}
  for p1 in coll1 :
    tmp = {p1:False}
    for p2 in coll2 :
      if deltaR(p1,p2) < dR :
        dR = deltaR(p1,p2)
        tmp = {p1:p2}
    association.update(tmp)
  return association        

def passAntiEMVA(iCat, raw, WP=0) :
  iCat = int(iCat)
  
  if iCat<0  : return False
  if iCat>15 : return True

  cutsLoose     = [0.835,0.831,0.849,0.859,0.873,0.823,0.85 ,0.855,0.816,0.861,0.862,0.847,0.893,0.82 ,0.845,0.851]
  cutsMedium    = [0.933,0.921,0.944,0.945,0.918,0.941,0.981,0.943,0.956,0.947,0.951,0.95 ,0.897,0.958,0.955,0.942]
  cutsTight     = [ 0.96,0.968,0.971,0.972,0.969,0.959,0.981,0.965,0.975,0.972,0.974,0.971,0.897,0.971,0.961,0.97 ]
  cutsVeryTight = [0.978,0.98 ,0.982,0.985,0.977,0.974,0.989,0.977,0.986,0.983,0.984,0.983,0.971,0.987,0.977,0.981]
  cut = 0
  
  if WP==0  : cut = cutsLoose[iCat]
  if WP==1  : cut = cutsMedium[iCat]
  if WP==2  : cut = cutsTight[iCat]
  if WP==3  : cut = cutsVeryTight[iCat]
  
  return (raw>cut)

def TauID(tau) :
  passed = tau.tauID('decayModeFinding')                         > 0.5  and \
           tau.tauID('byCombinedIsolationDeltaBetaCorrRaw3Hits') < 1.5  and \
           tau.tauID('againstMuonTight')                         > 0.5  and \
           tau.tauID('againstElectronLoose')                     > 0.5  
  return passed
  #if not passAntiEMVA(tau.tauID('againstElectronMVA3category'),tau.tauID('againstElectronMVA3raw')) : return False

def muonID(muon, threshold=0.15, fullID=True) :
  if   fullID : id = muon.isGlobalMuon() and muon.isTrackerMuon() and muon.isPFMuon()
  else        : id = muon.isGlobalMuon() 
  isoHandle = muon.pfIsolationR04()
  iso       = ( (isoHandle.sumChargedHadronPt + max(0.,isoHandle.sumNeutralHadronEt + isoHandle.sumPhotonEt - 0.5*isoHandle.sumPUPt) ) / muon.pt() < threshold)  
  passed = iso and id
  return passed

def kinematics(particle, pt=20., eta=2.3) :
  passed = particle.pt() > pt and abs(particle.eta()) < eta
  return passed

def sort_by_pt(myList, reverse=False) :
 newList = sorted(myList, key=lambda x: x.pt(), reverse=reverse)
 return newList

def sort_by_pt2(myList, reverse=False) :
 newList = sorted(myList, key=lambda x: x.p4().pt(), reverse=reverse)
 return newList

def find_closest_vertex(onlVertex, offVertices):
  dz = 9999999.
  for offVtx in offVertices :
    if abs(offVtx.position().z() - onlVertex.position().z()) < dz :
      dz = abs(offVtx.position().z() - onlVertex.position().z())
      closestVert = offVtx
  return closestVert
   

def buildMass(p1,p2) :
  p1P4 = ROOT.TLorentzVector(p1.px(), p1.py(), p1.pz(), p1.energy())
  p2P4 = ROOT.TLorentzVector(p2.px(), p2.py(), p2.pz(), p2.energy())
  return (p1P4 + p2P4).M()

def bookTrackHistos(nameTrack) :
  histos = {}
  histos.update({nameTrack:{}})
  histos[nameTrack].update({'chi2'                                  : ROOT.TH1F('chi2'                                   , 'chi2()                                 '    , 40, 0, 20)})
  histos[nameTrack].update({'ndof'                                  : ROOT.TH1F('ndof'                                   , 'ndof()                                 '    , 40, 0, 40)})
  histos[nameTrack].update({'normalizedChi2'                        : ROOT.TH1F('normalizedChi2'                         , 'normalizedChi2()                       '    , 20, 0, 20)})
  histos[nameTrack].update({'numberOfLostHits'                      : ROOT.TH1F('numberOfLostHits'                       , 'numberOfLostHits()                     '    , 20, 0, 20)})
  histos[nameTrack].update({'numberOfValidHits'                     : ROOT.TH1F('numberOfValidHits'                      , 'numberOfValidHits()                    '    , 20, 0, 20)})
  histos[nameTrack].update({'highPurity'                            : ROOT.TH1F('highPurity'                             , 'highPurity                             '    , 5 , 0, 5 )})
  histos[nameTrack].update({'hitPattern().numberOfValidPixelHits'   : ROOT.TH1F('hitPattern().numberOfValidPixelHits'    , 'hitPattern().numberOfValidPixelHits()  '    , 20, 0, 20)})
  histos[nameTrack].update({'hitPattern().numberOfValidTrackerHits' : ROOT.TH1F('hitPattern().numberOfValidTrackerHits'  , 'hitPattern().numberOfValidTrackerHits()'    , 20, 0, 20)})
  histos[nameTrack].update({'dxy(offlineVtx)'                       : ROOT.TH1F('dxy(offlineVtx)'                        , 'dxy(offlineVtx)                        '    , 40, 0, 2 )})
  histos[nameTrack].update({'dz(offlineVtx)'                        : ROOT.TH1F('dz(offlineVtx)'                         , 'dz(offlineVtx)                         '    , 40, 0, 20)})
 
def genDecayMode(genJetConstituents) :
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
    return [ -99, 'bad tau' ]  
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
  
def fillTrackHistos(histos, track, offvtx, hltpixvtx, hltmuvtx, offTau, onlTau) :
  #import pdb ; pdb.set_trace()
  histos['pt'                      ] .Fill(track.pt()                                   )
  histos['errPtOverPt'             ] .Fill(track.ptError()/track.pt()                   )
  histos['eta'                     ] .Fill(track.eta()                                  )
  histos['phi'                     ] .Fill(track.phi()                                  )
  histos['chi2'                    ] .Fill(track.ndof()                                 )
  histos['ndof'                    ] .Fill(track.chi2()                                 )
  histos['normalizedChi2'          ] .Fill(track.normalizedChi2()                       )
  histos['numberOfLostHits'        ] .Fill(track.numberOfLostHits()                     )
  histos['numberOfValidHits'       ] .Fill(track.numberOfValidHits()                    )
  histos['numberOfValidPixelHits'  ] .Fill(track.hitPattern().numberOfValidPixelHits()  )
  histos['numberOfValidTrackerHits'] .Fill(track.hitPattern().numberOfValidTrackerHits())
  histos['dxy_offVtx'              ] .Fill(track.dxy(offvtx)                            )
  histos['dz_offVtx'               ] .Fill(track.dz(offvtx)                             )
  histos['dxy_hltPixVtx'           ] .Fill(track.dxy(hltpixvtx)                         )
  histos['dz_hltPixVtx'            ] .Fill(track.dz(hltpixvtx)                          )
  histos['dxy_hltMuVtx'            ] .Fill(track.dxy(hltmuvtx)                          )
  histos['dz_hltMuVtx'             ] .Fill(track.dz(hltmuvtx)                           )
  histos['dRoffline'               ] .Fill(deltaR(track,offTau)                         )
  histos['dRonline'                ] .Fill(deltaR(track,onlTau)                         )
  histos['algo'                    ] .Fill(track.algo()-4                               )
  histos['layer'                   ] .Fill(track.hitPattern().pixelLayersWithMeasurement())


def plotting(offline_tau_pt, trigger_tau_pt, triggerDecayMode_tau_pt, triggerIsolation_tau_pt, allTausDM, badTausDM, myString) :

  c1 = ROOT.TCanvas('','',700,700)
  ROOT.gPad.SetLeftMargin(0.18)
  ROOT.gPad.SetBottomMargin(0.18)
  ROOT.gPad.SetFrameLineWidth(3)
  ROOT.gPad.SetGridx(1)
  ROOT.gPad.SetGridy(1)
  
  for hist in [offline_tau_pt, trigger_tau_pt, triggerDecayMode_tau_pt, triggerIsolation_tau_pt, allTausDM, badTausDM] :
    hist.SetTitle('')
    if myString == 'gen'  : hist.GetXaxis().SetTitle('gen #tau visible p_{T} [GeV]')
    if myString == 'reco' : hist.GetXaxis().SetTitle('offline #tau p_{T} [GeV]')
    hist.GetYaxis().SetTitle('efficiency')
    hist.GetXaxis().SetTitleOffset(1.5)
    hist.GetYaxis().SetTitleOffset(1.5)
    hist.SetLineWidth(2)
    hist.SetLineColor(ROOT.kBlue)
    hist.SetMarkerStyle(9)
  
  ratio1 = dc(trigger_tau_pt)
  ratio1.Divide(trigger_tau_pt,offline_tau_pt,1.,1.,'b')
  ratio1.SetLineColor(ROOT.kRed)
  trigger_tau_pt.SetLineColor(ROOT.kRed)
  ratio1.SetMaximum(1.05)
  ratio1.SetMinimum(0.5)
  ratio1.Draw('E')
  
  ratio2 = dc(triggerDecayMode_tau_pt)
  ratio2.Divide(triggerDecayMode_tau_pt,offline_tau_pt,1.,1.,'b')
  ratio2.SetLineColor(ROOT.kGreen+3)
  triggerDecayMode_tau_pt.SetLineColor(ROOT.kGreen+3)
  ratio2.SetMaximum(1.05)
  ratio2.SetMinimum(0.5)
  ratio2.Draw('ESAME')

  ratio3 = dc(triggerIsolation_tau_pt)
  ratio3.Divide(triggerIsolation_tau_pt,offline_tau_pt,1.,1.,'b')
  ratio3.SetLineColor(ROOT.kBlue)
  triggerIsolation_tau_pt.SetLineColor(ROOT.kBlue)
  ratio3.SetMaximum(1.05)
  ratio3.SetMinimum(0.5)
  #ratio3.Draw('ESAME')
  
  l1 = ROOT.TLegend(0.6,0.24,0.86,0.4)
  l1.AddEntry(trigger_tau_pt         ,'p_{T}>20 GeV'  )
  l1.AddEntry(triggerDecayMode_tau_pt,'Leading Track' )
  #l1.AddEntry(triggerIsolation_tau_pt,'Isolation'     )
  l1.SetFillColor(0)
  l1.Draw('sameAEPZ')
  
  c1.SaveAs('ratio_'+myString+'.pdf')
  
  badTausDM.Draw('E')
  c1.SaveAs('decayModeBad.pdf')
  allTausDM.Draw('E')
  c1.SaveAs('decayModeAll.pdf')
  
  ratio = dc(badTausDM)
  ratio.Divide(badTausDM,allTausDM,1.,1.,'b')
  ratio.SetTitle('Leading Track Finding failure rate')
  ratio.GetXaxis().SetTitle('#tau gen Decay Mode')
  ratio.GetYaxis().SetTitle('failure rate')
  ratio.Draw('E')
  c1.SaveAs('decayMode.pdf')

# def muonTightID(muon) :
#   muon.globalTrack().normalizedChi2() < 10.
#   muon.globalTrack().hitPattern().numberOfValidMuonHits() > 0
#   muon.numberOfMatchedStations() > 1
#   muon.dB() < 0.2
#   muon.innerTrack()->hitPattern().numberOfValidPixelHits() > 0
#   muon.track().hitPattern().trackerLayersWithMeasurement() > 8

