import FWCore.ParameterSet.Config as cms

# link to card:
# https://github.com/cms-sw/genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/production/13TeV/higgs/ggh01_M125_Toa01a01_M60_Tomumubb

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.3.3/ggh01_M125_Toa01a01_M60_Tomumubb/v1/ggh01_M125_Toa01a01_M60_Tomumubb_tarball.tar.xz'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

from Configuration.Generator.HerwigppDefaults_cfi import *
from Configuration.Generator.HerwigppUE_EE_5C_cfi import *
from Configuration.Generator.HerwigppPDF_CTEQ6_LO_cfi import *# Import CTEQ6L PDF as shower pdf                                                                                                             
from Configuration.Generator.HerwigppEnergy_13TeV_cfi import *
from Configuration.Generator.HerwigppLHEFile_cfi import *
from Configuration.Generator.HerwigppMECorrections_cfi import *


generator = cms.EDFilter("ThePEGHadronizerFilter",
                         herwigDefaultsBlock,
                         herwigppUESettingsBlock,
                         herwigppPDFSettingsBlock,
                         herwigppEnergySettingsBlock,
                         herwigppLHEFileSettingsBlock,
                         herwigppMECorrectionsSettingsBlock,
         # PDF for hard subprocess                                                                                                                                                                         
                         hwpp_pdf_NNPDF30LO_Hard = cms.vstring(
                             'create ThePEG::LHAPDF /Herwig/Partons/cmsHardPDFSet ThePEGLHAPDF.so',          # cmsHardPDFSet Default name for hard subprocess PDF
                             'set /Herwig/Partons/cmsHardPDFSet:PDFName NNPDF30_lo_as_0130.LHgrid',
                             'set /Herwig/Partons/cmsHardPDFSet:RemnantHandler /Herwig/Partons/HadronRemnants'
                         ),
                         herwigNewPhysics = cms.vstring(
                             'cd /Herwig/Particles',
                             'create ThePEG::ParticleData a01',
                             'setup a01 36 a01 60.0 0.0 0.0 0.0 0 0 0 1',
                             'cd /'
                             ),
                         configFiles = cms.vstring(),
                         parameterSets = cms.vstring(
                             'hwpp_cmsDefaults',
                             'herwigNewPhysics',
                             'hwpp_ue_EE5C',
                             'hwpp_cm_13TeV',
                             'hwpp_pdf_CTEQ6L1',# Shower PDF matching with the tune                                                                                                                        
                             'hwpp_pdf_NNPDF30LO_Hard',# PDF of hard subprocess 
                             'hwpp_LHE_MadGraph_DifferentPDFs',### WARNING ### Use this option only with LO MadGraph5_aMC@NLO LHE files
                             'hwpp_MECorr_Off'# Switch off ME corrections while showering LHE files as recommended by Herwig++ authors
                             ),
                         dummyprocess = cms.vstring( ),
                         crossSection = cms.untracked.double(-1),
                         filterEfficiency = cms.untracked.double(1.0),
                         )
ProductionFilterSequence = cms.Sequence(generator)


