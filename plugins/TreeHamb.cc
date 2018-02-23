#include "Haamm/HaNaMiniAnalyzer/interface/BaseMiniAnalyzer.h"
#include "TTree.h"
#include "TLorentzVector.h"
#include <iostream>

using namespace std;


class TreeHamb : public BaseMiniAnalyzer{
public:
  explicit TreeHamb(const edm::ParameterSet&);
  ~TreeHamb();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions){ BaseMiniAnalyzer::fillDescriptions( descriptions ); }




  // ----------member data ---------------------------

protected:
  virtual void beginJob() override;
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;
  unsigned int RunN;
  unsigned long long EventN;
  unsigned char nVertices;
  std::valarray<double> W;
  float* Weight;
  float puWeight, met , metPhi, metSig;
  float* bSelWeights;
  float nNonTagged;
  float nLooseNotMed;
  float nMedNotTight;
  float nTight;
  bool passHLT_Mu17Mu8;
  bool passHLT_Mu17Mu8_DZ;
  float hltWeight_Mu17Mu8;
  float hltWeight_Mu17Mu8_DZ;
  std::vector<float> jetsPt;
  std::vector<float> jetsE;
  std::vector<float> jetsEta;
  std::vector<float> jetsPhi;
  std::vector<float> jetsBtag;
  std::vector<float> jetsFlavour;

  std::vector<float> muPt;
  std::vector<float> muEta;
  std::vector<float> muPhi;
  std::vector<float> muIso;
  std::vector<float> muId;
  std::vector<bool> muCharge;
  std::vector<bool> muHLT;
  std::vector<float> muIsoChargedHadronPt;
  std::vector<float> muIsoNeutralHadronEt;
  std::vector<float> muIsoPhotonEt;
  std::vector<float> muPUPt;
  TTree* theSelectionResultTree;
  unsigned int nHistos;
  bool MakeTree,forOptimization;
  unsigned int EvtNumber;
  struct hltWeights{
    float mu17mu8, mu17mu8dz;
    hltWeights(double mu17mu8_ = 1.0, double mu17mu8dz_ =1.0){
      mu17mu8 = mu17mu8_;
      mu17mu8dz = mu17mu8dz_;
    };
    void set(double mu17mu8_ = 1.0, double mu17mu8dz_ =1.0){
      mu17mu8 = mu17mu8_;
      mu17mu8dz = mu17mu8dz_;
    };
  };
  struct particleinfo{
    float pt, eta, phi , mass, b1 , b2, w; 
    particleinfo( double pt_=-999, double eta_ =-999, double phi_=-999 , double mass_ = -999 , double b1_ = -999, double b2_ = -999, double W = 1. ){
      pt = pt_;
      eta= eta_;
      phi = phi_;
      mass = mass_;
      b1 = b1_;
      b2 = b2_;
      w = W;
    };
    void set( double pt_=-999, double eta_ =-999, double phi_=-999 , double mass_ = -999 , double b1_ = -999, double b2_ = -999, double W = 1. ){
      pt = pt_;
      eta= eta_;
      phi = phi_;
      mass = mass_;
      b1 = b1_;
      b2 = b2_;
      w = W;
    };
  };

  particleinfo aMu, aBjetPtOrdered, higgsjetPtOrdered, aBjetBtagOrdered, higgsjetBtagOrdered;
  hltWeights hltWs;
  // ---------- methods ---------------------------

  void FillTree(){
    if( !MakeTree )
      return;

    for(unsigned int i=0 ; i < nHistos ; i++)
      Weight[i] = W[i];

    theSelectionResultTree->Fill();
  }

  void resetTreeVals(){
    RunN = 0;
    EventN = 0;
    nVertices = 250;

    W = 1.0;
    for(unsigned int i=0 ; i < nHistos ; i++)
      Weight[i] = 1.0 ;

    for(unsigned int i=0 ; i < 9 ; i++)
      bSelWeights[i] = 0.0;

    puWeight = met = metPhi = metSig = -999;

    passHLT_Mu17Mu8 = passHLT_Mu17Mu8_DZ = true;

    hltWeight_Mu17Mu8 = hltWeight_Mu17Mu8_DZ = 1.0;

    jetsPt.clear();
    jetsEta.clear();
    jetsE.clear();
    jetsPhi.clear();
    jetsBtag.clear();
    jetsFlavour.clear();

    muPt.clear();
    muEta.clear();
    muPhi.clear();
    muIso.clear();
    muId.clear();
    muCharge.clear();
    muHLT.clear();
    muIsoChargedHadronPt.clear();
    muIsoNeutralHadronEt.clear();
    muIsoPhotonEt.clear();
    muPUPt.clear();
    particleinfo tmp;
    aMu = aBjetPtOrdered =  higgsjetPtOrdered = aBjetBtagOrdered = higgsjetBtagOrdered = tmp ;
    hltWeights tmp2;
    hltWs = tmp2;
  }
};

DEFINE_FWK_MODULE(TreeHamb);





TreeHamb::~TreeHamb() {}
TreeHamb::TreeHamb( const edm::ParameterSet& ps ) :
  BaseMiniAnalyzer( ps ), 
  theSelectionResultTree( NULL ),
  nHistos(1),
  MakeTree( ps.getParameter<bool>( "StoreEventNumbers" ))
{
  if(ps.getUntrackedParameter<bool>("forOptimization"))
	forOptimization = ps.getUntrackedParameter<bool>("forOptimization");
  else 
	forOptimization = false;
}


// ------------ method called once each job just before starting event loop  ------------
void TreeHamb::beginJob()
{
  if( SampleName == "Signal" )
    nHistos = 51;
  W = std::valarray<double>( 1.0 , nHistos);
  Weight = new float[nHistos];

  bSelWeights = new float[9];

  if( MakeTree ){
    edm::Service<TFileService> fs;
    TFileDirectory treeDir = fs->mkdir( "Trees" );
    theSelectionResultTree = treeDir.make<TTree>("Events" , "Events"); 
    theSelectionResultTree->Branch("EventNumber", &EventN );
    theSelectionResultTree->Branch("RunNumber", &RunN );
    //theSelectionResultTree->Branch("SelectionStep", &SelectionStep );

    std::string weightLeafList = "W0";
    for(unsigned int iii = 1 ; iii < nHistos ; iii++)
      weightLeafList += (":W" + std::to_string(iii) );
    if(!forOptimization){//for optimization we use a lighter version of the tree
        theSelectionResultTree->Branch("nVertices" , &nVertices);
	theSelectionResultTree->Branch("Weight", Weight , weightLeafList.c_str() );
	theSelectionResultTree->Branch("puWeight", &puWeight);
	theSelectionResultTree->Branch("bWs", bSelWeights , "W1L:W1M:W1T:W1L1M:W1L1T:W1M1T:W2L:W2M:W2T");
	theSelectionResultTree->Branch("hltWeights", &hltWs , "mu17mu8:mu17mu8dz");
        theSelectionResultTree->Branch("metPhi", &metPhi);
        theSelectionResultTree->Branch("passHLT_Mu17Mu8", &passHLT_Mu17Mu8);
        theSelectionResultTree->Branch("passHLT_Mu17Mu8_DZ", &passHLT_Mu17Mu8_DZ);
        theSelectionResultTree->Branch("hltWeight_Mu17Mu8", &hltWeight_Mu17Mu8);
        theSelectionResultTree->Branch("hltWeight_Mu17Mu8_DZ", &hltWeight_Mu17Mu8_DZ);
        theSelectionResultTree->Branch("aMu" , &aMu , "pt:eta:phi:mass:b1:b2:w");
        theSelectionResultTree->Branch("aBjetPtOrdered" , &aBjetPtOrdered , "pt:eta:phi:mass:b1:b2:w");
        theSelectionResultTree->Branch("higgsjetPtOrdered", &higgsjetPtOrdered , "pt:eta:phi:mass:b1:b2:w");
    }

    if(diMuReader->SignalStudy()){
    	theSelectionResultTree->Branch("muIsoChargedHadronPt",(&muIsoChargedHadronPt));
    	theSelectionResultTree->Branch("muIsoNeutralHadronEt",(&muIsoNeutralHadronEt));
    	theSelectionResultTree->Branch("muIsoPhotonEt",(&muIsoPhotonEt));
    	theSelectionResultTree->Branch("muPUPt",(&muPUPt));
    }

    theSelectionResultTree->Branch("met", &met);
    theSelectionResultTree->Branch("metSig", &metSig);

    theSelectionResultTree->Branch("jetsPt", (&jetsPt));
    theSelectionResultTree->Branch("jetsEta", (&jetsEta));
    theSelectionResultTree->Branch("jetsE", (&jetsE));
    theSelectionResultTree->Branch("jetsPhi", (&jetsPhi));
    theSelectionResultTree->Branch("jetsBtag", (&jetsBtag));
    theSelectionResultTree->Branch("jetsFlavour", (&jetsFlavour));

    theSelectionResultTree->Branch("nNonTagged", &nNonTagged);
    theSelectionResultTree->Branch("nLooseNotMed", &nLooseNotMed);
    theSelectionResultTree->Branch("nMedNotTight", &nMedNotTight);
    theSelectionResultTree->Branch("nTight", &nTight);

    theSelectionResultTree->Branch("muPt", (&muPt));
    theSelectionResultTree->Branch("muEta", (&muEta));
    theSelectionResultTree->Branch("muPhi", (&muPhi));
    theSelectionResultTree->Branch("muIso", (&muIso));
    theSelectionResultTree->Branch("muId", (&muId));
    theSelectionResultTree->Branch("muCharge", (&muCharge));
    theSelectionResultTree->Branch("muHLT", (&muHLT));


    resetTreeVals();
  }

  hCutFlowTable = new Histograms( SampleName , "CutFlowTable" , 10 , 0.5 , 10.5, nHistos );
  EvtNumber = 0;
}

//
bool TreeHamb::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  EvtNumber++;
  //cout<<"-------------- "<<EvtNumber<<endl;
  resetTreeVals();

  EventN = iEvent.eventAuxiliary().event() ;
  RunN = iEvent.eventAuxiliary().run() ;


  
  if( nHistos > 1 && SampleName == "Signal" ) {
    LHEReader->Read( iEvent );
    //W = LHEReader->ExtractWeightsInRange( 446 , 495 ); // To be checked for HiggsExo
  }

  stepEventSelection = 0;

  if( geninfoReader )
    W *= geninfoReader->Read( iEvent );
  hCutFlowTable->Fill( ++stepEventSelection , W );

//---------- HLT --------
// Currently no HLT in MC
//if(IsData){
 passHLT_Mu17Mu8 = (!( hltReader_Mu17Mu8->Read( iEvent ) < 0 ));
 passHLT_Mu17Mu8_DZ = (!( hltReader_Mu17Mu8_DZ->Read( iEvent ) < 0 ));
    //  } 
  
  hCutFlowTable->Fill( ++stepEventSelection , W );
//---------- PV --------
  if( vertexReader->Read( iEvent ) < 0 ){
    return false;
  }
  W *= vertexReader->puWeight;
  puWeight = vertexReader->puWeight;
  nVertices = vertexReader->vtxMult;
  hCutFlowTable->Fill( ++stepEventSelection , W );

  //cout<<"Before met "<<endl;
  //To be checked whether corrections are needed?
  met = metReader->Read(iEvent);
  metSig = metReader->ReadMetSig(iEvent);
  //cout<<"In tree maker, metSig: "<<metSig<<endl;
  metPhi = metReader->metphi;

  //cout<<"Before dimu "<<endl;
  DiMuonReader::SelectionStatus myDimuStat = diMuReader->Read( iEvent , vertexReader->PV() );

  //cout<<"After myDim "<<endl;
  for(unsigned int iMu = 0; iMu < diMuReader->goodMus.size(); iMu++){
    muPt.push_back(diMuReader->goodMus[iMu].pt());
    muEta.push_back(diMuReader->goodMus[iMu].eta());
    muPhi.push_back(diMuReader->goodMus[iMu].phi());
    muIso.push_back(diMuReader->goodMuIso[iMu]);
    muId.push_back(diMuReader->goodMuId[iMu]);
    if(diMuReader->SignalStudy()){
	muIsoChargedHadronPt.push_back(diMuReader->goodMuIsoChargedHadronPt[iMu]);
    	muIsoNeutralHadronEt.push_back(diMuReader->goodMuIsoNeutralHadronEt[iMu]);
    	muIsoPhotonEt.push_back(diMuReader->goodMuIsoPhotonEt[iMu]);
    	muPUPt.push_back(diMuReader->goodMuIsoPUPt[iMu]);
    }
    muCharge.push_back((diMuReader->goodMus[iMu].charge() > 0));
    //cout << "---- Muon "<<iMu<<" Charge: "<<diMuReader->goodMus[iMu].charge()<<",\tSign: "<<(diMuReader->goodMus[iMu].charge() > 0)<<endl;
    //cout<<diMuReader->goodMus[iMu].charge() <<"\t"<< muCharge[muCharge.size()-1]<<endl;
    muHLT.push_back(0);	// To be completed
  }
  
  //cout<<"------ OS muons: "<<diMuReader->goodMusOS.size()<<endl;
  TLorentzVector amu;
  if(diMuReader->goodMusOS.size() > 1){
	//cout<<"It has 2 OS muons!"<<endl;
  	amu.SetPxPyPzE(diMuReader->goodMusOS[0].px()+diMuReader->goodMusOS[1].px(),
		     diMuReader->goodMusOS[0].py()+diMuReader->goodMusOS[1].py(),
		     diMuReader->goodMusOS[0].pz()+diMuReader->goodMusOS[1].pz(),
		     diMuReader->goodMusOS[0].energy()+diMuReader->goodMusOS[1].energy());
	//cout<<"amu is set!"<<endl;
  	aMu.set(amu.Pt(), amu.Eta(), amu.Phi(), amu.M());
	//cout<<"aMu is set!"<<endl;
        if(!IsData)
	   hltWs.set(diMuReader->MuonSFHltMu17Mu8(diMuReader->goodMusOS[0].pt(),diMuReader->goodMusOS[1].pt()),
		  diMuReader->MuonSFHltMu17Mu8_DZ(diMuReader->goodMusOS[0].pt(),diMuReader->goodMusOS[1].pt()));
	//cout<<"hltW is set"<<endl;
  }

  //cout<<"before mu selection "<<endl;

  switch( myDimuStat ){
  case DiMuonReader::Pass:
    W *= (diMuReader->W) ;// No HLT!
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    hCutFlowTable->Fill( ++stepEventSelection , W );
    break;
  case DiMuonReader::UnderTheZPeak:
    W *= (diMuReader->W) ;
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiMuonReader::LowMassPair:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiMuonReader::NoPairWithChargeReq:
    hCutFlowTable->Fill( ++stepEventSelection , W );
  case DiMuonReader::LessThan2Muons:
    //if(!forOptimization)
    //    FillTree();
    return false;
  }
  /*cout <<"++++++++++++++ In tree Maker +++++++++++++++++++++"<<endl;
  cout <<"++++ Iso: "<<muIso[0]<<",\t"<<muIso[1]<<endl;	 
  if(diMuReader->SignalStudy()){
      cout <<"++++ chargedIso 0: "<<muIsoChargedHadronPt[0]<<",\tchargedIso 1: "<<muIsoChargedHadronPt[1]<<endl;
      cout <<"++++ neutralIso 0: "<<muIsoNeutralHadronEt[0]<<",\tneutralIso 1: "<<muIsoNeutralHadronEt[1]<<endl;
      cout <<"++++ photonIso 0: "<<muIsoPhotonEt[0]<<",\tphotonIso 1: "<<muIsoPhotonEt[1]<<endl;
      cout <<"++++ pilupIso 0: "<<muPUPt[0]<<",\tpileupIso 1: "<<muPUPt[1]<<endl;
  }
  cout <<"++++++++++++++++++++++++++++++++++++++++++++++++++"<<endl; */
  //cout<<"Before Jet "<<endl;
  JetReader::SelectionStatus myJetsStat = jetReader->Read( iEvent , &(diMuReader->DiMuon) );
  for(unsigned int iJet = 0; iJet < jetReader->selectedJets.size(); iJet++){
    jetsPt.push_back(jetReader->selectedJets[iJet].pt());
    jetsEta.push_back(jetReader->selectedJets[iJet].eta());
    jetsE.push_back(jetReader->selectedJets[iJet].energy());
    jetsPhi.push_back(jetReader->selectedJets[iJet].phi());
    jetsBtag.push_back(jetReader->selectedJets[iJet].bDiscriminator(jetReader->BTagAlgo));
    if(!IsData)
	jetsFlavour.push_back(jetReader->selectedJets[iJet].hadronFlavour());
  }

  for(int i = 0; i < 9; i++){
	bSelWeights[i] = jetReader->weights[i];
  }

  nTight = jetReader->nTight;
  nMedNotTight = jetReader->nMedNotTight;
  nLooseNotMed = jetReader->nLooseNotMed;
  nNonTagged = jetReader->nNonTagged;

  if(jetReader->selectedJets.size() > 1){
	//di-b-jet pt-ordered
	TLorentzVector tmp(jetReader->selectedJets[0].px()+jetReader->selectedJets[1].px(),
			   jetReader->selectedJets[0].py()+jetReader->selectedJets[1].py(),
			   jetReader->selectedJets[0].pz()+jetReader->selectedJets[1].pz(),
			   jetReader->selectedJets[0].energy()+jetReader->selectedJets[1].energy());

	aBjetPtOrdered.set(tmp.Pt(), tmp.Eta(), tmp.Phi(), tmp.M(), 
			   jetReader->selectedJets[0].bDiscriminator(jetReader->BTagAlgo), 
			   jetReader->selectedJets[1].bDiscriminator(jetReader->BTagAlgo));

	//making the higgs with pt-ordered
	tmp.SetPxPyPzE(tmp.Px()+amu.Px(), tmp.Py()+amu.Py(), tmp.Pz()+amu.Pz(), tmp.E()+amu.E());
	higgsjetPtOrdered.set(tmp.Pt(), tmp.Eta(), tmp.Phi(), tmp.M());

  }

  switch( myJetsStat ){
  case JetReader::Pass:
    hCutFlowTable->Fill( ++stepEventSelection , W );
    //W *= jetReader->W ;
    hCutFlowTable->Fill( ++stepEventSelection , W );
    break;
  case JetReader::NotEnoughBJets:
    hCutFlowTable->Fill( ++stepEventSelection , W );
    if (!diMuReader->SignalStudy())
	return false;
  case JetReader::NotEnoughJets:
    //FillTree();
    if(diMuReader->SignalStudy()){
	FillTree();
    }
    return false;
  }
  //cout<< "PASSED ---------------------------------"<<endl;
  FillTree();
  return true;
}
