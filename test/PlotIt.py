#!/usr/bin/env python
LUMI = 35900
from ROOT import gROOT, TLatex, TCanvas, TFile, gROOT, TColor
import math
from Yields_Oct14_MassProd  import *
#from Haamm.HaNaMiniAnalyzer.Yields_Oct14_Opt  import *

#nTuples = "/home/nadjieh/cernbox/Hamb13/Oct14_8020_MassProd/Trees/withReg"

gROOT.SetBatch(True)

from Samples80.Samples import *
samples = None
runOnOutsOfAnotherJob = False
if runOnOutsOfAnotherJob :
    samples = samples24june
    samples += sampleswith24juneonly
else :
    samples = MiniAOD80Samples

def GetSample( s ):
    if runOnOutsOfAnotherJob:
        for ss in samples:
            if s.Name == ss.Name :
                return ss
        return None
    else:
        return s
    
from Haamm.HaNaMiniAnalyzer.SampleType import *
from ROOT import kGray, kGreen, kOrange, kRed, kBlack, kCyan, kBlue, kAzure, kTeal, kPink, kYellow
dataSamples = SampleType("Data" , kBlack , [GetSample(s) for s in MiniAOD80Samples if s.IsData] , nTuples ) #the first item must be data
ci = TColor.GetColor("#ff6666")
DYSamples = SampleType("DY" , ci , [ GetSample(DYJets80) , GetSample(DYJetsLowMass80), GetSample(WJetsMG80)] , nTuples )
ci = TColor.GetColor("#ffff66")
TopSamples = SampleType("Top" , ci , [ GetSample(TTBar80) , GetSample(TChannelT80) , GetSample(TChannelTbar80) , GetSample(TW80), GetSample(TbarW80) ] , nTuples )
DibosonSamples = SampleType("Diboson" , kAzure-9 , [ GetSample(ZZ80) , GetSample(WZ80) , GetSample(WW80)] , nTuples )


mySignals = []

mySignals.append (SampleType( "Signal15" , kAzure+10 , [ GetSample(GGH1580) ] , nTuples , True ))
mySignals.append (SampleType( "Signal20" , kBlue+2 , [ GetSample(GGH2080) ] , nTuples , True ))
mySignals.append (SampleType( "Signal25" , kCyan+2	, [ GetSample(GGH2580) ] , nTuples , True ))
mySignals.append (SampleType( "Signal30" , kTeal+10 , [ GetSample(GGH3080) ] , nTuples , True ))
mySignals.append (SampleType( "Signal35" , kGreen+2 , [ GetSample(GGH3580) ] , nTuples , True ))
mySignals.append (SampleType( "Signal40" , kYellow+2 , [ GetSample(GGH4080) ] , nTuples , True ))
mySignals.append (SampleType( "Signal45" , kOrange-2 , [ GetSample(GGH4580) ] , nTuples , True ))
mySignals.append (SampleType( "Signal50" , kOrange+10 , [ GetSample(GGH5080) ] , nTuples , True ))
mySignals.append (SampleType( "Signal55" , kRed+2 , [ GetSample(GGH5580) ] , nTuples , True ))
mySignals.append (SampleType( "Signal60" , kPink+10 , [ GetSample(GGH6080) ] , nTuples , True ))

nTotals = {}
            
from Haamm.HaNaMiniAnalyzer.Plotter import *
plotter = Plotter()
allSTs = [dataSamples ,DibosonSamples , TopSamples , DYSamples ]
for iSt in mySignals:
    allSTs.append(iSt)

for st in allSTs :
    plotter.AddSampleType( st )
    for s in st.Samples:
        if s.IsData :
            continue
        if s.Name in nTotals :
            s.SetNTotal( nTotals[s.Name] )
        else:
            print "total number for sample %s is not set" % s.Name
  

            
cDiMu = CutInfo( "Trigger" , Cuts["Trigger"],myW,False)
cDiMu.AddHist( "amuMass" , amuMass, 55 , 15 , 70)
cDiMu.AddHist( "DR" , DR, 50 , 0 , 5)

cMetSig = CutInfo( "MuPt" , Cuts["MuPt"],myW,False)
cMetSig.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cJetPt = CutInfo( "JetPt" , Cuts["JetPt"],myW,False)
cJetPt.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cOptimCuts = CutInfo( "OptimCuts" , Cuts["OptimCuts"],myW,False)
cOptimCuts.AddHist( "amuMass" , amuMass, 55 , 15 , 70)
cOptimCuts.AddHist( "DR" , DR, 10 , 0 , 5)
cOptimCuts.AddHist( "DMass" , "abs("+abMass+"-"+amuMass+")", 50 , 0 , 100)
cOptimCuts.AddHist( "Dphi" , dphi, 8 , 0 , 4)
cOptimCuts.AddHist( "Deta" , deta, 10 , 0 , 5)
cOptimCuts.AddHist( "hPtReg" , hRegPt, 50 , 0 , 500)
cOptimCuts.AddHist( "hPt" , hPt, 50 , 0 , 500)
cOptimCuts.AddHist( "hMassReg" , mHReg, 30 , 0 , 300)
cOptimCuts.AddHist( "hMass" , mH, 30 , 0 , 300)
cOptimCuts.AddHist( "LeadmuLeadbMass" ,lb0M , 30 , 0 , 300)
cOptimCuts.AddHist( "LeadmuSubleadbMass" ,lb1M , 30 , 0 , 300)
cOptimCuts.AddHist( "SubmuLeadbMass" ,lb2M , 30 , 0 , 300)
cOptimCuts.AddHist( "SubmuSubleadbMass" ,lb3M , 30 , 0 , 300)
cOptimCuts.AddHist( "Chi2B", "pow(("+abMass+"-"+amuMass+"),2)/pow(%s,2)" %(width), 50, 0, 50)
cOptimCuts.AddHist( "Chi2H", "pow(("+mH+"-125),2)/pow(10.56,2)", 50, 0, 50)
cOptimCuts.AddHist( "Chi2Sum", "pow(("+mH+"-125),2)/pow(10.56,2) + pow(("+abMass+"-"+amuMass+"),2)/pow(%s,2)" %(width), 50, 0, 50)
cJetPt25 = CutInfo( "JetPt25" , Cuts["JetPt25"],myW,False)
cJetPt25.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cMET = CutInfo( "MET" , Cuts["MET"],myW,False)
cMET.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cMETJet25 = CutInfo( "METJet25" , Cuts["METJet25"],myW,False)
cMETJet25.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cLL = CutInfo( "LL" , Cuts["LL"],myW,False)
cLL.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cML = CutInfo( "ML" , Cuts["ML"],myWLM,False)
cML.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cTL = CutInfo( "TL" , Cuts["TL"],myWLT,False)
cTL.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cMM = CutInfo( "MM" , Cuts["MM"],myWMM,False)
cMM.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cTM = CutInfo( "TM" , Cuts["TM"],myWMT,False)
cTM.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cTT = CutInfo( "TT" , Cuts["TT"],myWTT,False)
cTT.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cChi2B = CutInfo( "Chi2B" , Cuts["Chi2B"],myWTT,False)
cChi2B.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cChi2H = CutInfo( "Chi2H" , Cuts["Chi2H"],myWTT,False)
cChi2H.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

cChi2Sum = CutInfo( "Chi2Sum" , Cuts["Chi2Sum"],myWTT,False)
cChi2Sum.AddHist( "amuMass" , amuMass, 55 , 15 , 70)

plotter.AddTreePlots( cDiMu )
plotter.AddTreePlots( cMetSig )
plotter.AddTreePlots( cJetPt )
plotter.AddTreePlots( cOptimCuts )
plotter.AddTreePlots( cJetPt25 )
plotter.AddTreePlots( cMET )
plotter.AddTreePlots( cMETJet25 )

plotter.AddTreePlots( cLL )
plotter.AddTreePlots( cML )
plotter.AddTreePlots( cTL )
plotter.AddTreePlots( cMM )
plotter.AddTreePlots( cTM )
plotter.AddTreePlots( cTT )
plotter.AddTreePlots( cChi2B )
plotter.AddTreePlots( cChi2H )
plotter.AddTreePlots( cChi2Sum )

plotter.LoadHistos( LUMI )

fout = TFile.Open("out_cft_normtolumi_unblind_"+outname+".root", "recreate")
plotter.Write(fout, False)
fout.Close()
