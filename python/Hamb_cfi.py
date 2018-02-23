import FWCore.ParameterSet.Config as cms
Hamb = cms.EDFilter('TreeHamb',
                     LHE = cms.PSet ( useLHEW = cms.bool( False ),
                                      Input = cms.InputTag("externalLHEProducer")
                                      ),

                     HLT_Mu17Mu8 = cms.PSet( Input = cms.InputTag( "TriggerResults","","HLT" ), 
                                     HLT_To_Or = cms.vstring()
                                     ),
                     HLT_Mu17Mu8_DZ = cms.PSet( Input = cms.InputTag( "TriggerResults","","HLT" ), 
                                     HLT_To_Or = cms.vstring()
                                     ),
                     Vertex = cms.PSet( Input = cms.InputTag( "offlineSlimmedPrimaryVertices" ),
                                        pileupSrc = cms.InputTag("slimmedAddPileupInfo"),
                                        PUDataFileName = cms.InputTag("pileUpData.root")
                                        ),
                     DiMuon = cms.PSet( Input = cms.InputTag("slimmedMuons"),
                                        MuonLeadingPtCut = cms.double(24),
                                        MuonSubLeadingPtCut = cms.double(9),
                                        MuonIsoCut = cms.double( 0.15 ),
                                        MuonEtaCut = cms.double( 2.4 ),
                                        DiMuLowMassCut = cms.double(15  ),#Remove the dimu lower bound
                                        DiMuCharge = cms.int32( -1 ),
                                        MuonID = cms.int32( 3 ), #0:no id, 1:Loose , 2:Medium , 3:tight , 4 : soft
                                        DiMuZMassWindow = cms.double( 70 ), #Remove the dimu upper bound
					isHamb = cms.bool(True),
					isSignalStudy = cms.bool(False),
                                        HLTUnc = cms.int32(0)
                                        ),

                     MET = cms.PSet( Input = cms.InputTag("slimmedMETs"),
                                     Cut = cms.double( 40. ),
                                     Uncertainty = cms.int(-1)
                                     #http://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_8_4_0_patch2/doc/html/db/deb/classpat_1_1MET.html#a5c8ea7c9575730bedb6f1639140a7422
                                     #enum  	METUncertainty {
                                     #   JetResUp =0, JetResDown =1, JetEnUp =2, JetEnDown =3,
                                     #   MuonEnUp =4, MuonEnDown =5, ElectronEnUp =6, ElectronEnDown =7,
                                     #   TauEnUp =8, TauEnDown =9, UnclusteredEnUp =10, UnclusteredEnDown =11,
                                     #   PhotonEnUp =12, PhotonEnDown =13, NoShift =14, METUncertaintySize =15,
                                     #   JetResUpSmear =16, JetResDownSmear =17, METFullUncertaintySize =18
                                     # }
                                     #oldjets = cms.InputTag("slimmedJets"),
				     #metsig = cms.InputTag("METSignificance:METSignificance:HaNa")	
                                     ),
                     Jets = cms.PSet( Input = cms.InputTag("slimmedJets"),
                                      ApplyJER = cms.bool( False ),
                                      JECUncertainty = cms.int32(0),
                                      JERUncertainty = cms.int32(0),
                                      JetPtCut = cms.double( 15. ),
                                      JetEtaCut = cms.double( 2.4 ),
                                      BTagAlgo = cms.string("pfCombinedInclusiveSecondaryVertexV2BJetTags"),
                                      BTagWPL = cms.double(  0.5426  ),
                                      BTagWPM = cms.double(  0.8484  ),
                                      BTagWPT = cms.double(  0.9535 ),
                                      #Which WP to use in selection: 0,1,2 ---> L, M, T
                                      # -1 ---> no requirement
                                      BTagCuts = cms.vint32(1,-1), # supporting up to two working point, the second is for veto
                                      BTagUncertainty = cms.int32(0),

                                      MinNJets = cms.uint32( 2 ),
                                      MinNBJets = cms.uint32( 2 ),
				      MaxNBJets = cms.int32( -1 )
                                      ),
                     
                     sample = cms.string("WJetsMG"),
                     isData = cms.bool( False ),
                     SetupDir = cms.string("Setup80"),
		     		 StoreEventNumbers = cms.bool( True ),
		     		 forOptimization = cms.untracked.bool(False)
                     )
