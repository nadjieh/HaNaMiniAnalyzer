#include <iostream>
#include "Haamm/HaNaMiniAnalyzer/interface/LHEEventReader.h"

LHEEventReader::LHEEventReader( edm::ParameterSet const& iPS, edm::ConsumesCollector && iC) :
  BaseEventReader< LHEEventProduct >( iPS , &iC )
{
  cutOnNGenJets = iPS.getUntrackedParameter<int>("cutOnNGenJets" , -1 );
}

double LHEEventReader::Read( const edm::Event& iEvent ){
  using namespace std;

  BaseEventReader< LHEEventProduct >::Read( iEvent );
  WeightSign = (handle->hepeup().XWGTUP > 0) ? 1.0 : -1.0 ; 

  //cout << "ww=" << handle->originalXWGTUP() << "--";
  //for(int i = 0 ; i < 9 ; i++)
  //  cout << "w" << i << "=" << handle->weights()[i].wgt << " -- " ;
  //cout << endl;
  scale_uu = handle->weights()[4].wgt/handle->originalXWGTUP();
  scale_dd = handle->weights()[8].wgt/handle->originalXWGTUP();


  NGenJets = 0 ;
  const lhef::HEPEUP& lheEvent = handle->hepeup();
  std::vector<lhef::HEPEUP::FiveVector> lheParticles = lheEvent.PUP;
  size_t numParticles = lheParticles.size();

  for ( size_t idxParticle = 0; idxParticle < numParticles; ++idxParticle ) {
    int absPdgId = TMath::Abs(lheEvent.IDUP[idxParticle]);
    int status = lheEvent.ISTUP[idxParticle];
    if (status == 1 && ((absPdgId >= 1 && absPdgId <= 6) || absPdgId == 21) ) { // quarks and gluons
      //lheHt += TMath::Sqrt(TMath::Power(lheParticles[idxParticle][0], 2.) + TMath::Power(lheParticles[idxParticle][1], 2.)); // first entry is px, second py
      ++NGenJets;
    }
  } 

  if( cutOnNGenJets > -1 )
    if( NGenJets != cutOnNGenJets )
      return 0.0 ;

  return WeightSign;
}
