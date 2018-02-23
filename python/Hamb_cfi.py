import FWCore.ParameterSet.Config as cms
Hamb = cms.EDFilter('TreeHamb',
                     LHE = cms.PSet ( useLHEW = cms.bool( False ),
                                      Input = cms.InputTag("externalLHEProducer")
                                      ),

                     HLT_Mu17Mu8 = cms.PSet( Input = cms.InputTag( "TriggerResults","","HLT" ), 
                                     HLT_To_Or = cms.vstring(),
                                             PrintTrigNamesPerRun = cms.bool( False )
                                     ),
                     HLT_Mu17Mu8_DZ = cms.PSet( Input = cms.InputTag( "TriggerResults","","HLT" ), 
                                     HLT_To_Or = cms.vstring(),
                                                PrintTrigNamesPerRun = cms.bool( False )
                                     ),
                     Vertex = cms.PSet( Input = cms.InputTag( "offlineSlimmedPrimaryVertices" ),
                                        pileupSrc = cms.InputTag("slimmedAddPileupInfo")
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
					isSignalStudy = cms.bool(False)
                                        ),

                     MET = cms.PSet( Input = cms.InputTag("slimmedMETs"),
                                     Cut = cms.double( 40. ),
                                     
                                     #oldjets = cms.InputTag("slimmedJets"),
				     #metsig = cms.InputTag("METSignificance:METSignificance:HaNa")	
                                     ),
                     Jets = cms.PSet( Input = cms.InputTag("slimmedJets"),
                                      ApplyJER = cms.bool( False ),
                                      JetPtCut = cms.double( 15. ),
                                      JetEtaCut = cms.double( 2.4 ),
                                      BTagAlgo = cms.string("pfCombinedInclusiveSecondaryVertexV2BJetTags"),
                                      BTagWPL = cms.double(  0.5426  ),
                                      BTagWPM = cms.double(  0.8484  ),
                                      BTagWPT = cms.double(  0.9535 ),
                                      #Which WP to use in selection: 0,1,2 ---> L, M, T
                                      # -1 ---> no requirement
                                      BTagCuts = cms.vint32(1,-1), # supporting up to two working point, the second is for veto

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
