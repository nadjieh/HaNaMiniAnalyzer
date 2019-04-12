import FWCore.ParameterSet.VarParsing as opts
options = opts.VarParsing ('analysis')
options.register('mass',
                 0,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.int ,
                 "")

options.parseArguments()


mass = options.mass
print mass
import sys
print sys.argv
del sys.argv[-1]
print sys.argv

from WMCore.Configuration import Configuration
config = Configuration()


config.section_("General")
config.General.requestName = "HIG_18_011_PS_ma%d" % mass
config.General.workArea = 'GENSIM'
config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'PrivateMC'
#name of the python cmsRun config to run
if mass == 20 :
    config.JobType.psetName = 'HIG-RunIISummer15wmLHEGS-00157_1_cfg.py'
elif mass == 40 :
    config.JobType.psetName = 'HIG-RunIISummer15wmLHEGS-00161_1_cfg.py'
elif mass == 60 :
    config.JobType.psetName = 'HIG-RunIISummer15wmLHEGS-00165_1_cfg.py'
#config.JobType.inputFiles = ['GeneratorInterface/GenFilters/src/TopDecayFilter.cc', 'GeneratorInterface/GenFilters/python/TopDecayFilter_cfi.py','GeneratorInterface/GenFilters/python/interface/TopDecayFilter.h']
config.JobType.disableAutomaticOutputCollection = False
#settings below should be enough for 1000 events per job. would advice 800-1000 events per job (jobs will fail if you use too many)
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 2750

config.section_("Data")
#Name of the private campaign. It is going to be published with /outputPrimaryDataset/username-outputDatasetTag/
config.Data.outputPrimaryDataset = 'SUSYGluGluToHToAA_AToMuMu_AToBB_M-%d_TuneCUETP8M1_13TeV_madgraph_Herwigpp' % mass
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1000
config.Data.totalUnits = 200000
#publication on das under prod/phys03.
config.Data.publication = True
#second part of the sample name
config.Data.outputDatasetTag = 'PSHerwigpp'


config.section_("Site")
#site where you have your t2 account and grid storage
config.Site.storageSite = 'T2_CH_CERN'
#configure which sites to run on
config.Site.whitelist = ['T2_*', 'T1_*']

config.section_("User")
## only german users
