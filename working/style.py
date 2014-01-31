from ROOT import gROOT, gStyle
import ROOT

### style parameters
gROOT.SetStyle("Plain")
gROOT.SetBatch(True)
gStyle.SetLegendFillColor(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetStatBorderSize(0)
gStyle.SetTitleBorderSize(0)
gStyle.SetOptStat(0)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
# gStyle.SetTitleX(0.14) ## to be changed to 0.15 with preliminary
gStyle.SetTitleSize(0.040,'t')
# gStyle.SetTitleOffset(1.200,"X")
gStyle.SetTitleX(-0.038) ## to be changed to 0.15
gStyle.SetTitleY(0.96)
gStyle.SetTitleW(0.8)
gStyle.SetTextFont(42)
gStyle.SetLegendFont(42)
# gStyle.SetLabelSize(0.040,'xy')
gStyle.SetLabelFont(42, 'xy')
# gStyle.SetTitleFont(42, 'xy')
# gStyle.SetTitleSize(0.105,'xy')



# from array import array
# 
# bins = array('d',[0.,17.5,20.,22.5,25.,30.,40.,50.,60.,80.,120.])
# 
# cut_flow = ROOT.TH1F ('cut_flow', 'cut_flow', 12, 0, 12)
# 
# offline_mu_pt              = ROOT.TH1F ('offline_mu_pt'             , 'offline #mu  p_{T}'    , len(bins)-1, bins)
# offline_tau_pt             = ROOT.TH1F ('offline_tau_pt'            , 'offline #tau p_{T}'    , len(bins)-1, bins)
# trigger_tau_pt             = ROOT.TH1F ('trigger_tau_pt'            , 'trigger #tau p_{T}'    , len(bins)-1, bins)
# triggerDecayMode_tau_pt    = ROOT.TH1F ('triggerDecayMode_tau_pt'   , 'trigger #tau p_{T}'    , len(bins)-1, bins)
# triggerIsolation_tau_pt    = ROOT.TH1F ('triggerIsolation_tau_pt'   , 'trigger #tau p_{T}'    , len(bins)-1, bins)
# offline_tau_genpt          = ROOT.TH1F ('offline_tau_genpt'         , 'offline #tau gen p_{T}', len(bins)-1, bins)
# trigger_tau_genpt          = ROOT.TH1F ('trigger_tau_genpt'         , 'trigger #tau gen p_{T}', len(bins)-1, bins)
# triggerDecayMode_tau_genpt = ROOT.TH1F ('triggerDecayMode_tau_genpt', 'trigger #tau gen p_{T}', len(bins)-1, bins)
# triggerIsolation_tau_genpt = ROOT.TH1F ('triggerIsolation_tau_genpt', 'trigger #tau gen p_{T}', len(bins)-1, bins)
# badTausDM                  = ROOT.TH1F ('badTausDM'                  ,'badTausDM'             , 15,0,15            ) 
# allTausDM                  = ROOT.TH1F ('allTausDM'                  ,'allTausDM'             , 15,0,15            ) 
# 
# histos = {}
# histos.update({'offline_wo_online':{}})
# histos['offline_wo_online'].update({'chi2'                                  : ROOT.TH1F('chi2'                                   , 'chi2()                                 '    , 40, 0, 20)})
# histos['offline_wo_online'].update({'ndof'                                  : ROOT.TH1F('ndof'                                   , 'ndof()                                 '    , 40, 0, 40)})
# histos['offline_wo_online'].update({'normalizedChi2'                        : ROOT.TH1F('normalizedChi2'                         , 'normalizedChi2()                       '    , 20, 0, 20)})
# histos['offline_wo_online'].update({'numberOfLostHits'                      : ROOT.TH1F('numberOfLostHits'                       , 'numberOfLostHits()                     '    , 20, 0, 20)})
# histos['offline_wo_online'].update({'numberOfValidHits'                     : ROOT.TH1F('numberOfValidHits'                      , 'numberOfValidHits()                    '    , 20, 0, 20)})
# histos['offline_wo_online'].update({'highPurity'                            : ROOT.TH1F('highPurity'                             , 'highPurity                             '    , 5 , 0, 5 )})
# histos['offline_wo_online'].update({'hitPattern().numberOfValidPixelHits'   : ROOT.TH1F('hitPattern().numberOfValidPixelHits'    , 'hitPattern().numberOfValidPixelHits()  '    , 20, 0, 20)})
# histos['offline_wo_online'].update({'hitPattern().numberOfValidTrackerHits' : ROOT.TH1F('hitPattern().numberOfValidTrackerHits'  , 'hitPattern().numberOfValidTrackerHits()'    , 20, 0, 20)})
# histos['offline_wo_online'].update({'dxy(offlineVtx)'                       : ROOT.TH1F('dxy(offlineVtx)'                        , 'dxy(offlineVtx)                        '    , 40, 0, 2 )})
# histos['offline_wo_online'].update({'dz(offlineVtx)'                        : ROOT.TH1F('dz(offlineVtx)'                         , 'dz(offlineVtx)                         '    , 40, 0, 20)})
