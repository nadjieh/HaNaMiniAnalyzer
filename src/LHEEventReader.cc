#include "Haamm/HaNaMiniAnalyzer/interface/LHEEventReader.h"

LHEEventReader::LHEEventReader( edm::ParameterSet const& iPS, edm::ConsumesCollector && iC) :
  BaseEventReader< LHEEventProduct >( iPS , &iC )
{
  
}

double LHEEventReader::Read( const edm::Event& iEvent ){
  BaseEventReader< LHEEventProduct >::Read( iEvent );
  WeightSign = (handle->hepeup().XWGTUP > 0) ? 1.0 : -1.0 ; 

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

  return WeightSign;
}
