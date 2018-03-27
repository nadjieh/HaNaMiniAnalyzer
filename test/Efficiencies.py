#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Haamm.HaNaMiniAnalyzer.ExtendedSample import *
from Samples80.Samples import *
from ROOT import gROOT, TLatex, TCanvas, TFile, gROOT, TColor, TH1
import math
import string

LUMI=35900
gROOT.SetBatch(True)

class CUTFlowTable :
    def __init__(self, cft , sampleName):
        self.SampleName = sampleName
        self.CFT = cft
        self.BinNames = { 1:["All"],
                          2:["HLT"],
                          3:["Vertex"],
                          4:["AtLeast2Mu"],
                          5:["OppositeSign"],
                          6:["Mass>12"],
                          7:["NotUnderZPeak"],
                          8:["2Jets"],
                          9:["2bJets"]}
        for cut in self.BinNames:
            self.BinNames[cut].append( cft.GetBinContent(cut ) )
            self.BinNames[cut].append( cft.GetBinError(cut ) )

    def Add(self, name , integral , error ):
        index = max( self.BinNames )+1
        self.BinNames[index] = [name, integral , error]
    
    def Print(self , refIndexForEff = 1 , indices = None , header = False):
        #print self.BinNames
        if not indices:
            indices = sorted( self.BinNames )
        if header :
            txt = " \t"
            for i in indices:
                txt += self.BinNames[i][0] + "\t"
            print txt
        txt = self.SampleName + "\t"
        refVal = self.BinNames[refIndexForEff][1]
        refErr = self.BinNames[refIndexForEff][2]
        refErrRatio2 = (refErr/refVal)*(refErr/refVal)
        for cut in indices :
            val = self.BinNames[cut][1]
            err = self.BinNames[cut][2]
            Eff = 100*val/refVal
            ratioErr = Eff*math.sqrt( (err/val)*(err/val) + refErrRatio2 )
            txt += "%g\t" % (Eff/100 ) #+%.4f%% , ratioErr )
        print txt

nTuples = "/home/hbakhshi/Downloads/Hamb_Nadjieh/withSelVariables/"
AllSamples = []
SamplesToPrint = { TTBar80:[],
                   DYJets80:[],
                   DYJetsLowMass80:[]}

                   # TChannelTbar80:[],
                   # TChannelT80:[],
                   # TW80:[],
                   # TbarW80:[],
                   # ZZ80:[],
                   # WZ80:[],
                   # WW80:[],
                   # GGH3080:[],
                   # GGH6080:[]
                   # }
for s in SamplesToPrint:
    es = ExtendedSample( s )
    es.LoadJobs( nTuples )
    es.LoadHistos()
    #es.NormalizeHistos( LUMI )
    cft = es.GetCFT()
    cft.GetBinContent( 3 )
    c = CUTFlowTable( cft , s.Name)
    integral, err = es.CutYields( "(passJetSize && passMuSize && passJet1Pt && passJet2Pt && passMu1Pt && passMu2Pt)"  , "(Weight*bWeightLL)" )
    c.Add( "BLL" , integral , err )
    integral, err = es.CutYields( "(passJetSize && passMuSize && passJet1Pt && passJet2Pt && passMu1Pt && passMu2Pt && (met < 60))"  , "(Weight*bWeightLL)" )
    c.Add( "met" , integral , err )
    integral, err = es.CutYields( "(passJetSize && passMuSize && passJet1Pt && passJet2Pt && passMu1Pt && passMu2Pt && (met < 60) && (passTL))"  , "(Weight*bWeightTL)" )
    c.Add( "TL" , integral , err )
    integral, err = es.CutYields( "(passJetSize && passMuSize && passJet1Pt && passJet2Pt && passMu1Pt && passMu2Pt && (met < 60) && (passTL) && (aMuMass < 70) && (aMuMass > 20))"  , "(Weight*bWeightTL)" )
    c.Add( "Mass20_70" , integral , err )
    integral, err = es.CutYields( "(passJetSize && passMuSize && passJet1Pt && passJet2Pt && passMu1Pt && passMu2Pt && (met < 60) && (passTL) && (chi2Sum < 5) && (aMuMass < 70) && (aMuMass > 20))"  , "(Weight*bWeightTL)" )
    c.Add( "Chi2Sum" , integral , err )            
    SamplesToPrint[s].append( c )
    AllSamples.append(es)

header = True
for s in SamplesToPrint:
    SamplesToPrint[s][0].Print(3 , [5,7,8,10,11,12,13,14] , header)
    header = False
