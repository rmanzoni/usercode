import ROOT
import sys
import math
import style
from files import *
from array import array
from utils import *
from copy import deepcopy as dc
from DataFormats.FWLite import Events, Handle

ROOT.TH1.SetDefaultSumw2()

events = Events (
myFiles
# ['/afs/cern.ch/work/m/manzoni/TauHLT/CMSSW_5_3_14_patch2_trg/src/TriggerStudies/Tau/test/patTuple.root',] 
# ['/afs/cern.ch/work/m/manzoni/TauHLT/CMSSW_5_3_14_patch2_trg/src/TriggerStudies/Tau/test/patTuple_loosenIter0Jet_v2.root',] 
# ['/afs/cern.ch/work/m/manzoni/TauHLT/CMSSW_5_3_14_patch2_trg/src/TriggerStudies/Tau/test/patTuple_originalIter0Jet_v2.root',] 
)

bins = array('d',[0.,17.5,20.,22.5,25.,30.,40.,50.,60.,80.,120.,180.,250.,500.])

cut_flow                   = ROOT.TH1F ('cut_flow'                  , 'cut_flow'              , 12, 0, 12        )
offline_mu_pt              = ROOT.TH1F ('offline_mu_pt'             , 'offline #mu  p_{T}'    , len(bins)-1, bins)
offline_tau_pt             = ROOT.TH1F ('offline_tau_pt'            , 'offline #tau p_{T}'    , len(bins)-1, bins)
trigger_tau_pt             = ROOT.TH1F ('trigger_tau_pt'            , 'trigger #tau p_{T}'    , len(bins)-1, bins)
triggerDecayMode_tau_pt    = ROOT.TH1F ('triggerDecayMode_tau_pt'   , 'trigger #tau p_{T}'    , len(bins)-1, bins)
triggerIsolation_tau_pt    = ROOT.TH1F ('triggerIsolation_tau_pt'   , 'trigger #tau p_{T}'    , len(bins)-1, bins)
offline_tau_genpt          = ROOT.TH1F ('offline_tau_genpt'         , 'offline #tau gen p_{T}', len(bins)-1, bins)
trigger_tau_genpt          = ROOT.TH1F ('trigger_tau_genpt'         , 'trigger #tau gen p_{T}', len(bins)-1, bins)
triggerDecayMode_tau_genpt = ROOT.TH1F ('triggerDecayMode_tau_genpt', 'trigger #tau gen p_{T}', len(bins)-1, bins)
triggerIsolation_tau_genpt = ROOT.TH1F ('triggerIsolation_tau_genpt', 'trigger #tau gen p_{T}', len(bins)-1, bins)
badTausDM                  = ROOT.TH1F ('badTausDM'                 , 'badTausDM'             , 7,0,7            ) 
allTausDM                  = ROOT.TH1F ('allTausDM'                 , 'allTausDM'             , 7,0,7            ) 

dRTauLT = ROOT.TH1F ('dRTauLT', 'dRTauLT', 30,0,0.6 ) 

dz_pixVtx_tauVtx = ROOT.TH1F ('dz_pixVtx_tauVtx', 'dz_pixVtx_tauVtx', 100,-20,20 ) 
dz_muVtx_tauVtx  = ROOT.TH1F ('dz_muVtx_tauVtx' , 'dz_muVtx_tauVtx' , 100,-20,20 ) 
isHighestPtSum   = ROOT.TH1F ('isHighestPtSum'  , 'isHighestPtSum'  , 2 ,0,2  ) 

for hist in [badTausDM, allTausDM] :
  hist.GetXaxis().SetBinLabel(1,'oneProng0Pi0'   )
  hist.GetXaxis().SetBinLabel(2,'oneProng1Pi0'   )
  hist.GetXaxis().SetBinLabel(3,'oneProng2Pi0'   )
  hist.GetXaxis().SetBinLabel(4,'oneProngOther'  )
  hist.GetXaxis().SetBinLabel(5,'threeProng0Pi0' )
  hist.GetXaxis().SetBinLabel(6,'threeProng1Pi0' )
  hist.GetXaxis().SetBinLabel(7,'threeProngOther')

tracksHists = { 'pass_onlineTrk'                : [] ,
                'pass_offlineTrk'               : [] ,
                'fail_without_online_offlineTrk': [] ,
                'fail_with_online_onlineTrk'    : [] ,
                'fail_with_online_offlineTrk'   : [] }

for key in tracksHists.keys() :
  pt                         = ROOT.TH1F(key+'_pt'                        , 'pt'                       , 40,    0, 200 )
  errPtOverPt                = ROOT.TH1F(key+'_errPtOverPt'               , 'errPtOverPt'              , 40,    0, 200 )
  eta                        = ROOT.TH1F(key+'_eta'                       , 'eta'                      , 25, -2.5, 2.5 )
  phi                        = ROOT.TH1F(key+'_phi'                       , 'phi'                      , 25,   -4, 4   )
  chi2                       = ROOT.TH1F(key+'_chi2'                      , 'chi2'                     , 40,    0, 40  )
  ndof                       = ROOT.TH1F(key+'_ndof'                      , 'ndof'                     , 40,    0, 40  )
  normalizedChi2             = ROOT.TH1F(key+'_normalizedChi2'            , 'normalizedChi2'           , 20,    0, 5   )
  numberOfLostHits           = ROOT.TH1F(key+'_numberOfLostHits'          , 'numberOfLostHits'         , 10,    0, 10  )
  numberOfValidHits          = ROOT.TH1F(key+'_numberOfValidHits'         , 'numberOfValidHits'        , 30,    0, 30  )
  numberOfValidPixelHits     = ROOT.TH1F(key+'_numberOfValidPixelHits'    , 'numberOfValidPixelHits'   , 10,    0, 10  )
  numberOfValidTrackerHits   = ROOT.TH1F(key+'_numberOfValidTrackerHits'  , 'numberOfValidTrackerHits' , 30,    0, 30  )
  dxy_offVtx                 = ROOT.TH1F(key+'_dxy_offVtx'                , 'dxy_offVtx'               , 80,   -2, 2   )
  dz_offVtx                  = ROOT.TH1F(key+'_dz_offVtx'                 , 'dz_offVtx'                , 80,  -20, 20  )
  dxy_hltPixVtx              = ROOT.TH1F(key+'_dxy_hltPixVtx'             , 'dxy_hltPixVtx'            , 80,   -2, 2   )
  dz_hltPixVtx               = ROOT.TH1F(key+'_dz_hltPixVtx'              , 'dz_hltPixVtx'             , 80,  -20, 20  )
  dxy_hltMuVtx               = ROOT.TH1F(key+'_dxy_hltMuVtx'              , 'dxy_hltMuVtx'             , 80,   -2, 2   )
  dz_hltMuVtx                = ROOT.TH1F(key+'_dz_hltMuVtx'               , 'dz_hltMuVtx'              , 80,  -20, 20  )
  dRoffline                  = ROOT.TH1F(key+'_dRoffline'                 , 'dRoffline'                , 20,    0, 2   )
  dRonline                   = ROOT.TH1F(key+'_dRonline'                  , 'dRonline'                 , 20,    0, 2   )
  algo                       = ROOT.TH1F(key+'_algo'                      , 'algo'                     , 20,    0, 20  )
  layer                      = ROOT.TH1F(key+'_layer'                     , 'layer'                    , 20,    0, 20  )
  tracksHists[key] = { 'pt'                       : pt                       , 
                       'errPtOverPt'              : errPtOverPt              , 
                       'eta'                      : eta                      , 
                       'phi'                      : phi                      , 
                       'chi2'                     : chi2                     , 
                       'ndof'                     : ndof                     , 
                       'normalizedChi2'           : normalizedChi2           ,
                       'numberOfLostHits'         : numberOfLostHits         ,
                       'numberOfValidHits'        : numberOfValidHits        ,
                       'numberOfValidPixelHits'   : numberOfValidPixelHits   ,
                       'numberOfValidTrackerHits' : numberOfValidTrackerHits ,
                       'dxy_offVtx'               : dxy_offVtx               , 
                       'dz_offVtx'                : dz_offVtx                ,
                       'dxy_hltPixVtx'            : dxy_hltPixVtx            , 
                       'dz_hltPixVtx'             : dz_hltPixVtx             ,
                       'dxy_hltMuVtx'             : dxy_hltMuVtx             ,
                       'dz_hltMuVtx'              : dz_hltMuVtx              , 
                       'dRoffline'                : dRoffline                , 
                       'dRonline'                 : dRonline                 ,
                       'algo'                     : algo                     ,
                       'layer'                    : algo                     ,}

handlePatMu   = Handle ('std::vector<pat::Muon>')
handlePatTau  = Handle ('std::vector<pat::Tau>')
handlePF      = Handle ('std::vector<reco::PFCandidate>')
handleVtx     = Handle ('std::vector<reco::Vertex>')
handleOnlTrk  = Handle ('std::vector<reco::Track>')
handleTrkJet  = Handle ('std::vector<reco::TrackJet>')
handleOnlJets = Handle ('std::vector<reco::CaloJet>')

labelOfflineMu    = ('selectedMuons')
labelPF           = ('particleFlow')
labelPFhlt        = ('hltParticleFlowForTaus')
labelOnlTrk       = ('hltPFMuonMerging')
labelOfflineTau   = ('selectedTaus')
# labelTriggerTau   = ('selectedHltPatTaus')           ## hltIsoMuonVertex
labelTriggerTau   = ('selectedHltPatTausStdVtx')     ## hltPixelVertices
labelOfflineVtx   = ('selectedPrimaryVertices')     
labelOnlinePixVtx = ('hltPixelVertices')     
labelOnlineMuVtx  = ('hltIsoMuonVertex')     
labelTrkJetPre0   = ('hltAntiKT5TrackJetsIter0')
labelTrkJet0      = ('hltTrackAndTauJetsIter0')
labelTrkJet1      = ('hltTrackAndTauJetsIter1')
labelTrkJet2      = ('hltTrackAndTauJetsIter2')
labelTrkJet3      = ('hltTrackAndTauJetsIter3')

labelTrkMerg1     = ('hltIter1Merged')
labelTrkMerg2     = ('hltIter2Merged')
labelTrkMerg3     = ('hltIter3Merged')

labelOnlJets      = ('hltAntiKT5CaloJetsPFEt5')
labelOnlIterTrk   = ('hltPFlowTrackSelectionHighPurity')

all    = 0
failed = 0
decayModeCross = []
failingEvents = [28150788,38979698,9377365,34287744,2073115,62411153,61730373,45685986,47009379,4002807,22405779,56029277,18718809,52991929,13991388,1953725,16196942,67886619,16228470,16138268,16277738,27435007,9365765,22024092,28389058,27226213,27228342,30051102,19575720,62078292,3835767,21848492,2682170,11037065,16270377,26689779,24705865,38498563,40177109,6063353,3924919,61479375,24710730,38972916,38951854,56561840,61830800,19760180,16253201,36230639,33444947,12782522,45053556,4441121,66238069,65020368,24505983,11490191,12838373,14199880,53197377,1382277,12812297,1249504,21513095,25618944,16215296,37977062,68700985,40605935,61890250,13727268,65101560,38184411,9353868,38410378,16160789,16273551,63543902,26934110,9368795,37232492,11498432,52813775,52536300,70645969,6524418,9355742,16189544,16190949]  

hasTrackJet = 0


for loopId, event in enumerate(events):

  #if loopId > 500 : break
  if loopId%(events.size()/10)==0 : print '===> \t',int(float(loopId)/float(events.size())*100),'%'
  
  #if event.eventAuxiliary().event() not in failingEvents : continue
  #if event.eventAuxiliary().event() != 61479375 : continue
  
  
  #print '\n\n\n'+'************'*5
  event.getByLabel (labelOfflineMu , handlePatMu )
  offline_muons = handlePatMu.product()

  event.getByLabel (labelOfflineTau, handlePatTau)
  offline_taus  = handlePatTau.product()

  event.getByLabel (labelTriggerTau, handlePatTau)
  trigger_taus  = handlePatTau.product()

  event.getByLabel (labelPF, handlePF)
  PFoff         = handlePF.product()

  event.getByLabel (labelPFhlt, handlePF)
  PFhlt         = handlePF.product()

  event.getByLabel (labelOnlTrk, handleOnlTrk)
  OnlTrk        = handleOnlTrk.product()

  event.getByLabel (labelTrkJet0, handleTrkJet)
  TrkJet0       = handleTrkJet.product()

  event.getByLabel (labelTrkJetPre0, handleTrkJet)
  TrkJetPre0    = handleTrkJet.product()

  event.getByLabel (labelTrkJet1, handleTrkJet)
  TrkJet1       = handleTrkJet.product()

  event.getByLabel (labelTrkJet2, handleTrkJet)
  TrkJet2       = handleTrkJet.product()

  event.getByLabel (labelTrkJet3, handleTrkJet)
  TrkJet3       = handleTrkJet.product()



  event.getByLabel (labelTrkMerg1, handleOnlTrk)
  TrkMerg1      = handleOnlTrk.product()

  event.getByLabel (labelTrkMerg2, handleOnlTrk)
  TrkMerg2      = handleOnlTrk.product()

  event.getByLabel (labelTrkMerg3, handleOnlTrk)
  TrkMerg3      = handleOnlTrk.product()



  event.getByLabel (labelOnlJets, handleOnlJets)
  OnlJets       = handleOnlJets.product()

  event.getByLabel (labelOnlIterTrk, handleOnlTrk)
  OnlIterTrk    = handleOnlTrk.product()

  event.getByLabel (labelOfflineVtx, handleVtx)
  OffVtx        = handleVtx.product()

  event.getByLabel (labelOnlinePixVtx, handleVtx)
  OnlPixVtx     = handleVtx.product()

  event.getByLabel (labelOnlineMuVtx, handleVtx)
  OnlMuVtx      = handleVtx.product()

  #OffVtx =  sort_by_pt2(OffVtx, reverse=True) 
  OffVtx    = [ vtx for vtx in OffVtx if vtx.ndof>4 and abs(vtx.z())<24. and abs(vtx.position().rho())<2.                    ] 
  goodMuons = [ mu  for mu  in offline_muons if kinematics(mu , pt=15., eta=2.1) and muonID(mu)                              ]
  vetoMuons = [ mu  for mu  in offline_muons if kinematics(mu , pt=15., eta=2.4) and muonID(mu, threshold=0.3, fullID=False) ]
  goodTaus  = [ tau for tau in offline_taus  if kinematics(tau, pt=20., eta=2.3) and TauID(tau) and bool(tau.genJet())       ]

  if len(OffVtx)    <  1                               : continue 
  if len(goodMuons) != 1                               : continue 
  if len(vetoMuons) >  1                               : continue 
  if len(goodTaus)  != 1                               : continue  
  if abs(OffVtx[0].z()-goodTaus[0].vertex().z()) > 0.2 : continue  
  if goodTaus[0].charge() * goodMuons[0].charge() >= 0 : continue
  if deltaR(goodTaus[0], goodMuons[0]) < 0.5           : continue      
  #mass = buildMass(goodTaus[0], goodMuons[0])
  #if mass > 85. and mass < 95.                         : continue 
  
  tau = goodTaus [0]
  mu  = goodMuons[0]

  taus = best_matching([tau], trigger_taus, dR=0.5)
  
  index = 0
  genJetConstituents = []
  while True :
    if bool(tau.genJet().getGenConstituent(index)) :
     genJetConstituents.append(tau.genJet().getGenConstituent(index))
     index += 1
    else :
      break

  genDM = genDecayMode(genJetConstituents)
  if genDM[0] < 0 :
    print 'event: ',event.eventAuxiliary().event(),'\t gen Tau is not a good hadronic tau \t SKIPPING' 
    continue
  
  if tau.leadPFChargedHadrCand().trackRef().isNull() :
    print 'event: ',event.eventAuxiliary().event(),'\t good offline Tau leading track has invalid leadPFChargedHadrCand().trackRef()\t SKIPPING' 
    continue
  else :
    offlineLeadTrack =  tau.leadPFChargedHadrCand().trackRef()

  decayModeCross.append([genDM[1],decayModeDict[tau.decayMode()]])
        
  PFCandsHLT = best_matching([offlineLeadTrack], [cand for cand in PFhlt if cand.charge()!=0], dR=0.1)
  PFCandsOff = best_matching([offlineLeadTrack], [cand for cand in PFoff if cand.charge()!=0], dR=0.1)
      
  offline_tau_pt   .Fill(tau.pt()         )        
  offline_tau_genpt.Fill(tau.genJet().pt())        
  
  if taus[tau] is False                        : continue
  trigger_tau_pt.Fill(tau.pt())    
  trigger_tau_genpt.Fill(tau.genJet().pt())    
  allTausDM.Fill(genDM[1],1.)
  all += 1

  if taus[tau].tauID('decayModeFinding') < 0.5 : #### DANGER CHANGE SIGN!!!
#     print '\nFailing DM online \tevent: ',event.eventAuxiliary().event()
#     print 'has online track?', PFCandsHLT.values()[0]
#     #print 'leading track', offlineLeadTrack.charge(), offlineLeadTrack.eta(), offlineLeadTrack.phi(), offlineLeadTrack.pt(), 'genDM', genDM, 'recoDM', tau.decayMode()
#     ##for i,tr in enumerate(PFhlt) : 
#     #import pdb ; pdb.set_trace()
#     #for i,tr in enumerate(OnlTrk) : 
#     #  if deltaR(taus[tau],tr)<0.5 and tr.charge() != 0 :
#     #    print i, tr.charge(), deltaR(taus[tau],tr), tr.eta(), tr.phi(), tr.pt() 
# 
#     myGoodJet = False
# 
#     for jet in OnlJets :
#       if deltaR(jet,taus[tau])>0.5 : continue 
#       ptIn  = 0.
#       ptOut = 0.
#       for tower in jet.getCaloConstituents() :
#         mydR = deltaR(tower,jet) * deltaR(tower,jet)
#         if   mydR < 0.2 : ptIn  += tower.pt()
#         elif mydR < 0.5 : ptOut += tower.pt()
#       
#       try    : frac = ptIn / (ptIn + ptOut)
#       except : frac = 0.
#       if frac < 0.7 : 
#         print 'BAD event\t',event.eventAuxiliary().event(), '\tfrac', frac  
#         #import pdb ; pdb.set_trace()
#         continue
#   
#       nmatch   = 0
#       nmatchpt = 0
#       for trkJetObj in TrkJet0 :
#         for trk in trkJetObj.tracks() :
#           if trk.isNonnull() and trk.isAvailable() :
#             if deltaR(trk, jet) < 0.5 :
#               nmatch += 1
#               nmatchpt += trk.pt()
#       
#       if nmatch>0 or nmatchpt>1 : 
#         print 'BAD event\t',event.eventAuxiliary().event(), '\tnmatch',nmatch, '\tnmatchpt', nmatchpt 
#         #import pdb ; pdb.set_trace()
#         continue
#   
#       nmatch2   = 0
#       nmatchpt2 = 0
#       for trk in OnlIterTrk :
#         if deltaR(trk, jet) < 0.5 :
#           nmatch2 += 1
#           nmatchpt2 += trk.pt()
#           
#       if nmatchpt2 / jet.pt() > 0.3 : 
#         print 'BAD event\t',event.eventAuxiliary().event(), '\tfracChargedPU',   nmatchpt2 / jet.pt()
#         #import pdb ; pdb.set_trace()
#         continue
#     
#       print 'this fucking jet should pass Iter0!'
#       print 'GOOD event\t',event.eventAuxiliary().event(), '\tfrac', frac  
#       print 'GOOD event\t',event.eventAuxiliary().event(), '\tnmatch',nmatch, '\tnmatchpt', nmatchpt 
#       print 'GOOD event\t',event.eventAuxiliary().event(), '\tfracChargedPU',   nmatchpt2 / jet.pt()
#       print 'GOOD event\t',event.eventAuxiliary().event(), '\tdR(tau,goodJet)',  deltaR(tau,jet)
#       myGoodJet = dc(jet)
#     
#     print '\t\tVertex discance', abs(OnlPixVtx[0].z() - OffVtx[0].z()), 'z onl',OnlPixVtx[0].z(), 'z off',OffVtx[0].z()
#     
#     
#     for trkJetObj in TrkJet0 :
#       #if bool(myGoodJet) is not False :
#       #  if deltaR(myGoodJet, trkJetObj)<0.5 : import pdb ; pdb.set_trace()
#       if deltaR(offlineLeadTrack, trkJetObj) < 0.1 : 
#         if myGoodJet is not False : print '\t\tMATCHED AT ITER 0\t\t tracks associated to this TrakJet', len(trkJetObj.tracks()),'\t deltaR(offlineLeadTrack,myGoodJet)', deltaR(offlineLeadTrack,myGoodJet), '\t dz', offlineLeadTrack.dz(myGoodJet.vertex())
#         else: print '\t\tMATCHED AT ITER 0\t\t tracks associated to this TrakJet', len(trkJetObj.tracks())
#         hasTrackJet += 1
#       for trk in trkJetObj.tracks() :
#         if trk.isNonnull() and trk.isAvailable() :
#           #print 'trk0', trk.pt(), trk.charge(), trk.eta(), trk.phi()
#           if deltaR(offlineLeadTrack, trk) < 0.1 :          print '\t\ttrk0', trk.pt(), trk.charge(), trk.eta(), trk.phi(), deltaR(offlineLeadTrack, trk), '\t\tMATCHED AT ITER 0'
# 
#     #import pdb ; pdb.set_trace()
# 
#           
#     for trkJetObj in TrkJet1 :
#       if deltaR(offlineLeadTrack, trkJetObj) < 0.1 : print '\t\tMATCHED AT ITER 1\t\t tracks associated to this TrakJet', len(trkJetObj.tracks())
#       for trk in trkJetObj.tracks() :
#         if trk.isNonnull() and trk.isAvailable() :
#           #print 'trk1', trk.pt(), trk.charge(), trk.eta(), trk.phi()
#           if deltaR(offlineLeadTrack, trk) < 0.1 :          print '\t\ttrk0', trk.pt(), trk.charge(), trk.eta(), trk.phi(), deltaR(offlineLeadTrack, trk), '\t\tMATCHED AT ITER 1'
# 
#     for trkJetObj in TrkJet2 :
#       if deltaR(offlineLeadTrack, trkJetObj) < 0.1 : print '\t\tMATCHED AT ITER 2\t\t tracks associated to this TrakJet', len(trkJetObj.tracks())
#       for trk in trkJetObj.tracks() :
#         if trk.isNonnull() and trk.isAvailable() :
#           #print 'trk2', trk.pt(), trk.charge(), trk.eta(), trk.phi()
#           if deltaR(offlineLeadTrack, trk) < 0.1 :          print '\t\ttrk0', trk.pt(), trk.charge(), trk.eta(), trk.phi(), deltaR(offlineLeadTrack, trk), '\t\tMATCHED AT ITER 2'
# 
#     for trkJetObj in TrkJet3 :
#       if deltaR(offlineLeadTrack, trkJetObj) < 0.1 : print '\t\tMATCHED AT ITER 3\t\t tracks associated to this TrakJet', len(trkJetObj.tracks())
#       for trk in trkJetObj.tracks() :
#         if trk.isNonnull() and trk.isAvailable() :
#           #print 'trk3', trk.pt(), trk.charge(), trk.eta(), trk.phi()
#           if deltaR(offlineLeadTrack, trk) < 0.1 :          print '\t\ttrk0', trk.pt(), trk.charge(), trk.eta(), trk.phi(), deltaR(offlineLeadTrack, trk), '\t\tMATCHED AT ITER 3'
#     
#     #import pdb ; pdb.set_trace()

    failed += 1
    badTausDM.Fill(genDM[1],1.)
    if PFCandsHLT.values()[0] is not False :
      #import pdb ; pdb.set_trace()
      #print ''
      #print 'event: ',event.eventAuxiliary().event()
      #print 'distance Onl Pix vertex vs Off vertex'
      #print 'z\t ',abs(OnlPixVtx[0].position().z() - OffVtx[0].position().z())
      #print 'distance Onl Mu vertex vs Off vertex'
      #print 'z\t ',abs(OnlMuVtx[0].position().z() - OffVtx[0].position().z())
      #print 'distance Onl Pix vertex vs Tau vertex'
      #print 'z\t ',abs(OnlPixVtx[0].position().z() - tau.vertex().z())
      #print 'distance Onl Mu vertex vs Tau vertex'
      #print 'z\t ',abs(OnlMuVtx[0].position().z() - tau.vertex().z())
      #print 'distance Off vertex vs Tau vertex'
      #print 'z\t ',abs(OffVtx[0].position().z() - tau.vertex().z())
      #dz_pixVtx_tauVtx.Fill(OnlPixVtx[0].position().z() - tau.vertex().z())
      #dz_muVtx_tauVtx .Fill(OffVtx[0].position().z() - tau.vertex().z()   ) 
      #print OnlPixVtx[0].position().z() - tau.vertex().z()
      #closestVert = find_closest_vertex(OnlPixVtx[0], OffVtx)
      #isHighest = closestVert.p4().pt() >= OffVtx[0].p4().pt()
      #isHighestPtSum.Fill(isHighest*'is highest #sumpT^{2}'+ (1-isHighest)*'is not highest #sumpT^{2}',1.)
      #print 'offline vertex index', OffVtx.index(closestVert)
      #print 'onl leading track - onl tau jet dR', deltaR(PFCandsHLT.values()[0].trackRef(),taus[tau]), '\t GenDM', genDM, '\t RecoDM', tau.decayMode()
      dRTauLT.Fill(deltaR(PFCandsHLT.values()[0].trackRef(),taus[tau]))
      fillTrackHistos(tracksHists['fail_with_online_onlineTrk' ]   , PFCandsHLT.values()[0].trackRef(), OffVtx[0].position(), OnlPixVtx[0].position(), OnlMuVtx[0].position(), tau, taus[tau] )
      fillTrackHistos(tracksHists['fail_with_online_offlineTrk']   , offlineLeadTrack                 , OffVtx[0].position(), OnlPixVtx[0].position(), OnlMuVtx[0].position(), tau, taus[tau] )
    else :
      fillTrackHistos(tracksHists['fail_without_online_offlineTrk'], offlineLeadTrack                 , OffVtx[0].position(), OnlPixVtx[0].position(), OnlMuVtx[0].position(), tau, taus[tau] )
      dz_pixVtx_tauVtx.Fill(OnlPixVtx[0].position().z() - tau.vertex().z())
      dz_muVtx_tauVtx .Fill(OffVtx[0].position().z() - tau.vertex().z()   ) 
    continue

  #import pdb ; pdb.set_trace()

  if PFCandsHLT.values()[0] is False :
    print 'event: ',event.eventAuxiliary().event(),'\t online leading Track does not match with offline leading track \t SKIPPING' 
    continue

  #dz_pixVtx_tauVtx.Fill(OnlPixVtx[0].position().z() - tau.vertex().z())
  #dz_muVtx_tauVtx .Fill(OffVtx[0].position().z() - tau.vertex().z()   ) 

  closestVert = find_closest_vertex(OnlPixVtx[0], OffVtx)
  isHighest = closestVert.p4().pt() >= OffVtx[0].p4().pt()
  isHighestPtSum.Fill(isHighest*'is highest #sumpT^{2}'+ (1-isHighest)*'is not highest #sumpT^{2}',1.)

  
  fillTrackHistos(tracksHists['pass_onlineTrk' ], PFCandsHLT.values()[0].trackRef(), OffVtx[0].position(), OnlPixVtx[0].position(), OnlMuVtx[0].position(), tau, taus[tau])
  fillTrackHistos(tracksHists['pass_offlineTrk'], offlineLeadTrack                 , OffVtx[0].position(), OnlPixVtx[0].position(), OnlMuVtx[0].position(), tau, taus[tau])

  triggerDecayMode_tau_pt.Fill(tau.pt()) 
  triggerDecayMode_tau_genpt.Fill(tau.genJet().pt()) 
  
  if taus[tau].tauID('byIsolation')      < 0.5 : continue
  triggerIsolation_tau_pt.Fill(tau.pt()) 
  triggerIsolation_tau_genpt.Fill(tau.genJet().pt()) 
  #import pdb ; pdb.set_trace()

plotting(offline_tau_pt   , trigger_tau_pt   , triggerDecayMode_tau_pt   , triggerIsolation_tau_pt   , allTausDM, badTausDM, 'reco')
plotting(offline_tau_genpt, trigger_tau_genpt, triggerDecayMode_tau_genpt, triggerIsolation_tau_genpt, allTausDM, badTausDM, 'gen' )

outfile = ROOT.TFile.Open('out.root','recreate')

outfile.cd()

for key in tracksHists.keys() :
  outfile.mkdir(key)
  outfile.cd(key)
  for key2 in tracksHists[key].keys() :
    tracksHists[key][key2].Write()
    
outfile.Close()           

crossDM = ROOT.TH2F('','',7,0,7,16,0,16)
crossDM.GetXaxis().SetBinLabel(1,'oneProng0Pi0'   )
crossDM.GetXaxis().SetBinLabel(2,'oneProng1Pi0'   )
crossDM.GetXaxis().SetBinLabel(3,'oneProng2Pi0'   )
crossDM.GetXaxis().SetBinLabel(4,'oneProngOther'  )
crossDM.GetXaxis().SetBinLabel(5,'threeProng0Pi0' )
crossDM.GetXaxis().SetBinLabel(6,'threeProng1Pi0' )
crossDM.GetXaxis().SetBinLabel(7,'threeProngOther')

crossDM.GetYaxis().SetBinLabel(1 ,'kOneProng0PiZero'  )
crossDM.GetYaxis().SetBinLabel(2 ,'kOneProng1PiZero'  )
crossDM.GetYaxis().SetBinLabel(3 ,'kOneProng2PiZero'  )
crossDM.GetYaxis().SetBinLabel(4 ,'kOneProng3PiZero'  )
crossDM.GetYaxis().SetBinLabel(5 ,'kOneProngNPiZero'  )
crossDM.GetYaxis().SetBinLabel(6 ,'kTwoProng0PiZero'  )
crossDM.GetYaxis().SetBinLabel(7 ,'kTwoProng1PiZero'  )
crossDM.GetYaxis().SetBinLabel(8 ,'kTwoProng2PiZero'  )
crossDM.GetYaxis().SetBinLabel(9 ,'kTwoProng3PiZero'  )
crossDM.GetYaxis().SetBinLabel(10,'kTwoProngNPiZero'  )
crossDM.GetYaxis().SetBinLabel(11,'kThreeProng0PiZero')
crossDM.GetYaxis().SetBinLabel(12,'kThreeProng1PiZero')
crossDM.GetYaxis().SetBinLabel(13,'kThreeProng2PiZero')
crossDM.GetYaxis().SetBinLabel(14,'kThreeProng3PiZero')
crossDM.GetYaxis().SetBinLabel(15,'kThreeProngNPiZero')
crossDM.GetYaxis().SetBinLabel(16,'kRareDecayMode'    )

for entry in decayModeCross :
  crossDM.Fill(entry[0],entry[1],1.)

c2 = ROOT.TCanvas('','',700,700)
ROOT.gPad.SetLeftMargin(0.30)
ROOT.gPad.SetRightMargin(0.20)
ROOT.gPad.SetBottomMargin(0.18)
ROOT.gPad.SetFrameLineWidth(3)
ROOT.gPad.SetGridx(1)
ROOT.gPad.SetGridy(1)
crossDM.Draw('TEXTCOLZ')
c2.SaveAs('myTH2.pdf')


c3 = ROOT.TCanvas('','',700,700)
ROOT.gPad.SetLeftMargin(0.18)
ROOT.gPad.SetBottomMargin(0.18)
ROOT.gPad.SetFrameLineWidth(3)
ROOT.gPad.SetGridx(1)
ROOT.gPad.SetGridy(1)

dRTauLT.SetTitle('')
dRTauLT.GetXaxis().SetTitle('Online #DeltaR(#tau,leading track)')
dRTauLT.GetYaxis().SetTitle('events')
dRTauLT.GetYaxis().SetTitleOffset(1.3)
dRTauLT.SetMarkerStyle(9)
dRTauLT.SetLineColor(ROOT.kRed)
dRTauLT.SetLineWidth(2)
dRTauLT.Draw('E')
c3.SaveAs('association.pdf')


c4 = ROOT.TCanvas('','',700,700)
ROOT.gPad.SetLeftMargin(0.18)
ROOT.gPad.SetBottomMargin(0.18)
ROOT.gPad.SetFrameLineWidth(3)
ROOT.gPad.SetGridx(1)
ROOT.gPad.SetGridy(1)
# ROOT.gPad.SetLogx(True)

dz_pixVtx_tauVtx.SetTitle('')
dz_pixVtx_tauVtx.GetXaxis().SetTitle('dz_{(online pix PV, offline PV)} [cm]')
dz_pixVtx_tauVtx.GetYaxis().SetTitle('events')
dz_pixVtx_tauVtx.GetYaxis().SetTitleOffset(1.5)
dz_pixVtx_tauVtx.GetXaxis().SetTitleOffset(1.5)
dz_pixVtx_tauVtx.SetMarkerStyle(9)
dz_pixVtx_tauVtx.SetLineColor(ROOT.kRed)
dz_pixVtx_tauVtx.SetLineWidth(2)
dz_pixVtx_tauVtx.Draw('E')
c4.SaveAs('dz_pixVtx_tauVtx.pdf')

dz_muVtx_tauVtx.SetTitle('')
dz_muVtx_tauVtx.GetXaxis().SetTitle('dz_{(online muon PV, offline PV)} [cm]')
dz_muVtx_tauVtx.GetYaxis().SetTitle('events')
dz_muVtx_tauVtx.GetYaxis().SetTitleOffset(1.5)
dz_muVtx_tauVtx.GetXaxis().SetTitleOffset(1.5)
dz_muVtx_tauVtx.SetMarkerStyle(9)
dz_muVtx_tauVtx.SetLineColor(ROOT.kRed)
dz_muVtx_tauVtx.SetLineWidth(2)
dz_muVtx_tauVtx.Draw('E')
c4.SaveAs('dz_muVtx_tauVtx.pdf')


ROOT.gPad.SetLogx(False)

isHighestPtSum.SetTitle('')
isHighestPtSum.GetXaxis().SetTitle('')
isHighestPtSum.GetYaxis().SetTitle('event fraction')
isHighestPtSum.GetYaxis().SetTitleOffset(1.5)
isHighestPtSum.SetMarkerStyle(9)
isHighestPtSum.SetLineColor(ROOT.kRed)
isHighestPtSum.SetLineWidth(2)
isHighestPtSum.DrawNormalized('E')
c4.SaveAs('isHighestPtSum.pdf')


print all
print failed
print hasTrackJet
