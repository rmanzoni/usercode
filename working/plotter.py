import ROOT

from copy import deepcopy as dc

### style parameters
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetLegendFillColor(0)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetStatBorderSize(0)
ROOT.gStyle.SetTitleBorderSize(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
# ROOT.gStyle.SetTitleX(0.14) ## to be changed to 0.15 with preliminary
ROOT.gStyle.SetTitleSize(0.040,'t')
# ROOT.gStyle.SetTitleOffset(1.200,"X")
ROOT.gStyle.SetTitleX(-0.038) ## to be changed to 0.15
ROOT.gStyle.SetTitleY(0.96)
ROOT.gStyle.SetTitleW(0.8)
ROOT.gStyle.SetTextFont(42)
ROOT.gStyle.SetLegendFont(42)	
# ROOT.gStyle.SetLabelSize(0.040,'xy')
ROOT.gStyle.SetLabelFont(42, 'xy')
# ROOT.gStyle.SetTitleFont(42, 'xy')
# ROOT.gStyle.SetTitleSize(0.105,'xy')

def doRatio( num, den ) :
  num1 = dc(num)
  den1 = dc(den)
  ratio = dc(num1)
  ratio.Divide(num1,den1,1.,1.,'b')
  ratio.SetMinimum(0.6)
  ratio.SetMaximum(1.1)
  return ratio  

def plot( basehisto, basehistolegend, name, xaxis, yaxis, title='', morehistos = {}, color = ROOT.kRed, drawoptions = 'E' ) :
  '''
  Plots an histogram, eventually more histos to be drawn with Draw(SAME).
  morehistos should be a dict like {histo:[ROOT.kBlue,'legend entry']}
  '''
  c1 = ROOT.TCanvas('','',700,700)
  
  ROOT.gPad.SetLeftMargin(0.18)
  ROOT.gPad.SetBottomMargin(0.18)
  ROOT.gPad.SetFrameLineWidth(3)
  ROOT.gPad.SetGridx(1)
  ROOT.gPad.SetGridy(1)

  l1 = ROOT.TLegend(0.5,0.3,0.8,0.5)
  l1.AddEntry(basehisto,basehistolegend)
  l1.SetFillColor(0)

  basehisto.SetLineWidth(2)  
  basehisto.SetLineColor(color)
  basehisto.SetMarkerStyle(9)
  basehisto.SetTitle('{TITLE};{XAXIS};{YAXIS}'.format(TITLE=title, XAXIS=xaxis, YAXIS=yaxis))
  basehisto.GetXaxis().SetTitle(xaxis)
  basehisto.GetYaxis().SetTitle(yaxis)
  basehisto.GetYaxis().SetTitleOffset(1.5)
  basehisto.Draw(drawoptions)
  
  for key in morehistos.keys() :
    l1.AddEntry(key,morehistos[key][1])
    key.SetLineWidth(2)  
    key.SetLineColor(morehistos[key][0])
    key.SetMarkerStyle(9)
    key.Draw('SAME'+drawoptions)

  l1.Draw('sameAEPZ')
  
  c1.SaveAs(name+'.pdf')

file = ROOT.TFile.Open('out2.root','read')

file.cd()

variable = '_gen_pt'


offTaus             = ROOT.gDirectory.FindObjectAny('offTaus'             + variable)
onlTauPix           = ROOT.gDirectory.FindObjectAny('onlTauPix'           + variable)
onlTauMu            = ROOT.gDirectory.FindObjectAny('onlTauMu'            + variable)
onlTauMuPassingDM   = ROOT.gDirectory.FindObjectAny('onlTauMuPassingDM'   + variable)
onlTauPixPassingDM  = ROOT.gDirectory.FindObjectAny('onlTauPixPassingDM'  + variable)
onlTauMuPassingIso  = ROOT.gDirectory.FindObjectAny('onlTauMuPassingIso'  + variable)
onlTauPixPassingIso = ROOT.gDirectory.FindObjectAny('onlTauPixPassingIso' + variable)

vert = ROOT.gDirectory.FindObjectAny('pixVtx_failDMonl_noOnlTrk_dz(offlineVtx)')

pixRatio1 = doRatio( onlTauPix          , offTaus )
pixRatio2 = doRatio( onlTauPixPassingDM , offTaus )
pixRatio3 = doRatio( onlTauPixPassingIso, offTaus )

muRatio1 = doRatio( onlTauMu          , offTaus )
muRatio2 = doRatio( onlTauMuPassingDM , offTaus )
muRatio3 = doRatio( onlTauMuPassingIso, offTaus )

# plot( pixRatio1, 'p_{T}>20 GeV', 'pixefficiency', 'offline #tau p_{T} [GeV]', 'efficiency', morehistos = {pixRatio2:[ROOT.kGreen+3,'pass DecayMode'],pixRatio3:[ROOT.kBlue,'pass Isolation']} )
# plot( muRatio1 , 'p_{T}>20 GeV', 'muefficiency' , 'offline #tau p_{T} [GeV]', 'efficiency', morehistos = {muRatio2 :[ROOT.kGreen+3,'pass DecayMode'],muRatio3 :[ROOT.kBlue,'pass Isoaltion']} )

# plot( pixRatio1, 'p_{T}>20 GeV', 'pixefficiency', 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {pixRatio2:[ROOT.kGreen+3,'pass DecayMode'],pixRatio3:[ROOT.kBlue,'pass Isolation']} )
# plot( muRatio1 , 'p_{T}>20 GeV', 'muefficiency' , 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {muRatio2 :[ROOT.kGreen+3,'pass DecayMode'],muRatio3 :[ROOT.kBlue,'pass Isoaltion']} )

plot( pixRatio1, 'p_{T}>20 GeV', 'pixefficiency', 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {pixRatio2:[ROOT.kGreen+3,'pass DecayMode']} )
plot( muRatio1 , 'p_{T}>20 GeV', 'muefficiency' , 'gen #tau p_{T} [GeV]', 'efficiency', morehistos = {muRatio2 :[ROOT.kGreen+3,'pass DecayMode']} )

plot( vert , '', 'dzPix_Off' , 'dz [cm]', 'events' )



















