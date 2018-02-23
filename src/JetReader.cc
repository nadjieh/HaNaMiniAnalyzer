#include "Haamm/HaNaMiniAnalyzer/interface/JetReader.h"


JetReader::JetReader( edm::ParameterSet const& iConfig, edm::ConsumesCollector && iC, bool isData , string SetupDir) :
  BaseEventReader< pat::JetCollection >( iConfig , &iC ),
  unc (iConfig.getParameter<int> ("JECUncertainty")),
  jerunc (iConfig.getParameter<int> ("JERUncertainty")),
  btagunc (iConfig.getParameter<int> ("BTagUncertainty")),
  IsData( isData ),
  ApplyJER( iConfig.getParameter<bool>( "ApplyJER" ) ),
  JetPtCut( iConfig.getParameter<double>( "JetPtCut" ) ),
  JetEtaCut( iConfig.getParameter<double>( "JetEtaCut" ) ),
  MinNJets( iConfig.getParameter<unsigned int>( "MinNJets" ) ),
  BTagWPL( iConfig.getParameter<double>( "BTagWPL" ) ),
  BTagWPM( iConfig.getParameter<double>( "BTagWPM" ) ),
  BTagWPT( iConfig.getParameter<double>( "BTagWPT" ) ),
  BTagAlgo( iConfig.getParameter<string>( "BTagAlgo" ) ),
  MinNBJets( iConfig.getParameter<unsigned int>( "MinNBJets" ) ),
  MaxNBJets( iConfig.getParameter<int>( "MaxNBJets" ) ),
  rndJER(new TRandom3( 13611360 ) )
{

 
  BTagCuts = iConfig.getParameter<std::vector<int> > ( "BTagCuts" );
  if(BTagCuts.size() > 2){
    std::cout<<"FATAL ERROR: The current code accepts up to two WP's, one for selection one for veto"<<std::endl;
    return;
  } else if(BTagCuts.size() < 2) 
    BTagCuts.push_back(-1);  
  if( !IsData ){
    //btw1L
    weighters.push_back(new BTagWeight("CSVv2", 0 , SetupDir, 1 , -1 , BTagWPL, BTagWPM, BTagWPT,-1,btagunc)); 
    //btw1M
    weighters.push_back(new BTagWeight("CSVv2", 1 , SetupDir, 1 , -1 , BTagWPL, BTagWPM, BTagWPT,-1,btagunc));
    //btw1T
    weighters.push_back(new BTagWeight("CSVv2", 2 , SetupDir, 1 , -1 , BTagWPL, BTagWPM, BTagWPT,-1,btagunc));
    //btw1M1L
    weighters.push_back(new BTagWeight("CSVv2", 1, SetupDir, 1, -1, BTagWPL, BTagWPM, BTagWPT, 0, btagunc, 1, -1));
    //btw1T1L
    weighters.push_back(new BTagWeight("CSVv2", 2, SetupDir, 1, -1, BTagWPL, BTagWPM, BTagWPT, 0, btagunc, 1, -1));
    //btw1T1M
    weighters.push_back(new BTagWeight("CSVv2", 2, SetupDir, 1, -1, BTagWPL, BTagWPM, BTagWPT, 1, btagunc, 1, -1));
    //btw2L
    weighters.push_back(new BTagWeight("CSVv2", 0 , SetupDir, 2 , 2 , BTagWPL, BTagWPM, BTagWPT,-1,btagunc));
    //btw2M
    weighters.push_back(new BTagWeight("CSVv2", 1 , SetupDir, 2 , 2 , BTagWPL, BTagWPM, BTagWPT,-1,btagunc));
    //btw2T
    weighters.push_back(new BTagWeight("CSVv2", 2 , SetupDir, 2 , 2 , BTagWPL, BTagWPM, BTagWPT,-1,btagunc));


    t_Rho_ = (iC.consumes<double>( edm::InputTag( "fixedGridRhoFastjetAll" ) ) );
    resolution = JME::JetResolution( SetupDir + "/MCJetPtResolution.txt" );
    resolution_sf = JME::JetResolutionScaleFactor(SetupDir + "/MCJetSF.txt");

    //For JEC uncertainties
    jecUnc = new JetCorrectionUncertainty(SetupDir + "/JECUncertainties.txt");
  }
}

const pat::JetCollection* JetReader::GetAllJets(){
  return handle.product() ;
}


JetReader::SelectionStatus JetReader::Read( const edm::Event& iEvent , pat::DiObjectProxy* diLepton ){
  BaseEventReader< pat::JetCollection >::Read( iEvent );
  for(int iComb = 0; iComb < 9; iComb++)
	weights[iComb] = 1.;

  if( (!IsData) && ApplyJER ){
    iEvent.getByToken(t_Rho_ ,rho);
    Rho = *rho;
  }


  selectedJets.clear();
  selectedBJets.clear();
  selectedJetsSortedByB.clear();


  nNonTagged = 0;
  nLooseNotMed = 0;
  nMedNotTight = 0;
  nTight = 0;

  for ( pat::Jet j : *handle) {
    if( !IsData && ApplyJER ){
      float pt = JER(j , Rho);
      reco::Candidate::LorentzVector tmp(j.p4());
      tmp.SetPx( tmp.X()*pt/tmp.Pt() );
      tmp.SetPy( tmp.Y()*pt/tmp.Pt() );
      j.setP4(tmp);
    }
    double jetPt = j.pt();
    if (!IsData && unc != 0 ){
      jecUnc->setJetEta(j.eta());
      jecUnc->setJetPt(j.pt()); // here you must use the CORRECTED jet pt
      double uncVal = jecUnc->getUncertainty(true);
      jetPt = jetPt * (1+uncVal*unc) ; // unc = +1(up), or -1(down)
    }
    if (jetPt < JetPtCut) continue;
    if ( fabs(j.eta() ) > JetEtaCut ) continue;
    if ( !JetLooseID( j ) ) continue;
    if( diLepton ){
      double dr0 = reco::deltaR( j.p4() , diLepton->cand1().p4() );
      double dr1 = reco::deltaR( j.p4() , diLepton->cand2().p4() );
      if( dr0 < 0.4 || dr1 < 0.4 ) continue ;
    }

    selectedJets.push_back(j);
    selectedJetsSortedByB.push_back(j);
 
    float btagval = j.bDiscriminator( BTagAlgo );

   if(btagval < BTagWPL) nNonTagged++;
   else if(btagval < BTagWPM) nLooseNotMed++;
   else if(btagval < BTagWPT) nMedNotTight++;
   else nTight++;

    if(BTagCuts[0] == 0) {
      if(btagval > BTagWPL) selectedBJets.push_back(j);
    } else if (BTagCuts[0] == 1) {
      if(btagval > BTagWPM) selectedBJets.push_back(j);
    } else if (BTagCuts[0] == 2) {
      if(btagval > BTagWPT) selectedBJets.push_back(j);
    } else
	selectedBJets.push_back(j);
  }
  
  ptSort<pat::Jet> mySort; 
  std::sort(selectedJets.begin(),selectedJets.end(),mySort);
  std::sort(selectedBJets.begin(),selectedBJets.end(),mySort);
  btagSort<pat::Jet> myBsort(BTagAlgo);
  std::sort(selectedJetsSortedByB.begin(),selectedJetsSortedByB.end(),myBsort);
    
  if( selectedJets.size() < MinNJets ) return JetReader::NotEnoughJets ;
  if(  selectedBJets.size() < MinNBJets ) return JetReader::NotEnoughBJets;
  if(!IsData){
    for(int iComb = 0; iComb < 9; iComb++)
	if(iComb < 3 || iComb > 5){
		//cout<<"-- "<<iComb <<", weight"<<endl;
		weights[iComb] = weighters[iComb]->weight(selectedJets);
	} else {
		//cout<<"-- "<<iComb <<", weightExclusive"<<endl;
		weights[iComb] = weighters[iComb]->weightExclusive(selectedJets);
	}
  }
  return JetReader::Pass;
}

float JetReader::JER( pat::Jet jet , double rho , int syst ){
  JME::JetParameters parameters_1;
  parameters_1.setJetPt(jet.pt());
  parameters_1.setJetEta(jet.eta());
  parameters_1.setRho( rho );
  float sf = resolution_sf.getScaleFactor(parameters_1,Variation(jerunc));

  const reco::GenJet*  genjet =  jet.genJet ();
  float ret = jet.pt();
  if( genjet != NULL && genjet->pt() > 0 ){
    ret = max(0., genjet->pt() + sf*( jet.pt() - genjet->pt() ) );
  }else{
    float r = resolution.getResolution(parameters_1);
    ret = rndJER->Gaus( jet.pt() , r*sqrt( sf*sf - 1) );
  }
  return ret;
}

bool JetReader::JetLooseID( pat::Jet j ){
  float NHF = j.neutralHadronEnergyFraction ();
  float NEMF = j.neutralEmEnergyFraction ();
  int NumConst = j.numberOfDaughters ();
  float eta = j.eta();
  float CHF = j.chargedHadronEnergyFraction ( ) ;
  float CHM = j.chargedMultiplicity ();
  float CEMF = j.chargedEmEnergyFraction ();
  int NumNeutralParticle = j.neutralMultiplicity ( );
  bool looseJetID1 = (NHF<0.99 && NEMF<0.99 && NumConst>1) && ((abs(eta)<=2.4 && CHF>0 && CHM>0 && CEMF<0.99) || abs(eta)>2.4) && abs(eta)<=3.0 ;
  bool looseJetID2 = (NEMF<0.90 && NumNeutralParticle>10 && abs(eta)>3.0 ) ;
  
  return looseJetID1 || looseJetID2 ;
}
