#include "Haamm/HaNaMiniAnalyzer/interface/HLTReader.h"

#include <iostream>

using namespace edm;
using namespace std;

HLTReader::HLTReader( edm::ParameterSet const& iPS, edm::ConsumesCollector && iC) :
  BaseEventReader< TriggerResults >( iPS , &iC ),
  HLT_To_Or ( iPS.getParameter< vector<string> >("HLT_To_Or" ) ),
  PrintTrigNamesPerRun( iPS.getParameter< bool >("PrintTrigNamesPerRun") )
{
  latestRun = 0;
}

double HLTReader::Read( const edm::Event& iEvent ){
    BaseEventReader< TriggerResults >::Read( iEvent );
    const edm::TriggerNames& trigNames = iEvent.triggerNames(*handle);

    if( PrintTrigNamesPerRun )
      if( latestRun != iEvent.eventAuxiliary().run() ){
	latestRun = iEvent.eventAuxiliary().run();
	cout << "===========================================================" << endl;
	cout << "TriggerNames in Run Number # " << latestRun << endl;

	for(unsigned int i = 0 ; i < trigNames.size() ; i++)
	  cout << "\t" << trigNames.triggerName(i) << endl;
	
	cout << "===========================================================" << endl;
      }

    passTrig = (HLT_To_Or.size() == 0);
    for(auto hlt : HLT_To_Or){
      uint hltindex = trigNames.triggerIndex(hlt);
      if( hltindex < trigNames.size() )
	passTrig |= handle->accept(hltindex);
    }
    if( !passTrig )
      return -1.0;
    else
      return 1.0;
  }
