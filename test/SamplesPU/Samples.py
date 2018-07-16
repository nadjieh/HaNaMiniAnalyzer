from Haamm.HaNaMiniAnalyzer.Sample import *

import os
Sample.WD = os.path.dirname(os.path.abspath(__file__))
print Sample.WD

MINIAOD = []

SingleMuonB1 = Sample( "SingleMuB1" ,  0 , False , "/SingleMuon/Run2016B-03Feb2017_ver1-v1/MINIAOD")
SingleMuonB2 = Sample( "SingleMuB2" ,  0 , False  , "/SingleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD")
SingleMuonC = Sample( "SingleMuC" ,  0 , False ,  "/SingleMuon/Run2016C-03Feb2017-v1/MINIAOD")
SingleMuonD = Sample( "SingleMuD" ,  0 , False ,  "/SingleMuon/Run2016D-03Feb2017-v1/MINIAOD")
SingleMuonE = Sample( "SingleMuE" ,  0 , False ,  "/SingleMuon/Run2016E-03Feb2017-v1/MINIAOD")
SingleMuonF = Sample( "SingleMuF" ,  0 , False ,  "/SingleMuon/Run2016F-03Feb2017-v1/MINIAOD")
SingleMuonG = Sample( "SingleMuG" ,  0 , False ,  "/SingleMuon/Run2016G-03Feb2017-v1/MINIAOD")
SingleMuonH2 = Sample( "SingleMuH2" ,  0 , False ,  "/SingleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD" )
SingleMuonH3 = Sample( "SingleMuH3" ,  0 , False ,  "/SingleMuon/Run2016H-03Feb2017_ver3-v1/MINIAOD" )

MINIAOD.extend( [ SingleMuonB1 , SingleMuonB2 , SingleMuonC , SingleMuonD , SingleMuonE , SingleMuonF , SingleMuonG , SingleMuonH2 , SingleMuonH3 ] )

ZMuMu = Sample( "ZmuMu" , 1 , False ,  "/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM" )
DYMuMu0J = Sample( "DYMuMu0J" , 1 , False ,  "/DYToLL_0J_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" )
DYMuMu1J = Sample( "DYMuMu1J" , 1 , False ,  "/DYToLL_1J_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" )
DYMuMu2J = Sample( "DYMuMu2J" , 1 , False ,  "/DYToLL_2J_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM" )

ZMuMuM1 = Sample( "ZmuMuM1" , 1 , False , "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-FlatPU0to75TuneCUETP8M1_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM")
ZMuMuM2 = Sample( "ZmuMuM2" , 1 , False , "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-FlatPU0to75TuneCUETP8M2_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM")
ZMuMuM3 = Sample( "ZmuMuM3" , 1 , False , "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-FlatPU0to75TuneCUETP8M3_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM")
ZMuMuM4 = Sample( "ZmuMuM4" , 1 , False , "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-FlatPU0to75TuneCUETP8M4_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM")

MINIAOD.extend( [ ZMuMuM1 , ZMuMuM2 , ZMuMuM3 , ZMuMuM4  ] ) #, DYMuMu0J , DYMuMu1J , DYMuMu2J ] )

NuGunM1 = Sample("NuGunM1" , 1 , False , "/NeutrinoGun_E_10GeV/RunIISummer16MiniAODv2-FlatPU0to75TuneCUETP8M1_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM")
NuGunM2 = Sample("NuGunM2" , 1 , False , "/NeutrinoGun_E_10GeV/RunIISummer16MiniAODv2-FlatPU0to75TuneCUETP8M2_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM")
NuGunM3 = Sample("NuGunM3" , 1 , False , "/NeutrinoGun_E_10GeV/RunIISummer16MiniAODv2-FlatPU0to75TuneCUETP8M3_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM")
NuGunM4 = Sample("NuGunM4" , 1 , False , "/NeutrinoGun_E_10GeV/RunIISummer16MiniAODv2-FlatPU0to75TuneCUETP8M4_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM")

MINIAOD.extend( [ NuGunM1 , NuGunM2 , NuGunM3 , NuGunM4 ] )

MinBiasB = Sample("MinBiasB" , 0 , False , "/MinimumBias/Run2016B-03Feb2017_ver1-v1/MINIAOD")
MinBiasF = Sample("MinBiasF" , 0 , False , "/MinimumBias/Run2016F-03Feb2017-v1/MINIAOD")
MinBiasG = Sample("MinBiasG" , 0 , False , "/MinimumBias/Run2016G-PromptReco-v1/MINIAOD")
MinBiasH1 = Sample("MinBiasH1" , 0 , False , "/MinimumBias/Run2016H-PromptReco-v1/MINIAOD")
MinBiasH2 = Sample("MinBiasH2" , 0 , False , "/MinimumBias/Run2016H-PromptReco-v2/MINIAOD")
MinBiasH3 = Sample("MinBiasH3" , 0 , False , "/MinimumBias/Run2016H-PromptReco-v3/MINIAOD")

MINIAOD.extend( [ MinBiasB , MinBiasF , MinBiasG , MinBiasH1 , MinBiasH2 , MinBiasH3 ] )

ZeroBiasH3 = Sample("ZeroBiasH3" , 0 , False , "/ZeroBias/Run2016H-03Feb2017_ver3-v1/MINIAOD")
ZeroBiasH2 = Sample("ZeroBiasH2" , 0 , False , "/ZeroBias/Run2016H-03Feb2017_ver2-v1/MINIAOD")
ZeroBiasG = Sample("ZeroBiasG" , 0 , False , "/ZeroBias/Run2016G-03Feb2017-v1/MINIAOD")
ZeroBiasF = Sample("ZeroBiasF" , 0 , False , "/ZeroBias/Run2016F-03Feb2017-v1/MINIAOD")
ZeroBiasE = Sample("ZeroBiasE" , 0 , False , "/ZeroBias/Run2016E-03Feb2017-v1/MINIAOD")
ZeroBiasD = Sample("ZeroBiasD" , 0 , False , "/ZeroBias/Run2016D-03Feb2017-v1/MINIAOD")
ZeroBiasC = Sample("ZeroBiasC" , 0 , False , "/ZeroBias/Run2016C-03Feb2017-v1/MINIAOD")

MINIAOD.extend( [ ZeroBiasC , ZeroBiasD , ZeroBiasE , ZeroBiasF , ZeroBiasG , ZeroBiasH2 , ZeroBiasH3 ] )


SingleNeutrinoTuneCP0 = Sample("SingleNeutrinoTuneCP0" , 1 , False , "/SingleNeutrino/RunIISummer16MiniAODv2-FlatPU0to75TuneCP0_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v3/MINIAODSIM" )
SingleNeutrinoTuneCP2 = Sample("SingleNeutrinoTuneCP2" , 1 , False , "/SingleNeutrino/RunIISummer16MiniAODv2-FlatPU0to75TuneCP2_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM" )
SingleNeutrinoTuneCP5 = Sample("SingleNeutrinoTuneCP5" , 1 , False , "/SingleNeutrino/RunIISummer16MiniAODv2-FlatPU0to75TuneCP5_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/MINIAODSIM" )

SingleNeutrinos = []
SingleNeutrinos.extend( [ SingleNeutrinoTuneCP0 , SingleNeutrinoTuneCP2 , SingleNeutrinoTuneCP5 ] )
MINIAOD.extend( [ SingleNeutrinoTuneCP0 , SingleNeutrinoTuneCP2 , SingleNeutrinoTuneCP5 ] )

