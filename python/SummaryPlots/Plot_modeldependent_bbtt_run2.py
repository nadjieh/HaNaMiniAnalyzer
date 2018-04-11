import argparse as argparse
#from RecoLuminosity.LumiDB import argparse
import math
import os
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas
import ROOT
import numpy as np
from array import array
from BR import get_total_width
from BR import gamma_quarks
from BR import gamma_mu
from BR import gamma_tau
from BR import gamma_photon
from BR import gamma_gg

def add_lumi():
    lowX=0.43
    lowY=0.845
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.055)
    lumi.AddText("35.9 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.12
    lowY=0.845
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.055)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi 

def add_Preliminary():
    lowX=0.24
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.04)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(52)
    #lumi.AddText("Preliminary")
    return lumi 

def make_legend():
    output = ROOT.TLegend(0.17, 0.68, 0.6, 0.83, "", "brNDC")
    output.SetLineWidth(0)
    output.SetLineStyle(0)
    output.SetFillStyle(0)
    output.SetBorderSize(0)
    output.SetTextFont(62)
    output.SetTextColor(0)
    return output

def add_model(model):
    lowX=0.21
    lowY=0.74
    #if (args.model==4):
    #   lowY=0.25
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.04)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    0 )
    lumi.SetTextFont(62)
    if str(model)=="1":
       lumi.AddText("2HDM+S type I")
    if str(model)=="2":
       lumi.AddText("2HDM+S type II")
    if str(model)=="3":
       lumi.AddText("2HDM+S type III")
    if str(model)=="4":
       lumi.AddText("2HDM+S type IV")
    return lumi

def add_br(model):
    lowX=0.21
    lowY=0.15
    if (args.model==4):
       lowY=0.15
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.035)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(62)
    #if (args.model==4):
    #   lumi.AddText("B(aa#rightarrow#mu#mu#tau#tau) #in [6.5#times10^{-5}, 1.6#times10^{-3}]")
    #if (args.model==3):
    #   lumi.AddText("B(aa#rightarrow#mu#mu#tau#tau) #in [6.7#times10^{-5}, 6.6#times10^{-3}]")
    return lumi

def frameTH2D(hist, threshold, frameValue=1000):
    # Now supports variable-binned histograms First adds a narrow frame (1% of
    # of bin widths) around the outside with same values as the real edge. Then
    # adds another frame another frame around this one filled with some chosen
    # value that will make the contours close

    # Get lists of the bin edges
    x_bins = [hist.GetXaxis().GetBinLowEdge(x)
              for x in xrange(1, hist.GetNbinsX() + 2)]
    y_bins = [hist.GetYaxis().GetBinLowEdge(y)
              for y in xrange(1, hist.GetNbinsY() + 2)]

    # New bin edge arrays will need an extra four values
    x_new = [0.] * (len(x_bins) + 4)
    y_new = [0.] * (len(y_bins) + 4)

    # Calculate bin widths at the edges
    xw1 = x_bins[1] - x_bins[0]
    xw2 = x_bins[-1] - x_bins[-2]
    yw1 = y_bins[1] - y_bins[0]
    yw2 = y_bins[-1] - y_bins[-2]

    # Set the edges of the outer framing bins and the adjusted
    # edge of the real edge bins
    x_new[0] = x_bins[0] - 2 * xw1 * 0.02
    x_new[1] = x_bins[0] - 1 * xw1 * 0.02
    x_new[-1] = x_bins[-1] + 2 * xw2 * 0.02
    x_new[-2] = x_bins[-1] + 1 * xw2 * 0.02
    y_new[0] = y_bins[0] - 2 * yw1 * 0.02
    y_new[1] = y_bins[0] - 1 * yw1 * 0.02
    y_new[-1] = y_bins[-1] + 2 * yw2 * 0.02
    y_new[-2] = y_bins[-1] + 1 * yw2 * 0.02

    # Copy the remaining bin edges from the hist
    for i in xrange(0, len(x_bins)):
        x_new[i + 2] = x_bins[i]
    for i in xrange(0, len(y_bins)):
        y_new[i + 2] = y_bins[i]

    # print x_new
    # print y_new

    framed = ROOT.TH2D('%s framed' % hist.GetName(), '%s framed' % hist.GetTitle(), len(
        x_new) - 1, array('d', x_new), len(y_new) - 1, array('d', y_new))
    framed.SetDirectory(0)

    for x in xrange(1, framed.GetNbinsX() + 1):
        for y in xrange(1, framed.GetNbinsY() + 1):
            if x == 1 or x == framed.GetNbinsX() or y == 1 or y == framed.GetNbinsY():
        # This is a a frame bin
                framed.SetBinContent(x, y, frameValue)
            else:
                # adjust x and y if we're in the first frame so as to copy the output
                # values from the real TH2
                ux = x
                uy = y
                if x == 2:
                    ux += 1
                elif x == (len(x_new) - 2):
                    ux -= 1
                if y == 2:
                    uy += 1
                elif y == (len(y_new) - 2):
                    uy -= 1
                framed.SetBinContent(x, y, hist.GetBinContent(ux - 2, uy - 2))
    return framed


def contourFromTH2(h2in, threshold, minPoints=10, frameValue=1000.):
    # // http://root.cern.ch/root/html/tutorials/hist/ContourList.C.html
    contoursList = [threshold]
    contours = array('d', contoursList)
    # if (h2in.GetNbinsX() * h2in.GetNbinsY()) > 10000: minPoints = 50
    # if (h2in.GetNbinsX() * h2in.GetNbinsY()) <= 100: minPoints = 10

    h2 = frameTH2D(h2in, threshold, frameValue)

    h2.SetContour(1, contours)

    # Draw contours as filled regions, and Save points
    # backup = R.gPad # doesn't work in pyroot, backup behaves like a ref to gPad
    canv = ROOT.TCanvas('tmp', 'tmp')
    canv.cd()
    h2.Draw('CONT Z LIST')
    ROOT.gPad.Update()  # Needed to force the plotting and retrieve the contours in

    conts = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
    contLevel = None

    if conts is None or conts.GetSize() == 0:
        print '*** No Contours Were Extracted!'
        return None
    ret = ROOT.TList()
    for i in xrange(conts.GetSize()):
        contLevel = conts.At(i)
        print '>> Contour %d has %d Graphs' % (i, contLevel.GetSize())
        for j in xrange(contLevel.GetSize()):
            gr1 = contLevel.At(j)
            print'\t Graph %d has %d points' % (j, gr1.GetN())
            if gr1.GetN() > minPoints:
                ret.Add(gr1.Clone())
            # // break;
    # backup.cd()
    canv.SaveAs("contour.pdf")
    canv.Close()
    return ret

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=int, default='1', help="Which type of 2HDM?")

    args = parser.parse_args()

    style1=GetStyleHtt()
    style1.cd()

    binbeta=200#1000
    minbeta=0.5
    maxbeta=10.0
    minmass=15
    maxmass=60
    binmass=200
    if (args.model==4):
       minbeta=0.1
       maxbeta=6
    if (args.model==2):
       minbeta=0.3
    #   maxbeta=0.8

    def fitFunc(x,par0,par1,par2,par3):
       return par0 + par1*x + par2*x*x + par3*x*x*x

    def fitFunc2(x, par):
       return par[0] + par[1] * x[0] + par[2] * x[0] * x[0] + par[3] * x[0] * x[0] * x[0]

    theFit = ROOT.TF1("theFit",fitFunc2,15,60,4);

    x_mmmm, y_mmmm = np.loadtxt('bbttRun2.txt', unpack=True)
    gmmmm1 = ROOT.TGraph(len(x_mmmm), x_mmmm.flatten('C'),y_mmmm.flatten('C'))

    theFit.SetParameter(0, 0)
    theFit.SetParameter(1, 0)
    theFit.SetParameter(2, 0)
    theFit.SetParameter(3, 0)
    gmmmm1.Fit("theFit", "R0")
    param0=theFit.GetParameters()[0]
    param1=theFit.GetParameters()[1]
    param2=theFit.GetParameters()[2]
    param3=theFit.GetParameters()[3]
    xsm= np.linspace(0, 1,binmass+1)
    ysm= np.linspace(0, 1,binmass+1)
    nsm = binmass+1;
    hist=ROOT.TH2F("hist","hist",binmass,minmass,maxmass,binbeta,minbeta,maxbeta)
    for b in range(0,binbeta+1):
      tanbeta=0.0000001+minbeta+1.0*b*(maxbeta-minbeta)/(binbeta)
      for i in range(0,binmass+1):
         xxsm=0.0000001+minmass+1.0*i*(maxmass-minmass)/(binmass)
         xsm[i]=0.0000001+minmass+1.0*i*(maxmass-minmass)/(binmass)
         width=get_total_width(args.model,float(xxsm),tanbeta)
    	 BRtt=gamma_tau(tanbeta,float(xxsm),args.model)/width
  	 BRbb=gamma_quarks(tanbeta,float(xxsm),args.model,6)/width
         ysm[i]=(0.01*fitFunc(xxsm,param0,param1,param2,param3)/(2*BRtt*BRbb))
   	 hist.Fill(xxsm,1.0*tanbeta,ysm[i])


    #x_bbttRun21, y_bbttRun21 = np.loadtxt('bbttRun2.txt', unpack=True)
    #x_bbttRun2=array("d",x_bbttRun21)
    #y_bbttRun2=array("d",y_bbttRun21)
    #hist=ROOT.TH2F("hist","hist",len(x_bbttRun2)-1,x_bbttRun2[0],x_bbttRun2[len(x_bbttRun2)-1],binbeta,minbeta,maxbeta)
    #for b in range(0,binbeta+1):
    #    tanbeta=0.001+minbeta+1.0*b*(maxbeta-minbeta)/(binbeta)
    #    for i in range(0,len(x_bbttRun2)):
    #       width=get_total_width(args.model,float(x_bbttRun2[i]),tanbeta)
    #       BRtt=gamma_tau(tanbeta,float(x_bbttRun2[i]),args.model)/width
    #       BRbb=gamma_quarks(tanbeta,float(x_bbttRun2[i]),args.model,6)/width
    #       y=0.01*y_bbttRun2[i]/(2*BRtt*BRbb)
    #       hist.Fill(x_bbttRun2[i],1.0*tanbeta,y)

    canvas = MakeCanvas("asdf","asdf",800,800)
    canvas.SetRightMargin(0.23)#FIXME 0.2
    canvas.SetLeftMargin(0.12)
    canvas.cd()
    if (args.model>-2):
      canvas.SetLogz()
    hist.GetXaxis().SetTitle("m_{a} (GeV)")
    hist.GetYaxis().SetTitle("tan #beta")
    hist.GetZaxis().SetTitle("95% CL on #frac{#sigma(h)}{#sigma_{SM}} B(h#rightarrow aa)")
    hist.GetZaxis().SetNdivisions(505)
    hist.GetZaxis().SetTitleOffset(1.25)
    hist.GetYaxis().SetTitleOffset(0.92)
    #hist.GetXaxis().SetRangeUser(15,62)
    if (args.model==3):
       hist.GetZaxis().SetRangeUser(0.05,3)
    if (args.model==2):
       hist.GetZaxis().SetRangeUser(0.05,3)
    if (args.model==4):
       hist.GetZaxis().SetRangeUser(0.1,300)
    if (args.model==1):
       hist.GetZaxis().SetRangeUser(0.1,1.0)
    hist.Draw("colz")
    lumiBlurb1=add_CMS()
    lumiBlurb1.Draw("same")
    lumiBlurb=add_lumi()
    lumiBlurb.Draw("same")
    lumiBlurb3=add_Preliminary()
    lumiBlurb3.Draw("same")
    lumi=add_model(args.model)
    lumi.Draw("same")
    lumi2=add_br(args.model)
    lumi2.Draw("same")
    #canvas.SaveAs('plots/plot_BRaa_bbttRun2_Type'+str(args.model)+'.png')
    #canvas.SaveAs('plots/plot_BRaa_bbttRun2_Type'+str(args.model)+'.pdf')

    mycontour100=contourFromTH2(hist, 1)
    mycontour100[0].SetLineWidth(7)
    mycontour100[0].SetLineStyle(5)
    mycontour100[0].SetLineColor(0)
    mycontour100[0].Draw("l")


    mycontour24=contourFromTH2(hist, 0.24)
    mycontour24[0].SetLineWidth(7)
    mycontour24[0].SetLineStyle(3)
    mycontour24[0].SetLineColor(0)
    mycontour24[0].Draw("l")

    ROOT.gPad.RedrawAxis()

    legend=make_legend()
    legend.AddEntry(mycontour100[0],"95% CL on #frac{#sigma(h)}{#sigma_{SM}}B(h#rightarrow aa) = 1.00","l")
    legend.AddEntry(mycontour24[0],"95% CL on #frac{#sigma(h)}{#sigma_{SM}}B(h#rightarrow aa) = 0.24","l")
    legend.Draw("same")

    canvas.SaveAs('plots/plot_BRaa_bbttRun2_Type'+str(args.model)+'.png')
    canvas.SaveAs('plots/plot_BRaa_bbttRun2_Type'+str(args.model)+'.pdf')


