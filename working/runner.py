import ROOT
import PATreader
from array import array
from files import *

bins = array('d',[0.,17.5,20.,22.5,25.,30.,40.,50.,60.,80.,120.,250.,500,])
# bins = array('d',[0.,17.5,20.,22.5,25.,30.,40.,50.,60.,80.,120.])

basic_histos = {}
names  = ['offTaus'            ,
          'onlTauPix'          ,
          'onlTauMu'           ,
          'onlTauMuPassingDM'  ,
          'onlTauPixPassingDM' ,
          'onlTauMuPassingIso' ,
          'onlTauPixPassingIso']

for name in names :
  basic_histos.update({name:{}})
  basic_histos[name].update({'pt'     : ROOT.TH1F( name+'_pt'     , '' , len(bins)-1, bins)} )
  basic_histos[name].update({'gen_pt' : ROOT.TH1F( name+'_gen_pt' , '' , len(bins)-1, bins)} )
  basic_histos[name].update({'eta'    : ROOT.TH1F( name+'_eta'    , '' , 25, -2.5, 2.5    )} )
  basic_histos[name].update({'phi'    : ROOT.TH1F( name+'_phi'    , '' , 25, -2.5, 2.5    )} )
  basic_histos[name].update({'charge' : ROOT.TH1F( name+'_charge' , '' , 25, -2.5, 2.5    )} )
  basic_histos[name].update({'recoDM' : ROOT.TH1F( name+'_recoDM' , '' , 25, -2.5, 2.5    )} )
  basic_histos[name].update({'genDM'  : ROOT.TH1F( name+'_genDM'  , '' , 25, -2.5, 2.5    )} )

track_histos = {}
names  = ['offTrk_failDMonl_hasOnlTrk_mu' ,
          'onlTrk_failDMonl_hasOnlTrk_mu' ,
          'offTrk_failDMonl_noOnlTrk_mu'  ,
          'offTrk_failDMonl_hasOnlTrk_pix',
          'onlTrk_failDMonl_hasOnlTrk_pix',
          'offTrk_failDMonl_noOnlTrk_pix' ]
 
for name in names :
  track_histos.update({name:{}})
  track_histos[name].update({'pt'                         : ROOT.TH1F( name+'_pt'                        , '' , 24, 0   , 120 )} )
  track_histos[name].update({'errPtOverPt'                : ROOT.TH1F( name+'_errPtOverPt'               , '' , 20, 0   , 100 )} )
  track_histos[name].update({'eta'                        : ROOT.TH1F( name+'_eta'                       , '' , 25, -2.5, 2.5 )} )
  track_histos[name].update({'phi'                        : ROOT.TH1F( name+'_phi'                       , '' , 25, -2.5, 2.5 )} )
  track_histos[name].update({'charge'                     : ROOT.TH1F( name+'_charge'                    , '' , 5 , -2  , 2   )} )
  track_histos[name].update({'chi2'                       : ROOT.TH1F( name+'_chi2'                      , '' , 40, 0   , 20  )} )
  track_histos[name].update({'ndof'                       : ROOT.TH1F( name+'_ndof'                      , '' , 40, 0   , 40  )} )
  track_histos[name].update({'normalizedChi2'             : ROOT.TH1F( name+'_normalizedChi2'            , '' , 20, 0   , 20  )} )
  track_histos[name].update({'numberOfLostHits'           : ROOT.TH1F( name+'_numberOfLostHits'          , '' , 20, 0   , 20  )} )
  track_histos[name].update({'numberOfValidHits'          : ROOT.TH1F( name+'_numberOfValidHits'         , '' , 20, 0   , 20  )} )
  track_histos[name].update({'highPurity'                 : ROOT.TH1F( name+'_highPurity'                , '' , 5 , 0   , 5   )} )
  track_histos[name].update({'numberOfValidPixelHits'     : ROOT.TH1F( name+'_numberOfValidPixelHits'    , '' , 20, 0   , 20  )} )
  track_histos[name].update({'pixelLayersWithMeasurement' : ROOT.TH1F( name+'_pixelLayersWithMeasurement', '' , 20, 0   , 20  )} )
  track_histos[name].update({'numberOfValidTrackerHits'   : ROOT.TH1F( name+'_numberOfValidTrackerHits'  , '' , 20, 0   , 20  )} )
  track_histos[name].update({'dxy(offlineVtx)'            : ROOT.TH1F( name+'_dxy(offlineVtx)'           , '' , 40, 0   , 2   )} )
  track_histos[name].update({'dz(offlineVtx)'             : ROOT.TH1F( name+'_dz(offlineVtx)'            , '' , 40, 0   , 20  )} )
  track_histos[name].update({'dxy(hltPixVtx)'             : ROOT.TH1F( name+'_dxy(hltPixVtx)'            , '' , 40, 0   , 2   )} )
  track_histos[name].update({'dz(hltPixVtx)'              : ROOT.TH1F( name+'_dz(hltPixVtx)'             , '' , 40, 0   , 20  )} )
  track_histos[name].update({'dxy(hltMuVtx)'              : ROOT.TH1F( name+'_dxy(hltMuVtx)'             , '' , 40, 0   , 2   )} )
  track_histos[name].update({'dz(hltMuVtx)'               : ROOT.TH1F( name+'_dz(hltMuVtx)'              , '' , 40, 0   , 20  )} )
  track_histos[name].update({'algo'                       : ROOT.TH1F( name+'_algo'                      , '' , 8 , 0   , 8   )} )
  track_histos[name].update({'dRoffline'                  : ROOT.TH1F( name+'_dRoffline'                 , '' , 40, 0   , 4   )} )
  track_histos[name].update({'dRonline'                   : ROOT.TH1F( name+'_dRonline'                  , '' , 40, 0   , 4   )} )

vertex_histos = {}
names  = ['muVtx_failDMonl_hasOnlTrk' ,
          'pixVtx_failDMonl_hasOnlTrk',
          'muVtx_failDMonl_noOnlTrk'  ,
          'pixVtx_failDMonl_noOnlTrk' ,
          'muVtx_passDMonl_hasOnlTrk' ,
          'pixVtx_passDMonl_hasOnlTrk']

for name in names :
  vertex_histos.update({name:{}})
  vertex_histos[name].update({'dxy(offlineVtx)': ROOT.TH1F( name+'_dxy(offlineVtx)' , '' , 50 , -2 , 2 )} )
  vertex_histos[name].update({'dz(offlineVtx)' : ROOT.TH1F( name+'_dz(offlineVtx)'  , '' , 100, -20, 20)} )


# myFiles = ['/afs/cern.ch/work/m/manzoni/TauHLT/CMSSW_5_3_14_patch2_trg/src/TriggerStudies/Tau/test/patTuple.root',] 
# myFiles = ['/afs/cern.ch/work/m/manzoni/TauHLT/CMSSW_5_3_14_patch2_trg/src/TriggerStudies/Tau/test/patTuple_loosenIter0Jet_v2.root',]  
# myFiles = ['/afs/cern.ch/work/m/manzoni/TauHLT/CMSSW_5_3_14_patch2_trg/src/TriggerStudies/Tau/test/patTuple_originalIter0Jet_v2.root',] 
failingEvents = [28150788,38979698,9377365,34287744,2073115,62411153,61730373,45685986,47009379,4002807,22405779,56029277,18718809,52991929,13991388,1953725,16196942,67886619,16228470,16138268,16277738,27435007,9365765,22024092,28389058,27226213,27228342,30051102,19575720,62078292,3835767,21848492,2682170,11037065,16270377,26689779,24705865,38498563,40177109,6063353,3924919,61479375,24710730,38972916,38951854,56561840,61830800,19760180,16253201,36230639,33444947,12782522,45053556,4441121,66238069,65020368,24505983,11490191,12838373,14199880,53197377,1382277,12812297,1249504,21513095,25618944,16215296,37977062,68700985,40605935,61890250,13727268,65101560,38184411,9353868,38410378,16160789,16273551,63543902,26934110,9368795,37232492,11498432,52813775,52536300,70645969,6524418,9355742,16189544,16190949]  

myAnalyzer = PATreader.PATreader(myFiles, basic_histos=basic_histos, track_histos=track_histos, vertex_histos=vertex_histos, onlineTauPixVtxCollection='onlTausPixVtx2', onlineTauMuVtxCollection='onlTausMuVtx')
myAnalyzer.looper(maxEvents=-1, pickEvents=[], verbose=False)
myAnalyzer.printSummary()

myAnalyzer.returnBasicHistos()
myAnalyzer.returnTrackHistos()

outFile = ROOT.TFile.Open('out2.root','recreate')

outFile.cd()

for key in basic_histos.keys() :
  outFile.mkdir(key)
  outFile.cd(key)
  for histo in basic_histos[key].values() :
    histo.Write()

outFile.cd()

for key in track_histos.keys() :
  outFile.mkdir(key)
  outFile.cd(key)
  for histo in track_histos[key].values() :
    histo.Write()

outFile.cd()

for key in vertex_histos.keys() :
  outFile.mkdir(key)
  outFile.cd(key)
  for histo in vertex_histos[key].values() :
    histo.Write()

outFile.Close()



