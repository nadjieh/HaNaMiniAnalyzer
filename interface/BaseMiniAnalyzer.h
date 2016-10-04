#ifndef BaseMiniAnalyzer_H
#define BaseMiniAnalyzer_H

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/ConsumesCollector.h"


#include "GenEventInfoProductReader.h"
#include "LHEEventReader.h"
#include "HLTReader.h"
#include "VertexReader.h"
#include "DiMuonReader.h"
#include "METReader.h"
#include "JetReader.h"


#include "Histograms.h"

//using namespace reco;
using namespace edm;
using namespace std;
//using namespace pat;

class BaseMiniAnalyzer : public edm::one::EDFilter<edm::one::SharedResources> {
public:
  explicit BaseMiniAnalyzer(const edm::ParameterSet&);
  ~BaseMiniAnalyzer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
protected:
  virtual void beginJob() override;
  virtual bool filter(edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;

  // ---------- Common variables needed for event analyzing in analyze method
  double W;
  double stepEventSelection;
  Histograms* hCutFlowTable;
  // --------- Common things to read from config file :
  string SetupDir;
  bool IsData;
  string SampleName;
  // --------- All Info needed in the event processing ---------------
  GenEventInfoProductReader* geninfoReader;
  LHEEventReader* LHEReader;
  HLTReader* hltReader_Mu17Mu8_DZ;
  HLTReader* hltReader_Mu17Mu8;
  VertexReader* vertexReader;
  METReader* metReader;
  DiMuonReader* diMuReader;
  JetReader* jetReader;

};

#endif

