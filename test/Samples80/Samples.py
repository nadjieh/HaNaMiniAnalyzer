from Haamm.HaNaMiniAnalyzer.Sample import *

import os
Sample.WD = os.path.dirname(os.path.abspath(__file__))
print Sample.WD

MiniAOD80Samples = []

DoubleMuB80 = Sample("DoubleMuB" , 0 , False ,  "/DoubleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD" )
MiniAOD80Samples.append( DoubleMuB80 )

DoubleMuC80 = Sample("DoubleMuC" , 0 , False ,  "/DoubleMuon/Run2016C-03Feb2017-v1/MINIAOD" )
MiniAOD80Samples.append( DoubleMuC80 )

DoubleMuD80 = Sample("DoubleMuD" , 0 , False ,  "/DoubleMuon/Run2016D-03Feb2017-v1/MINIAOD" )
MiniAOD80Samples.append( DoubleMuD80 )

DoubleMuE80 = Sample("DoubleMuE" , 0 , False ,  "/DoubleMuon/Run2016E-03Feb2017-v1/MINIAOD" )
MiniAOD80Samples.append( DoubleMuE80 )

DoubleMuF80 = Sample("DoubleMuF" , 0 , False ,  "/DoubleMuon/Run2016F-03Feb2017-v1/MINIAOD" )
MiniAOD80Samples.append( DoubleMuF80 )

DoubleMuG80 = Sample("DoubleMuG" , 0 , False ,  "/DoubleMuon/Run2016G-03Feb2017-v1/MINIAOD" )
MiniAOD80Samples.append( DoubleMuG80 )

DoubleMuH280 = Sample("DoubleMuH2" , 0 , False ,  "/DoubleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD" )
MiniAOD80Samples.append( DoubleMuH280 )

DoubleMuH380 = Sample("DoubleMuH3" , 0 , False ,  "/DoubleMuon/Run2016H-03Feb2017_ver3-v1/MINIAOD" )
MiniAOD80Samples.append( DoubleMuH380 )

WJetsMG80 = Sample( "WJetsMG" , 61526.7 , False , "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM" )
MiniAOD80Samples.append( WJetsMG80 )

DYJets80 = Sample( "DYJets" , 6025.2 , True ,  "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYJets80 )

DYJetsLowMass80 = Sample( "DYJetsLowMass" , 18610.0 , True ,  "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYJetsLowMass80 )

TTBar80 = Sample( "TTbar" , 831.80 , False ,  "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( TTBar80 )

TChannelTbar80 = Sample("TChannelTbar" , 81 , True ,  "/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( TChannelTbar80 )

TChannelT80 = Sample("TChannelT" , 136 , True ,  "/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( TChannelT80 )

TW80 = Sample("TW" , 35.6 , False ,  "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" )
MiniAOD80Samples.append( TW80 )

TbarW80 = Sample("TbarW" , 35.6 , False ,  "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" )
MiniAOD80Samples.append( TbarW80 )

ZZ80 = Sample( "ZZ" ,  15.4*2*0.071 , True ,  "/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append(ZZ80)

WZ80 = Sample( "WZ" ,  44.9*0.068 , True ,  "/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append(WZ80)

WW80 = Sample( "WW" ,  118.7 , False ,  "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM")
MiniAOD80Samples.append(WW80)

VBF2080 = Sample( "VBF20", 3.7820*1.7*0.0001,True, "/SUSYVBFToHToAA_AToMuMu_AToBB_M-20_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM")
MiniAOD80Samples.append(VBF2080)

VBF4080 = Sample( "VBF40", 3.7820*1.7*0.0001,True, "/SUSYVBFToHToAA_AToMuMu_AToBB_M-40_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM")
MiniAOD80Samples.append(VBF4080)

VBF6080 = Sample( "VBF60", 3.7820*1.7*0.0001,True, "/SUSYVBFToHToAA_AToMuMu_AToBB_M-60_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM")
MiniAOD80Samples.append(VBF6080)                                  

GGH1580 = Sample( "GGH15", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-15_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
MiniAOD80Samples.append(GGH1580)

GGH2080 = Sample( "GGH20", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-20_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
MiniAOD80Samples.append(GGH2080)

GGH2580 = Sample( "GGH25",48.5800*1.7*0.0001 ,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-25_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
MiniAOD80Samples.append(GGH2580)

GGH3080 = Sample( "GGH30", 48.5800*1.7*0.0001 ,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-30_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
MiniAOD80Samples.append(GGH3080)

GGH3580 = Sample( "GGH35", 48.5800*1.7*0.0001 ,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-35_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
MiniAOD80Samples.append(GGH3580)

GGH4080 = Sample( "GGH40", 48.5800*1.7*0.0001 ,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-40_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
MiniAOD80Samples.append(GGH4080)

GGH4580 = Sample( "GGH45", 48.5800*1.7*0.0001 ,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-45_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
MiniAOD80Samples.append(GGH4580)

GGH5080 = Sample( "GGH50", 48.5800*1.7*0.0001 ,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-50_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
MiniAOD80Samples.append(GGH5080)

GGH5580 = Sample( "GGH55", 48.5800*1.7*0.0001 ,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-55_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
MiniAOD80Samples.append(GGH5580)

GGH6080 = Sample( "GGH60", 48.5800*1.7*0.0001 ,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-60_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
MiniAOD80Samples.append(GGH6080)


GGHbbtt2080 = Sample( "GGHbbtt20", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToBB_AToTauTau_M-20_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM")
MiniAOD80Samples.append(GGHbbtt2080)

GGHbbtt4080 = Sample( "GGHbbtt40", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToBB_AToTauTau_M-40_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM")
MiniAOD80Samples.append(GGHbbtt4080)

GGHbbtt6080 = Sample( "GGHbbtt60", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToBB_AToTauTau_M-60_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM")
MiniAOD80Samples.append(GGHbbtt6080)


GGHmmtt2080 = Sample( "GGHmmtt20", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-20_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM")
MiniAOD80Samples.append(GGHmmtt2080)

GGHmmtt4080 = Sample( "GGHmmtt40", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-40_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM")
MiniAOD80Samples.append(GGHmmtt4080)

GGHmmtt6080 = Sample( "GGHmmtt60", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-60_TuneCUETP8M1_13TeV_madgraph_pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM")
MiniAOD80Samples.append(GGHmmtt6080)

#branching fractions for the DYMG samples are taken from AN 2016/360, no number is provided for DYMGInclusive10To50, the same k-factor of high mass is used for it
DYMGInclusive10To50XSection = 18610.*4895./5765.
DYLowMassZeroJet = DYMGInclusive10To50XSection -( (725.*18610./DYMGInclusive10To50XSection) + (395.*18610./DYMGInclusive10To50XSection) + (97.*18610./DYMGInclusive10To50XSection) + (34.8*18610./DYMGInclusive10To50XSection))
DYHighMasssZeroJet = 5765 - ((51.*5765./4895.)+(96.*5765./4895.)+(331.*5765./4895.)+(1016.*5765./4895))

DYMGInclusive10To50 = Sample( "DYMGInclusive10To50" , DYMGInclusive10To50XSection , True , "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMGInclusive10To50 )

DYMG0J10To50 = Sample( "DYMG0J10To50" , DYLowMassZeroJet , True , "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append(DYMG0J10To50)

DYMGInclusive50Ext1 = Sample( "DYMGInclusive50Ext1" , 5765 , True , "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM" )
MiniAOD80Samples.append( DYMGInclusive50Ext1 )

DYMGInclusive50Ext2 = Sample( "DYMGInclusive50Ext2" , 5765 , True , "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMGInclusive50Ext2 )

DYMG0J50Ext1 = Sample( "DYMG0J50Ext1" , DYHighMasssZeroJet , True , "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM" )
MiniAOD80Samples.append( DYMG0J50Ext1)

DYMG0J50Ext2 = Sample( "DYMG0J50Ext2" , DYHighMasssZeroJet , True , "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMG0J50Ext2 )

DYMG1J10To50 = Sample( "DYMG1J10To50" , 725.*18610./DYMGInclusive10To50XSection , True , "/DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMG1J10To50 )

DYMG1J50 = Sample( "DYMG1J50" , 1016.*5765./4895. , True , "/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMG1J50 )

DYMG2J10To50 = Sample( "DYMG2J10To50" , 395.*18610./DYMGInclusive10To50XSection , True , "/DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMG2J10To50 )

DYMG2J50 = Sample( "DYMG2J50" , 331.*5765./4895. , True , "/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMG2J50 )

DYMG3J10To50 = Sample( "DYMG3J10To50" , 97.*18610./DYMGInclusive10To50XSection , True , "/DY3JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMG3J10To50 )

DYMG3J50 = Sample( "DYMG3J50" , 96.*5765./4895. , True , "/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMG3J50 )

DYMG4J10To50 = Sample( "DYMG4J10To50" , 34.8*18610./DYMGInclusive10To50XSection , True , "/DY4JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMG4J10To50 )

DYMG4J50 = Sample( "DYMG4J50" , 51.*5765./4895. , True , "/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
MiniAOD80Samples.append( DYMG4J50 )

GGH20PSGENSIM = Sample( "GGH20PSGENSIM", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-20_TuneCUETP8M1_13TeV_madgraph_Herwigpp/hbakhshi-PSHerwigpp_RAWSIMoutput-ab3049243ffd725f50ccf1808f052c71/USER")
MiniAOD80Samples.append(GGH20PSGENSIM)

GGH40PSGENSIM = Sample( "GGH40PSGENSIM", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-40_TuneCUETP8M1_13TeV_madgraph_Herwigpp/hbakhshi-PSHerwigpp_RAWSIMoutput-bd046e34aab243306fd3f61b9f692474/USER")
MiniAOD80Samples.append(GGH40PSGENSIM)

GGH60PSGENSIM = Sample( "GGH60PSGENSIM", 48.5800*1.7*0.0001,True, "/SUSYGluGluToHToAA_AToMuMu_AToBB_M-60_TuneCUETP8M1_13TeV_madgraph_Herwigpp/hbakhshi-PSHerwigpp_RAWSIMoutput-51e223377599988f71f1e6bca84210cb/USER")
MiniAOD80Samples.append(GGH60PSGENSIM)
