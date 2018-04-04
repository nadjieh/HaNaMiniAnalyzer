#include "Haamm/HaNaMiniAnalyzer/interface/METReader.h"

using namespace edm;
using namespace reco;

METReader::METReader( edm::ParameterSet const& iPS, edm::ConsumesCollector && iC , bool isData) :
  BaseEventReader< pat::METCollection >( iPS , &iC ),
  MetCut( iPS.getParameter<double>( "Cut" ) )
{
  ReadOldJets = false;
  Uncertainty = -1;
  if(!isData){
    if (iPS.exists( "oldjets" )){
      oldjetToken_= iC.consumes<pat::JetCollection>(iPS.getParameter<edm::InputTag>("oldjets")) ;
      ReadOldJets = true;
    }
    Uncertainty = iPS.getParameter< int> ("Uncertainty");
  }
  
  reRunMetSig = iPS.exists("metsig");
  if(iPS.exists("metsig")){
    metsigToken_ = iC.consumes<double>(iPS.getParameter<edm::InputTag>("metsig"));
  }
}

double METReader::Read( const edm::Event& iEvent , pat::JetCollection* newJets ){
  BaseEventReader< pat::METCollection >::Read( iEvent );
  const pat::MET &met_ = handle->front();
  if( Uncertainty < 0)
    met = met_.p4();
  else{
    met = met_.shiftedP4( pat::MET::METUncertainty(Uncertainty) );
  }
  
  if( newJets && ReadOldJets){
    iEvent.getByToken(oldjetToken_, oldjets);
    oldht = HT4( *oldjets );
    newht = HT4( *newJets );
    
    met -= ( newht - oldht ); 
  }
  //return (met.Pt() - MetCut)  
  metphi = met.Phi();
  return (met.Pt());
}

  
reco::Candidate::LorentzVector METReader::HT4( pat::JetCollection jets ){
  reco::Candidate::LorentzVector ret ;
  for( auto j : jets )
    ret += j.p4();
  return ret;
};

double METReader::ReadMetSig (const edm::Event& iEvent){
  /*iEvent.getByToken(metsigToken_, metsig);
  //Test for METSignificance
  double METSignificance_;
  if(metsig.failedToGet()) cout<< "Failed to get METSig"<<endl;
  //else cout<<"MetSig is: "<<*metsig << endl;
  METSignificance_ = metsig.failedToGet() ? -999. : *metsig;
  return METSignificance_;*/
  //BaseEventReader< pat::METCollection >::Read( iEvent );
  //const pat::MET &met_ = handle->front();
  //return met_.metSignificance();
  //END
  //
  //
  if( !reRunMetSig ){
    return handle->front().metSignificance(); 
  }
   iEvent.getByToken(metsigToken_, metsig);
  //Test for METSignificance
  //double METSignificance_;
  if(metsig.failedToGet()) cout<< "Failed to get METSig"<<endl;
  //METSignificance_ = metsig.failedToGet() ? -999. : *metsig;
  BaseEventReader< pat::METCollection >::Read( iEvent );
  const pat::MET &met_ = handle->front();
  //cout<<"Default MET: "<<met_.metSignificance() << ", METSig module: "<<METSignificance_<<endl;
  return met_.metSignificance();
}
