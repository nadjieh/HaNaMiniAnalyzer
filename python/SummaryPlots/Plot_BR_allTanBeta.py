import argparse as argparse
import math
import os
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas
from BR import get_total_width
from BR import gamma_quarks
from BR import gamma_mu
from BR import gamma_tau
from BR import gamma_photon
from BR import gamma_gg
import ROOT
import numpy as np
from array import array

def add_lumi():
    lowX=0.64
    lowY=0.835
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.045)
    lumi.AddText("19.7 fb^{-1} (8 TeV)")
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
    lumi.AddText("Preliminary")
    return lumi 

def make_legend():
    output = ROOT.TLegend(0.55, 0.18, 0.75, 0.45, "", "brNDC")
    output.SetLineWidth(0)
    output.SetLineStyle(0)
    #output.SetFillStyle(0)
    output.SetFillColor(0)
    output.SetBorderSize(0)
    output.SetTextFont(62)
    return output

def add_model(channel,ma):
    lowX=0.21
    lowY=0.71
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.40, lowY+0.16, "NDC")
    lumi.SetTextSize(0.04)
    lumi.SetBorderSize(   0 )
    #lumi.SetFillStyle(    0 )
    lumi.SetFillColor(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(62)
    #lumi.AddText("2HDM+S type "+str(model)+", tan#beta = "+str(tanbeta))
    lumi.AddText("2HDM+S, m_{a} = "+str(int(ma))+" GeV")
    if channel=="mmtt":
       lumi.AddText("aa#rightarrow#mu#mu#tau#tau")
    if channel=="tttt":
       lumi.AddText("aa#rightarrow#tau#tau#tau#tau")
    if channel=="mmmm":
       lumi.AddText("aa#rightarrow#mu#mu#mu#mu")
    if channel=="mmbb":
       lumi.AddText("aa#rightarrow#mu#mubb")
    return lumi

def add_arxiv(channel,ma):
    lowX=0.21
    lowY=0.63
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

    style1=GetStyleHtt()
    style1.cd()

    parser = argparse.ArgumentParser()
    parser.add_argument('--channel', default='mmtt', help="mmtt,tttt,mmmm or mmbb?")
    parser.add_argument('--ma', type=float, default='1', help="Which pseudoscalar mass?")

    args = parser.parse_args()

    mintanbeta=0.1
    maxtanbeta=5
    n=100
    step=(maxtanbeta-mintanbeta)/n
    BRmm=1
    BRtt=1
    BRbb=1
    a_y1=[]
    a_y2=[]
    a_y3=[]
    a_y4=[]
    a_x=[]
    for i in range(0,100):
       tanbeta=mintanbeta+step*i
       width1=get_total_width(1,float(args.ma),tanbeta)
       width2=get_total_width(2,float(args.ma),tanbeta)
       width3=get_total_width(3,float(args.ma),tanbeta)
       width4=get_total_width(4,float(args.ma),tanbeta)
       BRmm1=gamma_mu(tanbeta,float(args.ma),1)/width1
       BRtt1=gamma_tau(tanbeta,args.ma,1)/width1
       BRbb1=gamma_quarks(tanbeta,args.ma,1,6)/width1
       BRmm2=gamma_mu(tanbeta,float(args.ma),2)/width2
       BRtt2=gamma_tau(tanbeta,args.ma,2)/width2
       BRbb2=gamma_quarks(tanbeta,args.ma,2,6)/width2
       BRmm3=gamma_mu(tanbeta,float(args.ma),3)/width3
       BRtt3=gamma_tau(tanbeta,args.ma,3)/width3
       BRbb3=gamma_quarks(tanbeta,args.ma,3,6)/width3
       BRmm4=gamma_mu(tanbeta,float(args.ma),4)/width4
       BRtt4=gamma_tau(tanbeta,args.ma,4)/width4
       BRbb4=gamma_quarks(tanbeta,args.ma,4,6)/width4
       if args.channel=="mmtt":
          a_y1.append(2*BRtt1*BRmm1)
          a_y2.append(2*BRtt2*BRmm2)
          a_y3.append(2*BRtt3*BRmm3)
          a_y4.append(2*BRtt4*BRmm4)
       if args.channel=="bbtt":
          a_y1.append(2*BRtt1*BRbb1)
          a_y2.append(2*BRtt2*BRbb2)
          a_y3.append(2*BRtt3*BRbb3)
          a_y4.append(2*BRtt4*BRbb4)
       if args.channel=="mmbb":
          a_y1.append(2*BRbb1*BRmm1)
          a_y2.append(2*BRbb2*BRmm2)
          a_y3.append(2*BRbb3*BRmm3)
          a_y4.append(2*BRbb4*BRmm4)
       if args.channel=="mmmm":
          a_y1.append(BRmm1*BRmm1)
          a_y2.append(BRmm2*BRmm2)
          a_y3.append(BRmm3*BRmm3)
          a_y4.append(BRmm4*BRmm4)
       if args.channel=="tttt":
          a_y1.append(BRtt1*BRtt1)
          a_y2.append(BRtt2*BRtt2)
          a_y3.append(BRtt3*BRtt3)
          a_y4.append(BRtt4*BRtt4)
       a_x.append(tanbeta)

    x = array("d", a_x)
    y1 = array("d", a_y1)
    y2 = array("d", a_y2)
    y3 = array("d", a_y3)
    y4 = array("d", a_y4)

    g1 = ROOT.TGraph(len(x),x,y1)
    g2 = ROOT.TGraph(len(x),x,y2)
    g3 = ROOT.TGraph(len(x),x,y3)
    g4 = ROOT.TGraph(len(x),x,y4)

    canvas = MakeCanvas("asdf","asdf",800,800)
    canvas.cd()
    canvas.SetLogy()
    canvas.SetLogx()
    canvas.SetGridx()
    canvas.SetGridy()
    g1.Draw("AC")
    g1.GetXaxis().SetRangeUser(0.1,5);
    g1.GetXaxis().SetLimits(0.1,5);
    g1.SetLineColor(ROOT.kOrange)
    g1.SetMinimum(0.0000000001);
    g1.SetMaximum(1);
    g1.GetXaxis().SetTitle("tan #beta");
    if args.channel=="mmtt":
       g1.GetYaxis().SetTitle("B(aa#rightarrow#mu#mu#tau#tau)")
    if args.channel=="mmbb":
       g1.GetYaxis().SetTitle("B(aa#rightarrow#mu#mubb)")
    if args.channel=="bbtt":
       g1.GetYaxis().SetTitle("B(aa#rightarrow bb#tau#tau)")
       g1.SetMinimum(0.001);
       g1.SetMaximum(1);
    if args.channel=="mmmm":
       g1.GetYaxis().SetTitle("B(aa#rightarrow#mu#mu#mu#mu)")
       g1.SetMinimum(0.000000000001);
       g1.SetMaximum(200);
    if args.channel=="tttt":
       g1.GetYaxis().SetTitle("B(aa#rightarrow#tau#tau#tau#tau)")
       g1.SetMinimum(0.001);
       g1.SetMaximum(50);
    g1.SetLineWidth(5)
    g1.SetLineStyle(1)
    g1.Draw("AC")
    canvas.Update();
    g2.SetLineColor(ROOT.kPink-3)
    g2.SetLineWidth(5)
    g2.SetLineStyle(2)
    g2.Draw("same")
    g3.SetLineColor(ROOT.kGreen+1)
    g3.SetLineWidth(5)
    g3.SetLineStyle(7)
    g3.Draw("same")
    g4.SetLineColor(ROOT.kViolet-5)
    g4.SetLineWidth(5)
    g4.SetLineStyle(8)
    g4.Draw("same")
    canvas.Update();

    legend=make_legend()
    legend.AddEntry(g1,"Type I","l")
    legend.AddEntry(g2,"Type II","l")
    legend.AddEntry(g3,"Type III","l")
    legend.AddEntry(g4,"Type IV","l")
    legend.Draw("same")

    #lumiBlurb1=add_CMS()
    #lumiBlurb1.Draw("same")
    #lumiBlurb2=add_Preliminary()
    #lumiBlurb2.Draw("same")
    #lumiBlurb=add_lumi()
    #lumiBlurb.Draw("same")
    lumi=add_model(args.channel,args.ma)
    lumi.Draw("same")
    #lumi2=add_arxiv(args.channel,args.ma)
    #lumi2.Draw("same")
    canvas.SaveAs('plots/plot_BR'+str(args.channel)+'_ma'+str(int(args.ma))+'.png')
    canvas.SaveAs('plots/plot_BR'+str(args.channel)+'_ma'+str(int(args.ma))+'.pdf')

