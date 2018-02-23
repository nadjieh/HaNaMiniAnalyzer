#!/usr/bin/env python
from ROOT import gROOT, TLatex, TCanvas, TFile, gROOT, TColor
import math
import string

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


#nTuples = "/home/nadjieh/cernbox/Hamb13/Oct14_8020_Opt/Trees/"
nTuples = "/home/nadjieh/cernbox/Hamb13/June06_Full2016_MassProd/"
print ">>>>"
from Haamm.HaNaMiniAnalyzer.SampleType import *
from ROOT import kGray, kGreen, kOrange, kRed, kBlack, kCyan, kBlue, kAzure, kTeal, kPink, kYellow
ci = TColor.GetColor("#ff6666")
DYSamples = SampleType("DY" , ci , [ GetSample(DYJets80) , GetSample(DYJetsLowMass80)] , nTuples )
ci = TColor.GetColor("#ffff66")
TopSamples = SampleType("Top" , ci , [ GetSample(TTBar80) , GetSample(TW80), GetSample(TbarW80) ] , nTuples )
ci = TColor.GetColor("#996633")
Mass = sys.argv[3]
lowmass = "15"
highmass = "70"
signalsamples = []
if(Mass == "20"):
#signalsamples.append(SampleType( "Signal15" , kRed+3 , [ GetSample(GGH1580) ] , nTuples , True ))
	signalsamples.append(SampleType( "Signal20" , kRed+2 , [ GetSample(GGH2080) ] , nTuples , True ))
	lowmass = "15"
	highmass = "25"
elif(Mass == "25"):	
	signalsamples.append(SampleType( "Signal25" , kRed+2 , [ GetSample(GGH2580) ] , nTuples , True ))
	lowmass = "20"
	highmass = "30"
elif(Mass == "30"):	
	signalsamples.append(SampleType( "Signal30" , kRed+2 , [ GetSample(GGH3080) ] , nTuples , True ))
	lowmass = "25"
	highmass = "35"
elif(Mass == "35"):	
	signalsamples.append(SampleType( "Signal35" , kRed+2 , [ GetSample(GGH3580) ] , nTuples , True ))
	lowmass = "30"
	highmass = "40"
elif(Mass == "40"):	
	signalsamples.append(SampleType( "Signal40" , kRed+2 , [ GetSample(GGH4080) ] , nTuples , True ))
	lowmass = "35"
	highmass = "45"
elif(Mass == "45"):	
	signalsamples.append(SampleType( "Signal45" , kRed+2 , [ GetSample(GGH4580) ] , nTuples , True ))
	lowmass = "40"
	highmass = "50"
elif(Mass == "55"):	
	signalsamples.append(SampleType( "Signal55" , kRed+2 , [ GetSample(GGH5580) ] , nTuples , True ))
	lowmass = "50"
	highmass = "60"
elif(Mass == "60"):	
	signalsamples.append(SampleType( "Signal60" , kRed+2 , [ GetSample(GGH6080) ] , nTuples , True ))
	lowmass = "55"
	highmass = "65"
else:
	signalsamples.append (SampleType( "Signal15" , kAzure+10 , [ GetSample(GGH1580) ] , nTuples , True ))
	signalsamples.append (SampleType( "Signal20" , kBlue+2 , [ GetSample(GGH2080) ] , nTuples , True ))
	signalsamples.append (SampleType( "Signal25" , kCyan+2	, [ GetSample(GGH2580) ] , nTuples , True ))
	signalsamples.append (SampleType( "Signal30" , kTeal+10 , [ GetSample(GGH3080) ] , nTuples , True ))
	signalsamples.append (SampleType( "Signal35" , kGreen+2 , [ GetSample(GGH3580) ] , nTuples , True ))
	signalsamples.append (SampleType( "Signal40" , kYellow+2 , [ GetSample(GGH4080) ] , nTuples , True ))
	signalsamples.append (SampleType( "Signal45" , kOrange-2 , [ GetSample(GGH4580) ] , nTuples , True ))
	signalsamples.append (SampleType( "Signal50" , kOrange+10 , [ GetSample(GGH5080) ] , nTuples , True ))
	signalsamples.append (SampleType( "Signal55" , kRed+2 , [ GetSample(GGH5580) ] , nTuples , True ))
	signalsamples.append (SampleType( "Signal60" , kPink+10 , [ GetSample(GGH6080) ] , nTuples , True ))



nTotals = {}
            
from Haamm.HaNaMiniAnalyzer.Plotter import *
plotter = Plotter()
listofdata = [GetSample(s) for s in MiniAOD80Samples if s.IsData]
dataSamples2 = SampleType("Data" , kBlack , [ listofdata[0] ]  , nTuples ) # the first item must be data
allSTs = [ dataSamples2 , TopSamples, DYSamples]
allSTs.extend(signalsamples)
for st in allSTs :
    plotter.AddSampleType( st )
    for s in st.Samples:
        if s.IsData :
            continue
        if s.Name in nTotals :
            s.SetNTotal( nTotals[s.Name] )
        else:
            print "total number for sample %s is not set" % s.Name

amuPx = "muPt[0]*cos(muPhi[0])+muPt[1]*cos(muPhi[1])"
amuPy = "muPt[0]*sin(muPhi[0])+muPt[1]*sin(muPhi[1])"
amuPz = "muPt[0]*sinh(muEta[0])+muPt[1]*sinh(muEta[1])"
amuEn = "sqrt(pow(muPt[0]*cos(muPhi[0]),2)+pow(muPt[0]*sin(muPhi[0]),2)+pow(muPt[0]*sinh(muEta[0]),2))+sqrt(pow(muPt[1]*cos(muPhi[1]),2)+pow(muPt[1]*sin(muPhi[1]),2)+pow(muPt[1]*sinh(muEta[1]),2))"

amuMass = "sqrt(pow(%s,2) + pow(%s,2) + pow(%s,2) - pow(%s,2))" %(amuPx,amuPy,amuPz,amuEn)

abPx = "jetsPt[0]*cos(jetsPhi[0])+jetsPt[1]*cos(jetsPhi[1])"
abPy = "jetsPt[0]*sin(jetsPhi[0])+jetsPt[1]*sin(jetsPhi[1])"
abPz = "jetsPt[0]*sinh(jetsEta[0])+jetsPt[1]*sinh(jetsEta[1])"
abEn = "jetsE[0] + jetsE[1]"

abMass = "sqrt(pow(%s,2) + pow(%s,2) + pow(%s,2) - pow(%s,2))" %(abPx,abPy,abPz,abEn)
dphiBB_ = "abs(jetsPhi[0]-jetsPhi[1])"
dphiBB = "(%s >= 3.14)*(6.28 - %s)+(%s < 3.14)*%s" %(dphiBB_,dphiBB_,dphiBB_,dphiBB_)
detaBB = "abs(jetsEta[0]-jetsEta[1])"
DR = "sqrt(pow(%s,2) + pow(%s,2))" % (dphiBB , detaBB)

hx = "%s+%s" %(amuPx,abPx)
hy = "%s+%s" %(amuPy,abPy)
hz = "%s+%s" %(amuPz,abPz)
he = "%s+%s" %(amuEn,abEn)

mH = "sqrt(pow(%s,2) + pow(%s,2) + pow(%s,2) - pow(%s,2))" %(hx,hy,hz,he)

width = "0.18 + 0.175* %s" %(amuMass)
chi2B = "pow((%s-%s),2)/(%s*%s)" %(amuMass,abMass,width,width)
chi2H = "pow((%s-125),2)/(10.56*10.56)" %(mH)
chi2Sum = "%s+%s" %(chi2B, chi2H)


masscut = "%s < %s && %s > %s" %(amuMass,highmass,amuMass,lowmass)
mupt = masscut+" && muPt[0]>20 && muPt[1]>9"
jetpt = mupt + "&& jetsPt[0]>20 && jetsPt[1]>15"
metSig = jetpt+" && met < 60"
#mhdiff = jetpt+" && fabs(%s -125) < 15" %(mH)
mhdiff = "abs(%s -125) < 15" %(mH)
chi2HCut = "%s < 5" %(chi2H)
chi2BCut = "%s < 5" %(chi2B)
chi2SumCut = "%s < 5" %(chi2Sum)
trueb = metSig + " && abs(jetsFlavour[0]) == 5 && abs(jetsFlavour[1]) == 5"
metcut = "met < 50"

#btagWP = [0.460, 0.800, 0.935] #ICHEP
btagWP = [0.5426, 0.8484, 0.9535] # full2016
Lumi = 35900

LL =  "jetsBtag[0] > %f && jetsBtag[1] > %f && %s" %(btagWP[0], btagWP[0], masscut)
ML =  "(jetsBtag[0] > %f && jetsBtag[1] > %f) | (jetsBtag[0] > %f && jetsBtag[1] > %f) && %s" %(btagWP[1], btagWP[0], btagWP[0], btagWP[1], masscut)
#TL =  "(jetsBtag[0] > %f && jetsBtag[1] > %f) | (jetsBtag[0] > %f && jetsBtag[1] > %f) && %s && %s" %(btagWP[2], btagWP[0], btagWP[0], btagWP[2], chi2SumCut,metSig)
TL =  "( (jetsBtag[0] > %f && jetsBtag[1] > %f) | (jetsBtag[0] > %f && jetsBtag[1] > %f) ) && %s" %(btagWP[2], btagWP[0], btagWP[0], btagWP[2], metcut)
MM =  "jetsBtag[0] > %f && jetsBtag[1] > %f && %s" %(btagWP[1], btagWP[1], masscut)
TM =  "(jetsBtag[0] > %f && jetsBtag[1] > %f) | (jetsBtag[0] > %f && jetsBtag[1] > %f) && %s" %(btagWP[2], btagWP[1], btagWP[1], btagWP[2], masscut)
TT =  "jetsBtag[0] > %f && jetsBtag[1] > %f && %s" %(btagWP[2], btagWP[2], masscut)

Cuts = {"LL":LL,
	    "ML":ML,
	    "TL":TL,
	    "MM":MM,
	    "TM":TM,
	    "TT":TT,
	    "metSig":metSig,
	    }

cLL = CutInfo( "LL" , Cuts["LL"])
cML = CutInfo( "ML" , Cuts["ML"])
cTL = CutInfo( "TL" , Cuts["TL"])
cMM = CutInfo( "MM" , Cuts["MM"])
cTM = CutInfo( "TM" , Cuts["TM"])
cTT = CutInfo( "TT" , Cuts["TT"])

print Cuts["TL"]

cMetSig = CutInfo( "metSig" , Cuts["metSig"])

mHDiff = "abs(%s-125)" %(mH)

cLL.AddHist( "HiggsMDiff" , mHDiff, 20 , 0. , 100., False )
cLL.AddHist( "amuMass" , amuMass, 55 , 15 , 70)
cLL.AddHist( "chi2B" , chi2B, 25 , 0. , 50., False )
cLL.AddHist( "chi2H" , chi2H, 25 , 0. , 50., False )
cLL.AddHist( "chi2Sum" , chi2Sum, 25 , 0. , 50., False )

cML.AddHist( "HiggsMDiff" , mHDiff, 20 , 0. , 100., False )
cML.AddHist( "amuMass" , amuMass, 55 , 15 , 70)
cML.AddHist( "chi2B" , chi2B, 25 , 0. , 50., False )
cML.AddHist( "chi2H" , chi2H, 25 , 0. , 50., False )
cML.AddHist( "chi2Sum" , chi2Sum, 25 , 0. , 50., False )

#cTL.AddHist( "MuPtLead" , "muPt[0]", 75 , 0. , 150., True )
#cTL.AddHist( "MuPtSubLead" , "muPt[1]", 75 , 0. , 150., True )
#cTL.AddHist( "JetPtLead" , "jetsPt[0]", 75 , 0. , 150., True )
#cTL.AddHist( "JetPtSubLead" , "jetsPt[1]", 75 , 0. , 150., True )
cTL.AddHist( "Met" , "met", 100 , 0. , 200., False )
#cTL.AddHist( "MetSig" , "metSig", 50 , 0. , 10., False )
cTL.AddHist( "HiggsMDiff" , mHDiff, 20 , 0. , 100., False )
cTL.AddHist( "amuMass" , amuMass, 55 , 15 , 70)
#cTL.AddHist( "chi2B" , chi2B, 25 , 0. , 50., False )
#cTL.AddHist( "chi2H" , chi2H, 25 , 0. , 50., False )
cTL.AddHist( "chi2Sum" , chi2Sum, 25 , 0. , 50., False )
#cTL.AddHist( "DRbb" , DR, 25 , 0. , 10., True )

cMM.AddHist( "HiggsMDiff" , mHDiff, 20 , 0. , 100., False )
cMM.AddHist( "amuMass" , amuMass, 55 , 15 , 70)
cMM.AddHist( "chi2B" , chi2B, 25 , 0. , 50., False )
cMM.AddHist( "chi2H" , chi2H, 25 , 0. , 50., False )
cMM.AddHist( "chi2Sum" , chi2Sum, 25 , 0. , 50., False )


cTM.AddHist( "HiggsMDiff" , mHDiff, 20 , 0. , 100., False )
cTM.AddHist( "amuMass" , amuMass, 55 , 15 , 70)
cTM.AddHist( "chi2B" , chi2B, 25 , 0. , 50., False )
cTM.AddHist( "chi2H" , chi2H, 25 , 0. , 50., False )
cTM.AddHist( "chi2Sum" , chi2Sum, 25 , 0. , 50., False )

cTT.AddHist( "HiggsMDiff" , mHDiff, 20 , 0. , 100., False )
cTT.AddHist( "amuMass" , amuMass, 55 , 15 , 70)
cTT.AddHist( "chi2B" , chi2B, 25 , 0. , 50., False )
cTT.AddHist( "chi2H" , chi2H, 25 , 0. , 50., False )
cTT.AddHist( "chi2Sum" , chi2Sum, 25 , 0. , 50., False )

cMetSig.AddHist( "HiggsMDiff" , mHDiff, 20 , 0. , 100., False )
cMetSig.AddHist( "amuMass" , amuMass, 55 , 15 , 70)
cMetSig.AddHist( "chi2B" , chi2B, 25 , 0. , 50., False )
cMetSig.AddHist( "chi2H" , chi2H, 25 , 0. , 50., False )
cMetSig.AddHist( "chi2Sum" , chi2Sum, 25 , 0. , 50., False )

import sys
method = sys.argv[1]
print "I'm going to apply %s" % (method)
cuttoapply = sys.argv[2] 
allcuts = []

#allcuts.append( cLL )
#allcuts.append( cML )
allcuts.append( cTL )
#allcuts.append( cMM )
#allcuts.append( cTM )
#allcuts.append( cTT )


if method == "significance":
	for i in range(0, len(allcuts)):
		plotter.AddTreePlots( allcuts[i] )
	plotter.LoadHistos( Lumi )
	#plotter.CalcSignificances(2)
	plotter.CalcSignificances(3)
	plotter.CalcSignificances(4)
	#plotter.CalcSignificances(5)
elif method == "limit":
	for i in range(0, len(allcuts)):
		if cuttoapply == allcuts[i].Name :
			plotter.AddTreePlots( allcuts[i] )
			plotter.LoadHistos( Lumi )
			break
	plotter.CalcExpLimits()
else:
	print "not implemented"
	exit()

fout = TFile.Open("out_mH_ttdy_%s_%s_%s.root" %(method,cuttoapply,Mass), "recreate")
plotter.Write(fout, False)
fout.Close()
