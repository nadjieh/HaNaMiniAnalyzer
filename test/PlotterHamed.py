#!/usr/bin/env python
from ROOT import gROOT, TLatex, TCanvas, TFile, gROOT, TColor
import math
import string

LUMI=35900
LOCATION = "/eos/user/a/ajafari/"
#LOCATION = "/home/ajafari/cernbox/"

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

nTuples = "%s/Hamb13/March02_Full2016_MassProd_CorrectBtag/withSelVariables/withMoreBtags/" %(LOCATION)
datanTuples = "%s/Hamb13/June06_Full2016_MassProd/withSelVariables/withMoreBtags/" %(LOCATION)
#nTuples = "/home/hbakhshi/Downloads/Hamb_Nadjieh/withSelVariables/"

from Haamm.HaNaMiniAnalyzer.SampleType import *
from ROOT import kGray, kGreen, kOrange, kRed, kBlack, kCyan, kBlue, kAzure, kTeal, kPink, kYellow
ci = TColor.GetColor("#ff6666")
DYSamples = SampleType("DY" , ci , [ GetSample(DYJets80) , GetSample(DYJetsLowMass80), GetSample(WJetsMG80)] , nTuples )
ci = TColor.GetColor("#ffff66")
TopSamples = SampleType("Top" , ci , [ GetSample(TTBar80) , GetSample(TW80), GetSample(TbarW80) , GetSample(TChannelTbar80) , GetSample( TChannelT80 ) ] , nTuples )
ci = 38
DiBosonSamples = SampleType("DiBoson" , ci , [ GetSample(ZZ80) , GetSample(WZ80), GetSample(WW80) ] , nTuples )
ci = TColor.GetColor("#996633")

bWeightLL = "bWeightLL"
bWeightML = "bWeightML"
bWeightTL = "bWeightTL"
bWeightTM = "bWeightTM"
bWeightTT = "bWeightTT"
bWeightMM = "bWeightMM"

if len(sys.argv) == 3:
    bW = "bWsShape.%s" %(sys.argv[2])
    bWeightLL = bW
    bWeightML = bW
    bWeightTL = bW
    bWeightTM = bW
    bWeightTT = bW
    bWeightMM = bW

signalsamples = []
#signalsamples.append (SampleType( "Signal15" , kAzure+10 , [ GetSample(GGH1580) ] , nTuples , True ))
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
dataSamples2 = SampleType("Data" , kBlack , listofdata  , datanTuples  ) # , additionalCut="(higgsMass > 135 || higgsMass < 115)"
allSTs = [ dataSamples2 , DiBosonSamples, TopSamples, DYSamples ]
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

upperboundMuPt = ""

Cuts = { "HLT":"(passHLT_Mu17Mu8 || passHLT_Mu17Mu8_DZ)",
         "BasicJetsMu":"passJetSize && passMuSize && passJet1Pt && passJet2Pt && passMu1Pt && passMu2Pt %s" %(upperboundMuPt),
         "MET":"met < 60 ",
         "chi2sum":"chi2Sum < 5 ",
         "TL":"passTL" ,
         "TM":"passTM" ,
         "TT":"passTT" ,
         "MM":"passMM" ,
         "LL" : "1==1",
         "TLFormula":"Max$(jetsBtag) > 0.9535 && Sum$( jetsBtag > 0.5426 ) > 1",
         "invchi2sum":"chi2Sum > 5 && chi2Sum < 11",
         "mHDiff25":"abs(higgsMass - 125) < 25",
         "mHDiff10":"abs(higgsMass - 125) < 10",         
	 "lowmet":"met<30",
	 "highmet":"met>30",
	 "TLexc":"passTL && !passTM && !passTT",
	 "TMexc":"passTM && !passTT"
         }

cPreselectionLL = CutInfo( "PreselectionLL" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "LL"]] ) , "Weight*%s" %(bWeightLL) , title="2#mu2loose-bjets"  )
cPreselectionTL = CutInfo( "PreselectionTL" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL"]] ) , "Weight*%s" %(bWeightTL) , title="2#mu, tight-loose b-jets"  )
cPreselectionTM = CutInfo( "PreselectionTM" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TM"]] ) , "Weight*%s" %(bWeightTM) , title="2#mu, tight-medium b-jets"  )
cPreselectionTT = CutInfo( "PreselectionTT" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TT"]] ) , "Weight*%s" %(bWeightTT) , title="2#mu, tight-tight b-jets"  )
cPreselectionMM = CutInfo( "PreselectionMM" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "MM"]] ) , "Weight*%s" %(bWeightMM) , title="2#mu, medium-medium b-jets"  )


cTLMetBlind = CutInfo( "TLMetBlind" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET"]] ) , "Weight*%s" %(bWeightTL) , title="2#mu, tight-loose b-jets, met>60 (blind)" , blind=True  )
cSRTLBlind = CutInfo( "SRTLBlind" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET" , "chi2sum"]] ) , "Weight*%s" %(bWeightTL) , title="Signal Region (blind)" , blind=True )

cSRTL = CutInfo( "SRTL" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET" , "chi2sum"]] ) , "Weight*%s" %(bWeightTL) , title="Signal Region - TL"  )
cSRTM = CutInfo( "SRTM" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TM" , "MET" , "chi2sum"]] ) , "Weight*%s" %(bWeightTM) , title="Signal Region - TM"  )
cSRTT = CutInfo( "SRTT" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TT" , "MET" , "chi2sum"]] ) , "Weight*%s" %(bWeightTT) , title="Signal Region - TT"  )
cSRMM = CutInfo( "SRMM" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "MM" , "MET" , "chi2sum"]] ) , "Weight*%s" %(bWeightMM) , title="Signal Region - MM"  )
cSRTLmHDiff25 = CutInfo( "SRTLmHDiff25" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET" , "mHDiff25"]] ) , "Weight*%s" %(bWeightTL) , title="Signal Region - TL (mH 25)"  )
cSRTLmHDiff10 = CutInfo( "SRTLmHDiff10" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET" , "mHDiff10"]] ) , "Weight*%s" %(bWeightTL) , title="Signal Region - TL (mH 10)"  )

cTLMet = CutInfo( "TLMet" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET"]] ) , "Weight*%s" %(bWeightTL) , title="2#mu, tight-loose b-jets, met>60"   )
cTLChi2Sum = CutInfo( "TLChi2Sum" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "chi2sum"]] ) , "Weight*%s" %(bWeightTL) , title="2#mu, tight-loose b-jets, chi2sum<5"   )
cTLInvChi2Sum = CutInfo( "CRChi2Sum" , "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET", "invchi2sum"]] ) , "Weight*%s" %(bWeightTL) , title="2#mu, tight-loose b-jets, 11>chi2sum>5"   )

#Categories for more sensitivity
cSRLowMET = CutInfo("SRLowMET", "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET" , "chi2sum", "lowmet"]] ), "Weight*%s" %(bWeightTL) , title="SR+MET<30"   )
cSRHighMET = CutInfo("SRHighMET", "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET" , "chi2sum", "highmet"]] ), "Weight*%s" %(bWeightTL) , title="SR+MET>30"   )
cCRLowMET = CutInfo("CRLowMET", "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET" , "invchi2sum", "lowmet"]] ), "Weight*%s" %(bWeightTL) , title="CR+MET<30"   )
cCRHighMET = CutInfo("CRHighMET", "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TL" , "MET" , "invchi2sum", "highmet"]]), "Weight*%s" %(bWeightTL) , title="CR+MET>30"   )

cSRTLexc = CutInfo("SRTLexc", "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TLexc" , "MET" , "chi2sum"]] ), "Weight*%s" %(bWeightTL) , title="SR+TLexc"   )
cSRTMexc = CutInfo("SRTMexc", "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TMexc" , "MET" , "chi2sum"]] ), "Weight*%s" %(bWeightTM) , title="SR+TMexc"   )
cCRTLexc = CutInfo("CRTLexc", "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TLexc" , "MET" , "invchi2sum"]] ), "Weight*%s" %(bWeightTL) , title="CR+TLexc"   )
cCRTMexc = CutInfo("CRTMexc", "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TMexc" , "MET" , "invchi2sum"]]), "Weight*%s" %(bWeightTM) , title="CR+TMexc"   )
cCRTT = CutInfo("CRTT", "&&".join( [Cuts[ss] for ss in ["HLT", "BasicJetsMu" , "TT" , "MET" , "invchi2sum"]]), "Weight*%s" %(bWeightTT) , title="CR+TT"   )

cuts = [cPreselectionTL, cPreselectionTM, cPreselectionTT, cPreselectionMM, cPreselectionLL , cTLMet , cSRTL , cSRTM, cSRTT, cSRMM, cSRTLBlind, cTLMetBlind, cTLChi2Sum, cTLInvChi2Sum, cSRTLmHDiff25, cSRTLmHDiff10,  cSRLowMET,cSRHighMET, cCRLowMET,cCRHighMET, cSRTLexc, cSRTMexc,cCRTLexc, cCRTMexc, cCRTT ]

for cut in cuts :
    if "Blind" not in cut.Name :
        cut.AddHist( "nJets" , "@jetsPt.size()", 10 , 0 , 10, False , Title="#jets" , dirName="Jets" )
        cut.AddHist( "nVertices" , "nVertices" , 50 , 0. , 50., False , Title="#Vertices" , dirName="General" )
        cut.AddHist( "metPhi" , "abs(metPhi)" , 16 , 0. , 3.2, False , Title="#phi" , dirName="MET" )
        cut.AddHist( "metSig" , "metSig" , 25, 0, 50, False , Title="met significance" , dirName="MET" )
        met = cut.AddHist( "met" , "met" , 30 , 0. , 300, False , Title="met" , dirName="MET")
        cut.AddHist( "amuPt" , "amPt" , 30 , 0. , 300., False , Title="p_{T}^{#mu#mu}" , dirName="MuMu")
        cut.AddHist( "abPt" , "abPt" , 30 , 0. , 300., False , Title="p_{T}^{bb}" , dirName="bb")
        cut.AddHist( "abMass" , "abMass" , 24, 10. , 250., False , Title="m_{bb}" , dirName="bb")
        cut.AddHist( "Mu1Pt" , "muPt[0]" , 50 , 0 , 500 , False , Title="p_{T}^{#mu} (leading)"  , dirName="Mus" )
        cut.AddHist( "Mu2Pt" , "muPt[1]" , 50 , 0 , 500 , False , Title="p_{T}^{#mu} (sub-leading)" , dirName="Mus")
        cut.AddHist( "Jet1Pt" , "jetsPt[0]" , 50 , 0 , 500 , False , Title="p_{T}^{jet} (leading)" , dirName="Jets")
        cut.AddHist( "Jet2Pt" , "jetsPt[1]" , 50 , 0 , 500 , False , Title="p_{T}^{jet} (sub-leading)", dirName="Jets")
        cut.AddHist( "Mu1Eta" , "muEta[0]" , 10 , -2.5 , 2.5 , False , Title="#mu_{lead.} #eta" , dirName="Mus")
        cut.AddHist( "Mu2Eta" , "muEta[1]" , 10 , -2.5 , 2.5 , False , Title="#mu_{sub-lead.} #eta" , dirName="Mus" )
        cut.AddHist( "Jet1Eta" , "jetsEta[0]" , 10 ,-2.5 , 2.5 , False , Title="jet_{lead.} #eta" , dirName="Jets")
        cut.AddHist( "Jet2Eta" , "jetsEta[1]" , 10 , -2.5 , 2.5 , False , Title="jet_{sub-lead.} #eta" , dirName="Jets"  )
    chi2sum = cut.AddHist( "chi2Sum" , "chi2Sum", 25 , 0. , 50., False , Title="#chi^{2}_{H}+#chi^{2}_{a#rightarrowbb}", dirName="Jets")
    amuMass = cut.AddHist( "amuMass" , "aMuMass", 25 , 20 , 70 , Title="#mu#mu mass" , dirName="General")
    cut.AddHist( "HiggsMass" , "higgsMass" , 46 , 75 , 305, False , Title="m_{#mu#mubb}" , dirName="MuMU" )
    cut.AddHist( "HiggsPt" , "higgsPt" , 30 , 0. , 300., False , Title="p_{T}^{#mu#mubb}", dirName="MuMubb")
    cut.AddHist( "chi2B" , "chi2B", 25 , 0. , 50., False , Title="#chi^{2}_{a#rightarrowbb}" , dirName="bb")
    cut.AddHist( "chi2H" , "chi2H", 25 , 0. , 50., False , Title="#chi^{2}_{H#rightarrowbb#mu#mu}" , dirName="MuMubb" )
    cut.AddHist( "chi2SUM" , "chi2Sum", 25 , 0. , 50., False , Title="Sum #chi^{2}" , dirName="MuMubb" )
    cut.AddHist( "HiggsMDiff" , "abs(higgsMass - 125.0)", 20 , 0. , 100., False , Title="|mass_{#mu#mubb}-125.0|" , dirName="MuMubb" )
    #cut.AddHist( amuMass , chi2sum )
    #cut.AddHist( amuMass , met )

for c in cuts :
    plotter.AddTreePlots( c )

name_extent = sys.argv[1] if len(sys.argv) >= 2 else "defaults"
plotter.LoadHistos( LUMI , "%s" %(name_extent))
if len(sys.argv) == 3:
    name_extent = name_extent+sys.argv[2]
fout = TFile.Open("out_FinalPlots_%s.root" %(name_extent), "recreate")
plotter.Write(fout, False)
fout.Close()
