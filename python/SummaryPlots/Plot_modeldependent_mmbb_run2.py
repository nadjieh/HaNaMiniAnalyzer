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

tobekept = []
def contourFromTH2(h2in, threshold, minPoints=10, frameValue=1000. , canv = None):
    # // http://root.cern.ch/root/html/tutorials/hist/ContourList.C.html
    contoursList = [threshold]
    contours = array('d', contoursList)
    # if (h2in.GetNbinsX() * h2in.GetNbinsY()) > 10000: minPoints = 50
    # if (h2in.GetNbinsX() * h2in.GetNbinsY()) <= 100: minPoints = 10

    #h2 = h2in.Clone("%s_contours_%.2f" % (h2in.GetName() , threshold))
    h2 = h2in.Clone() #frameTH2D(h2in, threshold, frameValue)
    tobekept.append( h2 )
    h2.SetContour(1) #, contours)
    h2.SetContourLevel( 0 , threshold )
    # h2.SetContourLevel( 1 , threshold*2 )
    # Draw contours as filled regions, and Save points
    # backup = R.gPad # doesn't work in pyroot, backup behaves like a ref to gPad
    if not canv :
        canv = ROOT.TCanvas('tmp', 'tmp')
    canv.cd()
    h2.Draw('CONT Z LIST')
    canv.Update()  # Needed to force the plotting and retrieve the contours in
    canv.Update()
    #ROOT.gROOT.GetListOfSpecials().Print( "" , 3)
    conts = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
    contLevel = None
    #print conts
    if not conts or conts.GetSize() == 0:
        print '*** No Contours Were Extracted!'
        return None
    h2.Draw('CONT Z LIST')
    canv.Update()  # Needed to force the plotting and retrieve the contours in
    #ROOT.gROOT.GetListOfSpecials().Print( "" , 3)
    conts = ROOT.gROOT.GetListOfSpecials().FindObject('contours')
    #conts.Print("" , 2)
    ret = ROOT.TList()
    for i in xrange(conts.GetSize()):
        contLevel = conts.At(i)
        #print '>> Contour %d has %d Graphs' % (i, contLevel.GetSize())
        for j in xrange(contLevel.GetSize()):
            gr1 = contLevel.At(j)
            #print'\t Graph %d has %d points' % (j, gr1.GetN())
            if gr1.GetN() > minPoints:
                ret.Add(gr1.Clone())
            # // break;
    # backup.cd()
    # canv.SaveAs("contour_%.2f.pdf" % threshold)
    if not canv :
        canv.Close()
    return ret

from MuMu_bb import LimitReader

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=int, default='1', help="Which type of 2HDM?")

    args = parser.parse_args()

    style1=GetStyleHtt()
    style1.cd()


    
    tanbetas = np.linspace( 0.01 , 10.01 , 100 , endpoint=False )
    tanbetas = tanbetas[2:]
    masses = np.linspace( 20 , 62.5 , 17 , endpoint=False )
    binbeta = len( tanbetas )
    minbeta = tanbetas[0]
    maxbeta = tanbetas[-1]
    binmass = len( masses )
    minmass = masses[0]
    maxmass = masses[-1]
    
    # binbeta=200#1000
    # minbeta=0.5
    # maxbeta=10.0
    # minmass=20
    # maxmass=60
    # binmass=200
    # if (args.model==4):
    #    minbeta=0.1
    #    maxbeta=6
    # if (args.model==2):
    #    minbeta=0.3
    # #   maxbeta=0.8

    limits = LimitReader( "../../macro/combine/Feb2018/bTagSR2016Systs/myLimitXsec.root" )
    ROOT.gROOT.cd()
    
    histLimit=ROOT.TH2F("histLimit","Limit",binmass,minmass,maxmass,binbeta,minbeta,maxbeta)
    histBRbb=ROOT.TH2F("histBRbb","BRbb",binmass,minmass,maxmass,binbeta,minbeta,maxbeta)
    histBRmm=ROOT.TH2F("histBRmm","BRmm",binmass,minmass,maxmass,binbeta,minbeta,maxbeta)
    histBRmmbb=ROOT.TH2F("histBRmmbb","BRmmbb",binmass,minmass,maxmass,binbeta,minbeta,maxbeta)
    histWidth=ROOT.TH2F("histWidth","Width",binmass,minmass,maxmass,binbeta,minbeta,maxbeta)
    histLimitOriginal=ROOT.TH2F("histLimitOriginal","Origianl Limit",binmass,minmass,maxmass,binbeta,minbeta,maxbeta)
    for i in range(1,binmass+1):
        xxsm= histLimitOriginal.GetXaxis().GetBinCenter(i) #0.0000001+minmass+1.0*i*(maxmass-minmass)/(binmass)
        mass = masses[i-1]
        for b in range(1,binbeta+1):
            tanbeta= tanbetas[b-1] #histLimitOriginal.GetYaxis().GetBinLowEdge( b )
            ysm , limit , width , BRmm , BRbb = limits.GetModelLimit( args.model , xxsm , tanbeta )

            # dirName = "/home/hbakhshi/Desktop/Hamb13/HaNaMiniAnalyzer/macro/combine/Feb2018/bTagSR2016Systs_MMTTIncluded/model%d/tanbeta%d" % (args.model , tanbeta*100)
            # if int(mass)-mass == 0 :
            #     fName = dirName + "/higgsCombineTest.Asymptotic.mH%d.root" % int(mass)
            # else:
            #     fName = dirName + "/higgsCombineTest.Asymptotic.mH%.1f.root" % mass

            # #print fName
            # if os.path.isfile( fName ):
            #     ysm =  limits.ExtractLimit( fName )
            # else :
            #     print fName , "is not found"
            #     ysm = 0.000001

            binindex = histLimit.GetBin( i , b ) #xxsm , tanbeta )
   	    histLimit.SetBinContent(binindex,ysm)
            histBRmmbb.SetBinContent( binindex,BRmm*BRbb)
            histBRmm.SetBinContent( binindex,BRmm*width)
            histBRbb.SetBinContent( binindex,BRbb*width)
            histWidth.SetBinContent( binindex,width*width)
            histLimitOriginal.SetBinContent( binindex,limit)

    canvas = MakeCanvas("asdf","asdf",800,800)
    canvas.SetRightMargin(0.23)#FIXME 0.2
    canvas.SetLeftMargin(0.12)
    canvas.cd()
    if (args.model>-2):
      canvas.SetLogz()
      histLimit.SetAxisRange( 0.0001 , 1000 , "Z" )
    histLimit.GetXaxis().SetTitle("m_{a} (GeV)")
    histLimit.GetYaxis().SetTitle("tan #beta")
    histLimit.GetZaxis().SetTitle("95% CL on #frac{#sigma(h)}{#sigma_{SM}} B(h#rightarrow aa)")
    histLimit.GetZaxis().SetNdivisions(505)
    histLimit.GetZaxis().SetTitleOffset(1.25)
    histLimit.GetYaxis().SetTitleOffset(0.92)
    #histLimit.GetXaxis().SetRangeUser(15,62)
    # if (args.model==3):
    #    histLimit.GetZaxis().SetRangeUser(0.05,3)
    # if (args.model==2):
    #    histLimit.GetZaxis().SetRangeUser(0.05,3)
    # if (args.model==4):
    #    histLimit.GetZaxis().SetRangeUser(0.1,300)
    # if (args.model==1):
    #     #histLimit.GetZaxis().SetRangeUser(0.1,1.0) 1.7*0.0001*
    #     histLimit.GetZaxis().SetRangeUser(0.00001 , 1.0 ) #0.00008/(1.7*0.0001),0.0002/(1.7*0.0001))
    histLimit.Draw("colz")
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

    legend=make_legend()
    cTmp1 = ROOT.TCanvas("cTmp1" , "cTmp1")
    mycontour100=contourFromTH2(histLimit, 1.0 , canv = cTmp1)
    canvas.cd()
    #mycontour100.Print()
    if mycontour100 and mycontour100.GetSize() > 0 :
        for contour in mycontour100 :
            contour.SetLineWidth(7)
            contour.SetLineStyle(5)
            contour.SetLineColor(0)
            contour.Draw("l")
            print "contour %.2f plotted" % 1.0
        legend.AddEntry(mycontour100[0],"95% CL on #frac{#sigma(h)}{#sigma_{SM}}B(h#rightarrow aa) = 1.00","l")

    cTmp2 = ROOT.TCanvas("cTmp2" , "cTmp2")
    mycontour24=contourFromTH2(histLimit, 0.44 , canv = cTmp2)
    canvas.cd()
    print mycontour24.GetSize(), mycontour100.GetSize()
    if mycontour24 and mycontour24.GetSize() > 0 :
        for contour in mycontour24 :
            contour.SetLineWidth(7)
            contour.SetLineStyle(3)
            contour.SetLineColor(ROOT.kBlue)
            contour.Draw("l")
            print "contour %.2f plotted" % 0.34
        legend.AddEntry(mycontour24[0],"95% CL on #frac{#sigma(h)}{#sigma_{SM}}B(h#rightarrow aa) = 0.34","l")

    #canvas.RedrawAxis()
    legend.Draw() #"same")

    canvas.SaveAs('plots/plot_BRaa_bbttRun2_Type'+str(args.model)+'.png')
    canvas.SaveAs('plots/plot_BRaa_bbttRun2_Type'+str(args.model)+'.pdf')

    fout = ROOT.TFile.Open('plots/plot_BRaa_bbttRun2_Type'+str(args.model)+'.root' , "recreate")
    canvas.Write()
    cTmp2.Write()
    cTmp1.Write()
    histLimit.Write()
    histBRmmbb.Write()
    histBRmm.Write()
    histBRbb.Write()
    histWidth.Write()
    histLimitOriginal.Write()
    legend.Write()
    fout.Close()


