import argparse as argparse
#from RecoLuminosity.LumiDB import argparse
import math
import os
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas
import ROOT
import numpy as np
from MuMu_bb import *
from array import array
from BR import get_total_width
from BR import gamma_quarks
from BR import gamma_mu
from BR import gamma_tau
from BR import gamma_photon
from BR import gamma_gg


def add_lumi():
    lowX=0.355
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.04)
    lumi.AddText("19.7 fb^{-1} (8 TeV) or 35.9 fb^{-1} (13 TeV)")
    return lumi

def add_CMS():
    lowX=0.21
    lowY=0.75
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.07)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS")
    return lumi 

def add_Preliminary():
    lowX=0.21
    lowY=0.70
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.03)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(52)
    #lumi.AddText("Supplementary")
    lumi.AddText("Preliminary")
    return lumi 

def make_legend():
    #output = ROOT.TLegend(0.10, 0.25, 0.94, 0.85, "", "brNDC")
    output = ROOT.TLegend(0.5, 0.20, 0.90, 0.52, "", "brNDC")
    output.SetLineWidth(0)
    output.SetLineStyle(0)
    output.SetFillColor(0)
    output.SetBorderSize(0)
    output.SetTextFont(62)
    return output

def make_legend2():
    #output = ROOT.TLegend(0.10, 0.165, 0.94, 0.23, "", "brNDC")
    output = ROOT.TLegend(0.53, 0.165, 0.85, 0.20, "", "brNDC")
    output.SetLineWidth(0)
    output.SetNColumns(2)
    output.SetLineStyle(0)
    output.SetFillColor(0)
    output.SetBorderSize(0)
    output.SetTextFont(62)
    return output

def add_model(model,tanbeta):
    lowX=0.21
    lowY=0.15
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.04)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(62)
    if str(model)=="1":
       lumi.AddText("2HDM+S type I")
    if str(model)=="2":
       lumi.AddText("2HDM+S type II")
    if str(model)=="3":
       lumi.AddText("2HDM+S type III")
    if str(model)=="4":
       lumi.AddText("2HDM+S type IV")
    if str(model)!="1":
	lumi.AddText("tan#beta = "+str(tanbeta))
    return lumi

def add_arxiv(channel,ma):
    lowX=0.21
    lowY=0.08
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.03)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(12)
    lumi.AddText("arXiv:1312.4992")
    return lumi


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=int, default='1', help="Which type of 2HDM?")
    parser.add_argument('--tanbeta', type=float, default='1', help="Which tan beta?")

    args = parser.parse_args()

    style1=GetStyleHtt()
    style1.cd()

    #### h->aa->mmtt ####
    x_mmtt1, y_mmtt1 = np.loadtxt('mmtt_obs.txt', unpack=True)
    print x_mmtt1
    x_mmtt=array("d",x_mmtt1)
    y_mmtt=array("d",y_mmtt1)
    for i in range(0,len(x_mmtt)):
        width=get_total_width(args.model,float(x_mmtt[i]),args.tanbeta)
        BRtt=gamma_tau(args.tanbeta,float(x_mmtt[i]),args.model)/width
        y_mmtt[i]=y_mmtt[i]/(BRtt*BRtt)
	#print x_mmtt[i],y_mmtt[i]
    gmmtt = ROOT.TGraph(len(x_mmtt), x_mmtt,y_mmtt)

    x_mmtt1_e, y_mmtt1_e = np.loadtxt('mmtt_exp.txt', unpack=True)
    x_mmtt_e=array("d",x_mmtt1_e)
    y_mmtt_e=array("d",y_mmtt1_e)
    for i in range(0,len(x_mmtt_e)):
        width=get_total_width(args.model,float(x_mmtt_e[i]),args.tanbeta)
        BRtt=gamma_tau(args.tanbeta,float(x_mmtt_e[i]),args.model)/width
        y_mmtt_e[i]=y_mmtt_e[i]/(BRtt*BRtt)
    gmmtt_e = ROOT.TGraph(len(x_mmtt_e), x_mmtt_e,y_mmtt_e)

    #### h->aa->mmtt Run-2####
    x_mmtt1R2, y_mmtt1R2 = np.loadtxt('mmttRun2.txt', unpack=True)
    x_mmttR2=array("d",x_mmtt1R2)
    y_mmttR2=array("d",y_mmtt1R2)
    for i in range(0,len(x_mmttR2)):
        width=get_total_width(args.model,float(x_mmttR2[i]),args.tanbeta)
        BRtt=gamma_tau(args.tanbeta,float(x_mmttR2[i]),args.model)/width
	BRmm=gamma_mu(args.tanbeta,float(x_mmttR2[i]),args.model)/width
        y_mmttR2[i]=0.001*y_mmttR2[i]/(2*BRmm*BRtt)
    gmmttR2 = ROOT.TGraph(len(x_mmttR2), x_mmttR2,y_mmttR2)

    x_mmtt1R2_e, y_mmtt1R2_e = np.loadtxt('mmttRun2_exp.txt', unpack=True)
    x_mmttR2_e=array("d",x_mmtt1R2_e)
    y_mmttR2_e=array("d",y_mmtt1R2_e)
    for i in range(0,len(x_mmttR2_e)):
        width=get_total_width(args.model,float(x_mmttR2_e[i]),args.tanbeta)
        BRtt=gamma_tau(args.tanbeta,float(x_mmttR2_e[i]),args.model)/width
        BRmm=gamma_mu(args.tanbeta,float(x_mmttR2_e[i]),args.model)/width
        y_mmttR2_e[i]=0.001*y_mmttR2_e[i]/(2*BRmm*BRtt)
    gmmttR2_e = ROOT.TGraph(len(x_mmttR2_e), x_mmttR2_e,y_mmttR2_e)

    #### h->aa->mmbb ####
    x_mmbb, y_mmbb = np.loadtxt('mmbb_obs.txt', unpack=True)
    for i in range(0,len(x_mmbb)):
        width=get_total_width(args.model,float(x_mmbb[i]),args.tanbeta)
        BRmm=gamma_mu(args.tanbeta,float(x_mmbb[i]),args.model)/width
        BRbb=gamma_quarks(args.tanbeta,float(x_mmbb[i]),args.model,6)/width
	y_mmbb[i]=y_mmbb[i]*0.00017
        y_mmbb[i]=y_mmbb[i]/(2*BRmm*BRbb)
	#print x_mmbb[i],y_mmbb[i]
    gmmbb = ROOT.TGraph(len(x_mmbb), x_mmbb.flatten('C'),y_mmbb.flatten('C'))

    x_mmbb_e, y_mmbb_e = np.loadtxt('mmbb_exp.txt', unpack=True)
    for i in range(0,len(x_mmbb_e)):
        width=get_total_width(args.model,float(x_mmbb_e[i]),args.tanbeta)
        BRmm=gamma_mu(args.tanbeta,float(x_mmbb_e[i]),args.model)/width
        BRbb=gamma_quarks(args.tanbeta,float(x_mmbb_e[i]),args.model,6)/width
        y_mmbb_e[i]=y_mmbb_e[i]*0.00017
        y_mmbb_e[i]=y_mmbb_e[i]/(2*BRmm*BRbb)
    gmmbb_e = ROOT.TGraph(len(x_mmbb_e), x_mmbb_e.flatten('C'),y_mmbb_e.flatten('C'))

    #### h->aa->bbtt ####
    x_bbtt, y_bbtt = np.loadtxt('bbtt_obs.txt', unpack=True)
    for i in range(0,len(x_bbtt)):
        width=get_total_width(args.model,float(x_bbtt[i]),args.tanbeta)
        BRtt=gamma_tau(args.tanbeta,float(x_bbtt[i]),args.model)/width
        BRbb=gamma_quarks(args.tanbeta,float(x_bbtt[i]),args.model,6)/width
        y_bbtt[i]=(0.01*y_bbtt[i])/(2*BRtt*BRbb)
    gbbtt = ROOT.TGraph(len(x_bbtt), x_bbtt.flatten('C'),y_bbtt.flatten('C'))

    x_bbtt_e, y_bbtt_e = np.loadtxt('bbtt_exp.txt', unpack=True)
    for i in range(0,len(x_bbtt_e)):
        width=get_total_width(args.model,float(x_bbtt_e[i]),args.tanbeta)
        BRtt=gamma_tau(args.tanbeta,float(x_bbtt_e[i]),args.model)/width
        BRbb=gamma_quarks(args.tanbeta,float(x_bbtt_e[i]),args.model,6)/width
        y_bbtt_e[i]=(0.01*y_bbtt_e[i])/(2*BRtt*BRbb)
    gbbtt_e = ROOT.TGraph(len(x_bbtt_e), x_bbtt_e.flatten('C'),y_bbtt_e.flatten('C'))


    #### h->aa->tttt (HIG-14-019) ####
    x_tttt1, y_tttt1 = np.loadtxt('tttt1_obs.txt', unpack=True)
    for i in range(0,len(x_tttt1)):
        width=get_total_width(args.model,float(x_tttt1[i]),args.tanbeta)
        BRtt=gamma_tau(args.tanbeta,float(x_tttt1[i]),args.model)/width
        y_tttt1[i]=y_tttt1[i]/(19.3*BRtt*BRtt)
    gtttt1 = ROOT.TGraph(len(x_tttt1), x_tttt1.flatten('C'),y_tttt1.flatten('C'))

    x_tttt1_e, y_tttt1_e = np.loadtxt('tttt1_exp.txt', unpack=True)
    for i in range(0,len(x_tttt1_e)):
        width=get_total_width(args.model,float(x_tttt1_e[i]),args.tanbeta)
        BRtt=gamma_tau(args.tanbeta,float(x_tttt1_e[i]),args.model)/width
        y_tttt1_e[i]=y_tttt1_e[i]/(19.3*BRtt*BRtt)
    gtttt1_e = ROOT.TGraph(len(x_tttt1_e), x_tttt1_e.flatten('C'),y_tttt1_e.flatten('C'))

    #### h->aa->tttt (HIG-14-022) ####
    x_tttt2, y_tttt2 = np.loadtxt('tttt2_obs.txt', unpack=True)
    for i in range(0,len(x_tttt2)):
        width=get_total_width(args.model,float(x_tttt2[i]),args.tanbeta)
        BRtt=gamma_tau(args.tanbeta,float(x_tttt2[i]),args.model)/width
        y_tttt2[i]=y_tttt2[i]/(BRtt*BRtt)
	print x_tttt2[i],y_tttt2[i]
    gtttt2 = ROOT.TGraph(len(x_tttt2), x_tttt2.flatten('C'),y_tttt2.flatten('C'))

    x_tttt2_e, y_tttt2_e = np.loadtxt('tttt2_exp.txt', unpack=True)
    for i in range(0,len(x_tttt2_e)):
        width=get_total_width(args.model,float(x_tttt2_e[i]),args.tanbeta)
        BRtt=gamma_tau(args.tanbeta,float(x_tttt2_e[i]),args.model)/width
        y_tttt2_e[i]=y_tttt2_e[i]/(BRtt*BRtt)
    gtttt2_e = ROOT.TGraph(len(x_tttt2_e), x_tttt2_e.flatten('C'),y_tttt2_e.flatten('C'))

    #### h->aa->mmmm ####
    x_mmmm, y_mmmm = np.loadtxt('mmmm_obs.txt', unpack=True)
    #for i in range(0,len(x_mmmm)):
    #    width=get_total_width(args.model,float(x_mmmm[i]),args.tanbeta)
    #    BRmm=gamma_mu(args.tanbeta,float(x_mmmm[i]),args.model)/width
    #    y_mmmm[i]=y_mmmm[i]/(19300*BRmm*BRmm)
    #gmmmm = ROOT.TGraph(len(x_mmmm), x_mmmm.flatten('C'),y_mmmm.flatten('C'))

    x_mmmm_e, y_mmmm_e = np.loadtxt('mmmm_exp.txt', unpack=True)

    def fitFunc(x,par0,par1,par2,par3):
       return par0 + par1*x + par2*x*x + par3*x*x*x 

    def fitFunc2(x, par):
       return par[0] + par[1] * x[0] + par[2] * x[0] * x[0] + par[3] * x[0] * x[0] * x[0]

    theFit = ROOT.TF1("theFit",fitFunc2,0.25,3.55,4);
    for i in range(0,len(x_mmmm)):
        y_mmmm[i]=y_mmmm[i]/(19300)
    gmmmm1 = ROOT.TGraph(len(x_mmmm), x_mmmm.flatten('C'),y_mmmm.flatten('C'))

    for i in range(0,len(x_mmmm_e)):
        y_mmmm_e[i]=y_mmmm_e[i]/(19300)
    gmmmm1_e = ROOT.TGraph(len(x_mmmm_e), x_mmmm_e.flatten('C'),y_mmmm_e.flatten('C'))

    theFit.SetParameter(0, 0)
    theFit.SetParameter(1, 0)
    theFit.SetParameter(2, 0)
    theFit.SetParameter(3, 0)
    gmmmm1.Fit("theFit", "R0")
    param0=theFit.GetParameters()[0]
    param1=theFit.GetParameters()[1]
    param2=theFit.GetParameters()[2]
    param3=theFit.GetParameters()[3]
    xsm= np.linspace(0, 1,500)
    ysm= np.linspace(0, 1,500)
    nsm = 500;
    for i in range(0,nsm):
      xxsm=(0.25+i*(3.55-0.25)/499)
      xsm[i]=(0.25+i*(3.55-0.25)/499);
      width=get_total_width(args.model,float(xxsm),args.tanbeta)
      BRmm=gamma_mu(args.tanbeta,float(xxsm),args.model)/width
      ysm[i]=(fitFunc(xxsm,param0,param1,param2,param3)/(BRmm*BRmm))
    gmmmm = ROOT.TGraph(nsm,xsm,ysm)

    gmmmm1_e.Fit("theFit", "R0")
    param0=theFit.GetParameters()[0]
    param1=theFit.GetParameters()[1]
    param2=theFit.GetParameters()[2]
    param3=theFit.GetParameters()[3]
    xsm_e= np.linspace(0,1,500)
    ysm_e= np.linspace(0,1,500)
    nsm_e = 500;
    for i in range(0,nsm_e):
      xxsm_e=(1+i*(3.55-1)/499)
      xsm_e[i]=(1+i*(3.55-1)/499);
      width=get_total_width(args.model,float(xxsm_e),args.tanbeta)
      BRmm=gamma_mu(args.tanbeta,float(xxsm_e),args.model)/width
      ysm_e[i]=(fitFunc(xxsm_e,param0,param1,param2,param3)/(BRmm*BRmm))
    gmmmm_e = ROOT.TGraph(nsm_e,xsm_e,ysm_e)

    #### Dummy histogram for plotting purposes ####
    x, y = np.loadtxt('dummy.txt', unpack=True)
    gx = ROOT.TGraph(len(x), x.flatten('C'),y.flatten('C'))

    #### Shaded areas above curves ####
    ymax=100000000000000000
    gmmtt_shade = ROOT.TGraph(len(x_mmtt))
    for i in range(0,len(x_mmtt)):
      gmmtt_shade.SetPoint(i,x_mmtt[i],ymax)
      gmmtt_shade.SetPoint(len(x_mmtt)+i,x_mmtt[len(x_mmtt)-i-1],y_mmtt[len(x_mmtt)-i-1])
    gmmtt_shade.SetFillStyle(3001)
    adapt1=ROOT.gROOT.GetColor(ROOT.kPink+7)
    trans1, new_idx1=newColor(adapt1.GetRed(), adapt1.GetGreen(),adapt1.GetBlue() )
    gmmtt_shade.SetFillColor(new_idx1)

    gmmttR2_shade = ROOT.TGraph(len(x_mmttR2))
    for i in range(0,len(x_mmttR2)):
      gmmttR2_shade.SetPoint(i,x_mmttR2[i],ymax)
      gmmttR2_shade.SetPoint(len(x_mmttR2)+i,x_mmttR2[len(x_mmttR2)-i-1],y_mmttR2[len(x_mmttR2)-i-1])
    gmmttR2_shade.SetFillStyle(3001)
    adapt7=ROOT.gROOT.GetColor(ROOT.kCyan)
    trans7, new_idx7=newColor( adapt7.GetRed(), adapt7.GetGreen(),adapt7.GetBlue() )
    gmmttR2_shade.SetFillColor(new_idx7)

    gmmbb_shade = ROOT.TGraph(len(x_mmbb))
    for i in range(0,len(x_mmbb)):
      gmmbb_shade.SetPoint(i,x_mmbb[i],ymax)
      gmmbb_shade.SetPoint(len(x_mmbb)+i,x_mmbb[len(x_mmbb)-i-1],y_mmbb[len(x_mmbb)-i-1])
    gmmbb_shade.SetFillStyle(3001)
    adapt2=ROOT.gROOT.GetColor(ROOT.kGreen-3)
    trans2 , new_idx2 =newColor( adapt2.GetRed(), adapt2.GetGreen(),adapt2.GetBlue())
    gmmbb_shade.SetFillColor(new_idx2)

    gbbtt_shade = ROOT.TGraph(len(x_bbtt))
    for i in range(0,len(x_bbtt)):
      gbbtt_shade.SetPoint(i,x_bbtt[i],ymax)
      gbbtt_shade.SetPoint(len(x_bbtt)+i,x_bbtt[len(x_bbtt)-i-1],y_bbtt[len(x_bbtt)-i-1])
    gbbtt_shade.SetFillStyle(3001)
    adapt22=ROOT.gROOT.GetColor(ROOT.kRed+3)
    trans22 , new_idx22 = newColor( adapt22.GetRed(), adapt22.GetGreen(),adapt22.GetBlue() )
    gbbtt_shade.SetFillColor(new_idx22)


    gtttt1_shade = ROOT.TGraph(len(x_tttt1))
    for i in range(0,len(x_tttt1)):
      gtttt1_shade.SetPoint(i,x_tttt1[i],ymax)
      gtttt1_shade.SetPoint(len(x_tttt1)+i,x_tttt1[len(x_tttt1)-i-1],y_tttt1[len(x_tttt1)-i-1])
    gtttt1_shade.SetFillStyle(3001)
    adapt3=ROOT.gROOT.GetColor(ROOT.kBlue-3)
    trans3 , new_idx3=newColor( adapt3.GetRed(), adapt3.GetGreen(),adapt3.GetBlue() )
    gtttt1_shade.SetFillColor(new_idx3)

    gtttt2_shade = ROOT.TGraph(len(x_tttt2))
    for i in range(0,len(x_tttt2)):
      gtttt2_shade.SetPoint(i,x_tttt2[i],ymax)
      gtttt2_shade.SetPoint(len(x_tttt2)+i,x_tttt2[len(x_tttt2)-i-1],y_tttt2[len(x_tttt2)-i-1])
    gtttt2_shade.SetFillStyle(3001)
    adapt4=ROOT.gROOT.GetColor(ROOT.kOrange-3)
    trans4 , new_idx4 =newColor( adapt4.GetRed(), adapt4.GetGreen(),adapt4.GetBlue())
    gtttt2_shade.SetFillColor(ROOT.kOrange-3)

    gmmmm_shade = ROOT.TGraph(len(xsm))
    for i in range(0,len(xsm)):
      gmmmm_shade.SetPoint(i,xsm[i],ymax)
      gmmmm_shade.SetPoint(len(xsm)+i,xsm[len(xsm)-i-1],ysm[len(xsm)-i-1])
    gmmmm_shade.SetFillStyle(3001)
    adapt5=ROOT.gROOT.GetColor(ROOT.kViolet-3)
    trans5 , new_idx5=newColor( adapt5.GetRed(), adapt5.GetGreen(),adapt5.GetBlue() )
    gmmmm_shade.SetFillColor(ROOT.kViolet-3)

    #### Vertical shaded areas for not valid computations ####
    shade1=ROOT.TGraph(2)
    shade1.SetPoint(0,3,ymax)
    shade1.SetPoint(2,5.2,0.00000000001)
    shade1.SetPoint(1,5.2,ymax)
    shade1.SetPoint(3,3,0.000000000001)
    shade1.SetFillColor(ROOT.kWhite)
    shade1_2=shade1.Clone()
    shade1_2.SetFillStyle(3005)
    shade1_2.SetFillColor(ROOT.kGray+1)
    shade1_2.SetLineColor(ROOT.kWhite)

    shade2=ROOT.TGraph(2)
    shade2.SetPoint(0,9.4,ymax)
    shade2.SetPoint(2,11.6,0.0000000000001)
    shade2.SetPoint(1,11.6,ymax)
    shade2.SetPoint(3,9.4,0.000000000001)
    shade2.SetFillColor(ROOT.kWhite)
    shade2_2=shade2.Clone()
    shade2_2.SetFillStyle(3005)
    shade2_2.SetFillColor(ROOT.kGray+1)

    shade3=ROOT.TGraph(2)
    shade3.SetPoint(0,0.25,ymax)
    shade3.SetPoint(2,1,0.0000000000001)
    shade3.SetPoint(1,1,ymax)
    shade3.SetPoint(3,0.25,0.000000000001)
    shade3.SetFillColor(ROOT.kWhite)
    shade3_2=shade3.Clone()
    shade3_2.SetFillStyle(3005)
    shade3_2.SetFillColor(ROOT.kGray+1)

    adapt1=ROOT.gROOT.GetColor(ROOT.kPink+7)

    #### Plotting ####
    canvas = MakeCanvas("asdf","asdf",800,800)
    canvas.cd()
    canvas.SetLogy()
    canvas.SetLogx()
    gx.Draw("AC")
    gx.GetXaxis().SetRangeUser(0.94,67)
    gx.GetXaxis().SetLimits(0.94,67)

    gx.SetMaximum(1000)
    gx.SetMinimum(0.0000001)
    if args.model<3:
       gx.SetMinimum(0.0001)
    
    gx.GetXaxis().SetTitle("m_{a} (GeV)");
    gx.GetYaxis().SetTitle("95% CL on #frac{#sigma_{h}}{#sigma_{SM}}B(h#rightarrow aa)")
    gx.Draw("AC")
    canvas.Update();
    gmmtt.SetLineWidth(1)
    gmmttR2.SetLineWidth(1)
    gmmbb.SetLineWidth(1)
    gbbtt.SetLineWidth(1)
    gmmtt.SetLineColor(ROOT.kPink+7)
    gmmttR2.SetLineColor(ROOT.kCyan)
    gmmbb.SetLineColor(ROOT.kGreen-3)
    gbbtt.SetLineColor(ROOT.kRed+3)
    gmmtt_e.SetLineColor(ROOT.kPink+7)
    gmmtt_shade.SetLineColor(ROOT.kPink+7)
    gmmttR2_e.SetLineColor(ROOT.kCyan)
    gmmttR2_shade.SetLineColor(ROOT.kCyan)
    gmmbb_e.SetLineColor(ROOT.kGreen-3)
    gbbtt_e.SetLineColor(ROOT.kRed+3)
    gmmtt_e.SetFillColor(ROOT.kPink+7)
    gmmttR2_e.SetFillColor(ROOT.kCyan)
    gmmbb_e.SetFillColor(ROOT.kGreen-3)
    gmmbb_shade.SetLineColor(ROOT.kGreen-3)
    gbbtt_e.SetFillColor(ROOT.kRed+3)
    gbbtt_shade.SetLineColor(ROOT.kRed+3)
    gmmtt_e.SetFillStyle(3004)
    gmmttR2_e.SetFillStyle(3004)
    gmmbb_e.SetFillStyle(3004)
    gbbtt_e.SetFillStyle(3004)
    gmmtt_shade.SetLineWidth(1)
    gmmttR2_shade.SetLineWidth(1)
    gmmbb_shade.SetLineWidth(1)
    gmmttR2_shade.Draw("fsame")
    gmmtt_shade.Draw("fsame")
    gbbtt_shade.Draw("fsame")
    gmmbb_shade.Draw("fsame")
    #gmmbb_e.Draw("lsame")
    gmmbb.Draw("lsame")
    gbbtt_shade.SetLineWidth(1)
    #gbbtt_e.Draw("lsame")
    gbbtt.Draw("lsame")
    #gmmtt_e.Draw("lsame")
    gmmtt.Draw("lsame")
    #gmmttR2_e.Draw("lsame")
    gmmttR2.Draw("lsame")
    gbbtt.Draw("lsame")
    #gmmtt_e.Draw("lsame")
    gmmtt.Draw("lsame")
    #gbbtt_e.Draw("lsame")
    #gmmbb_e.Draw("lsame")
    gmmbb.Draw("lsame")

    limitsMMBB2016 = LimitReader( "../../macro/combine/Feb2018/bTagSR2016Systs/myLimitXsec.root" , ROOT.kAzure-7 )
    gMMBB2016_shade = limitsMMBB2016.ProduceGraphTanbBeta( args.model,args.tanbeta, ymax = ymax )
    gMMBB2016 = limitsMMBB2016.ProduceGraphTanbBeta( args.model,args.tanbeta  )
    gMMBB2016_shade.Draw("fsame")
    gMMBB2016.Draw("lsame")
    
    gtttt1.SetLineColor(ROOT.kBlue-3)
    gtttt1_e.SetLineColor(ROOT.kBlue-3)
    gtttt1_shade.SetLineColor(ROOT.kBlue-3)
    gtttt1_e.SetFillColor(ROOT.kBlue-3)
    #gtttt1_e.SetLineWidth(602)
    gtttt1_e.SetFillStyle(3004)
    gtttt1_shade.SetLineWidth(1)
    gtttt1.SetLineWidth(1)
    gtttt2_shade.SetLineWidth(1)
    gtttt2.SetLineWidth(1)
    gmmmm_shade.SetLineWidth(1)
    gmmmm.SetLineWidth(1)
    gtttt1_shade.Draw("fsame")
    #gtttt1_e.Draw("lsame")
    gtttt1.Draw("lsame")
    gtttt2.SetLineColor(ROOT.kOrange-3)
    gtttt2_shade.SetLineColor(ROOT.kOrange-3)
    gtttt2_e.SetLineColor(ROOT.kOrange-3)
    gtttt2_e.SetFillColor(ROOT.kOrange-3)
    gtttt2_e.SetFillStyle(3004)
    gtttt2_shade.Draw("fsame")
    #gtttt2_e.Draw("lsame")
    gtttt2.Draw("lsame")
    gmmmm.SetLineColor(ROOT.kViolet-3)
    gmmmm_shade.SetLineColor(ROOT.kViolet-3)
    gmmmm_shade.Draw("fsame")
    gmmmm.Draw("lsame")
    shade1.Draw("fsame")
    shade2.Draw("fsame")
    shade3.Draw("fsame")
    shade1_2.Draw("fsame")
    shade2_2.Draw("fsame")
    shade3_2.Draw("fsame")
    line = ROOT.TLine(1,1,62.5,1)
    line.SetLineStyle(2)
    line.SetLineColor(ROOT.kRed)
    line.Draw("lsame")
    ROOT.gPad.RedrawAxis()
    canvas.Update()
    shade1.SetLineColor(ROOT.kGray)

    legend=make_legend()
    #legend.SetHeader("#it{h(125)#rightarrowaa searches}")
    #legend.AddEntry(shade1_2,"No prediction for B(a#rightarrow XX)","f")
    #legend.AddEntry(gmmmm_shade,"h#rightarrowaa#rightarrow#mu#mu#mu#mu (PLB 752 (2016) 146)","fl")
    #legend.AddEntry(gtttt1_shade,"h#rightarrowaa#rightarrow#tau#tau#tau#tau (JHEP 01 (2016) 079)","fl")
    legend.AddEntry(gmmmm_shade,"h#rightarrowaa#rightarrow#mu#mu#mu#mu (8 TeV)","fl")
    legend.AddEntry(gtttt1_shade,"h#rightarrowaa#rightarrow#tau#tau#tau#tau (8 TeV)","fl")
    legend.AddEntry(gtttt2_shade,"h#rightarrowaa#rightarrow#tau#tau#tau#tau (8 TeV)","fl")
    legend.AddEntry(gmmbb_shade,"h#rightarrowaa#rightarrow#mu#mubb (8 TeV)","fl")
    legend.AddEntry(gmmtt_shade,"h#rightarrowaa#rightarrow#mu#mu#tau#tau (8 TeV)","fl")
    legend.AddEntry(gmmttR2_shade,"h#rightarrowaa#rightarrow#mu#mu#tau#tau (13 TeV)","fl")
    legend.AddEntry(gbbtt_shade,"h#rightarrowaa#rightarrow#tau#taubb (13 TeV)","fl")
    legend.AddEntry(gMMBB2016_shade,"h#rightarrowaa#rightarrow#mu#mubb (13 TeV)","fl")
    legend.Draw("same")

    go=gmmtt_shade.Clone()
    go.SetFillColor(ROOT.kGray+1)
    go.SetLineColor(ROOT.kGray+1)
    ge=gmmtt_e.Clone()
    ge.SetFillColor(ROOT.kGray+1)
    ge.SetLineColor(ROOT.kGray+1)
    legend2=make_legend2()
    legend2.AddEntry(ge,"expected","l")
    legend2.AddEntry(go,"observed","fl")
    #legend2.Draw("same")

    ROOT.gPad.RedrawAxis()

    lumiBlurb1=add_CMS()
    lumiBlurb1.Draw("same")
    lumiBlurb2=add_Preliminary()
    lumiBlurb2.Draw("same")
    lumiBlurb=add_lumi()
    lumiBlurb.Draw("same")
    lumi=add_model(args.model,args.tanbeta)
    lumi.Draw("same")
    lumi2=add_arxiv(args.model,args.tanbeta)
    #lumi2.Draw("same")
    postfix=""
    if (args.model>1):
        postfix="_tanbeta"+str(int(args.tanbeta))
    canvas.SaveAs('plots/run2_plot_BRaa_Type'+str(args.model)+postfix+'.png')
    canvas.SaveAs('plots/run2_plot_BRaa_Type'+str(args.model)+postfix+'.pdf')

    #canvas2 = MakeCanvas("asdf","asdf",800,800)
    #canvas2.cd()
    #legend.Draw()
    #legend2.Draw("same")
    #canvas2.SaveAs('plots/legende.png')
    #canvas2.SaveAs('plots/legende.pdf')
