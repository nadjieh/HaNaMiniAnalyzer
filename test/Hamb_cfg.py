import FWCore.ParameterSet.Config as cms

process = cms.Process("HaNa")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("RecoMET/METProducers.METSignificance_cfi")
process.load("RecoMET/METProducers.METSignificanceParams_cfi")
##____________________________________________________________________________||
process.load('Configuration.StandardSequences.Services_cff')
#process.load("JetMETCorrections.Modules.JetResolutionESProducer_cfi")
#from CondCore.DBCommon.CondDBSetup_cfi import *

#process.jer = cms.ESSource("PoolDBESSource",
#      CondDBSetup,
#      toGet = cms.VPSet(
#         # Pt Resolution
#         cms.PSet(
#            record = cms.string('JetResolutionRcd'),
#            tag    = cms.string('JR_MC_PtResolution_Summer15_25nsV6_AK4PFchs'),
#            label  = cms.untracked.string('AK4PFchs_pt')
#            ),
#
#         # Phi Resolution
#         cms.PSet(
#            record = cms.string('JetResolutionRcd'),
#            tag    = cms.string('JR_MC_PhiResolution_Summer15_25nsV6_AK4PFchs'),
#            label  = cms.untracked.string('AK4PFchs_phi')
#            ),
#
#         # Scale factors
#         cms.PSet(
#            record = cms.string('JetResolutionScaleFactorRcd'),
#            tag    = cms.string('JR_DATAMCSF_Summer15_25nsV6_AK4PFchs'),
#            label  = cms.untracked.string('AK4PFchs')
#            ),
#         ),
#      connect = cms.string('sqlite:Summer15_25nsV6.db')
#      )

#process.es_prefer_jer = cms.ESPrefer('PoolDBESSource', 'jer')

##____________________________________________________________________________||
process.TFileService = cms.Service("TFileService", fileName = cms.string("histo.root") )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
                            fileNames = cms.untracked.vstring()
)

process.load("Haamm.HaNaMiniAnalyzer.Hamb_cfi")
#process.TTH 

import FWCore.ParameterSet.VarParsing as opts
options = opts.VarParsing ('analysis')
options.register('sync',
                 0,
		 #1,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int ,
                 "")
options.register('sample',
		 'TTbar',
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 'Sample to analyze')
options.register('job',
                 0,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int ,
                 "number of the job")
options.register('nFilesPerJob',
                 1,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int ,
                 "number of the files pre job")
options.register('output',
                 "out",
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string ,
                 "could be root://eoscms//eos/cms/store/user/hbakhshi/out")

options.parseArguments()


theSample = None
import os

if options.sync == 0 :
    from Samples80.Samples import MiniAOD80Samples as samples


    for sample in samples:
        if sample.Name == options.sample :
            theSample = sample

    if not theSample.Name == options.sample:
        raise NameError("The correct sample is not found %s !+ %s" % (sample.Name , options.sample) )

    if theSample == None:
        raise NameError("Sample with name %s wasn't found" % (options.sample))
else:
    from Haamm.HaNaMiniAnalyzer.Sample import *
    theSample = Sample( "Sync" , "Sync" , 100 , False , 0 , "" )
    #theSample.Files = ['/store/mc/RunIIFall15MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1/00000/0C5BB11A-E2C1-E511-8C02-002590A831B6.root']
    theSample.Files = ['/store/mc/RunIISpring16MiniAODv2/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/00000/001AFDCE-C33B-E611-B032-0025905D1C54.root']
    #theSample.Files = ['/store/data/Run2016C/DoubleMuon/MINIAOD/PromptReco-v2/000/275/658/00000/0498AA19-863B-E611-A9B3-02163E0138A8.root']
    options.nFilesPerJob = 1
    options.output = "out" 
    options.job = 0

process.Hamb.sample = theSample.Name
process.Hamb.LHE.useLHEW = theSample.LHEWeight
process.Hamb.isData = theSample.IsData
process.Hamb.Jets.BTagCuts = cms.vint32(0,-1)
process.Hamb.DiMuon.MuonLeadingPtCut = cms.double(20)

if not ( options.job < theSample.MakeJobs( options.nFilesPerJob , options.output ) ):
    raise NameError("Job %d is not in the list of the jobs of sample %s with %d files per run" % (options.job , options.sample , options.nFilesPerJob ) )
job = theSample.Jobs[ options.job ]

process.source.fileNames.extend( job.Inputs )
process.TFileService.fileName = job.Output

process.maxEvents.input = options.maxEvents

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
runMetCorAndUncFromMiniAOD(process, isData = theSample.IsData)

if theSample.IsData :
    process.Hamb.MET.Input = "slimmedMETsMuEGClean"
    
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(filename = (process.Hamb.SetupDir.value() + '/JSON.txt')).getVLuminosityBlockRange()
    #process.GlobalTag.globaltag = '76X_dataRun2_v15'
    #process.GlobalTag.globaltag = '80X_dataRun2_Prompt_ICHEP16JEC_v0
    process.GlobalTag.globaltag = '80X_dataRun2_2016SeptRepro_v7'
    if (theSample.Name is 'DoubleMuH2') or (theSample.Name is 'DoubleMuH3'):
	process.GlobalTag.globaltag = '80X_dataRun2_Prompt_v16'
    
    
    process.p = cms.Path( process.fullPatMetSequence+process.METSignificance + process.Hamb )
    #process.p = cms.Path( process.Hamb )
    for v in range(0 , 10 ):
        process.Hamb.HLT_Mu17Mu8_DZ.HLT_To_Or.append( 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v%d' % (v) )
        process.Hamb.HLT_Mu17Mu8_DZ.HLT_To_Or.append( 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v%d' % (v) )
        process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v%d' % (v) )
        process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v%d' % (v) )
        process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_IsoMu24_v%d' % (v) )
        process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_IsoTkMu24_v%d' % (v) )
        process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_IsoMu22_eta2p1_v%d' % (v) )
        process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_IsoTkMu22_eta2p1_v%d' % (v) )


else :
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

   # If you only want to re-correct and get the proper uncertainties
    runMetCorAndUncFromMiniAOD(process,
                               isData=False
                               )
    process.Hamb.MET.Input = "slimmedMETs"

    process.Hamb.Jets.ApplyJER = True
    #process.GlobalTag.globaltag = '76X_dataRun2_16Dec2015_v0' #76X_mcRun2_asymptotic_RunIIFall15DR76_v1
    #process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_miniAODv2_v1'
    process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v8'
    # from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import *
    # process.patJetCorrFactorsReapplyJEC = updatedPatJetCorrFactors.clone(
    #     src = cms.InputTag("slimmedJets"),
    #     levels = ['L1FastJet', 
    #               'L2Relative', 
    #               'L3Absolute'],
    #     payload = 'AK4PFchs' ) # Make sure to choose the appropriate levels and payload here!

    # process.patJetsReapplyJEC = updatedPatJets.clone(
    #     jetSource = cms.InputTag("slimmedJets"),
    #     jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
    #     )

    # process.Hamb.Jets.Input = "patJetsReapplyJEC"
    # process.METSignificance.srcPfJets = "patJetsReapplyJEC"
    #  + process.METSignificance
    process.p = cms.Path( process.fullPatMetSequence + process.Hamb)
    if options.sync == 0 :
        for v in range(0 , 10 ):
            process.Hamb.HLT_Mu17Mu8_DZ.HLT_To_Or.append( 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v%d' % (v) )
            process.Hamb.HLT_Mu17Mu8_DZ.HLT_To_Or.append( 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v%d' % (v) )
            process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v%d' % (v) )
            process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v%d' % (v) )
            process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_IsoMu24_v%d' % (v) )
            process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_IsoTkMu24_v%d' % (v) )
            process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_IsoMu22_eta2p1_v%d' % (v) )
            process.Hamb.HLT_Mu17Mu8.HLT_To_Or.append( 'HLT_IsoTkMu22_eta2p1_v%d' % (v) )
    if theSample.DSName.count( "_reHLT_" ):
	process.Hamb.HLT_Mu17Mu8_DZ.Input = cms.InputTag( "TriggerResults","","HLT2" )
	process.Hamb.HLT_Mu17Mu8.Input = cms.InputTag( "TriggerResults","","HLT2" )

    if theSample.Name.count("GGH") :
        process.HambPUUp = process.Hamb.clone()
        process.HambPUUp.Vertex.PUDataFileName = "pileUpDataUp.root"
        process.HambPUDown = process.Hamb.clone()
        process.HambPUDown.Vertex.PUDataFileName = "pileUpDataDown.root"
        process.HambJECUP = process.Hamb.clone()
        process.HambJECUP.Jets.JECUncertainty = 1
        process.HambJECDOWN = process.Hamb.clone()
        process.HambJECDOWN.Jets.JECUncertainty = -1
        process.HambJERUP = process.Hamb.clone()
        process.HambJERUP.Jets.JERUncertainty = 2
        process.HambJERDOWN = process.Hamb.clone()
        process.HambJERDOWN.Jets.JERUncertainty = 1
        process.HambBUP = process.Hamb.clone()
        process.HambBUP.Jets.BTagUncertainty = 1
        process.HambBDOWN = process.Hamb.clone()
        process.HambBDOWN.Jets.BTagUncertainty = -1                
        process.HambMETJESDOWN = process.Hamb.clone()
        process.HambMETJESDOWN.MET.Uncertainty = 3
        process.HambMETJESUP = process.Hamb.clone()
        process.HambMETJESUP.MET.Uncertainty = 2
        process.HambMETUnClusDOWN = process.Hamb.clone()
        process.HambMETUnClusDOWN.MET.Uncertainty = 11
        process.HambMETUnClusUP = process.Hamb.clone()
        process.HambMETUnClusUP.MET.Uncertainty = 10
        process.HambHLTUP = process.Hamb.clone()
        process.HambHLTUP.DiMuon.HLTUnc = 1
        process.HambHLTDOWN = process.Hamb.clone()
        process.HambHLTDOWN.DiMuon.HLTUnc = -1
        process.pathSystematics = cms.Path( process.HambPUDown + process.HambPUUp + process.HambJECUP + process.HambJECDOWN + process.HambBUP + process.HambBDOWN + process.HambJERUP + process.HambJERDOWN + process.HambMETJESUP + process.HambMETJESDOWN + process.HambMETUnClusUP + process.HambMETUnClusDOWN + process.HambHLTDOWN + process.HambHLTUP )

process.outp1=cms.OutputModule("PoolOutputModule",
   outputCommands = cms.untracked.vstring('keep *'), 
   fileName = cms.untracked.string(job.Output2),
   SelectEvents = cms.untracked.PSet(  SelectEvents = cms.vstring('p')  )
)


#process.ep = cms.EndPath( process.outp1 )


