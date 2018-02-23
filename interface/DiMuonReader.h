#ifndef DiMuonReader_H
#define DiMuonReader_H

#include "BaseEventReader.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "PhysicsTools/PatUtils/interface/PATDiObjectProxy.h"

#include "TH2.h"
#include "TROOT.h"
#include "TFile.h"
#include "TDirectory.h"
#include "TGraphAsymmErrors.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

using namespace edm;
using namespace pat;

class Isolation{
public:
        Isolation(TString Name):name(Name){
		edm::Service<TFileService> fs;
    		TFileDirectory subDir = fs->mkdir( name.Data() );
		
                iso = subDir.make<TH1D>(name+"_iso","iso", 500, 0,5);
                charged = subDir.make<TH1D>(name+"_charged","charged",500,0,5);
                neutral = subDir.make<TH1D>(name+"_neutral","neutral",500,0,5);
                photon = subDir.make<TH1D>(name+"_photon","photon",500,0,5);
                pileup = subDir.make<TH1D>(name+"_pileup","pileup",500,0,5);
        }
        ~Isolation(){
        }
        void Fill(reco::MuonPFIsolation Iso, double pt){
		double reliso = (Iso.sumChargedHadronPt+TMath::Max(0.,Iso.sumNeutralHadronEt+Iso.sumPhotonEt-0.5*Iso.sumPUPt))/pt;
		//cout <<"*************** In Isolation class *****"<<endl;
		iso->Fill(reliso);
		//cout<<"*** reliso: "<<reliso<<endl;
		charged->Fill(Iso.sumChargedHadronPt/pt);
		//cout<<"*** charged: "<<Iso.sumNeutralHadronEt<<endl;
		neutral->Fill(Iso.sumNeutralHadronEt/pt);
		//cout<<"*** neutral: "<<Iso.sumNeutralHadronEt<<endl;
		photon->Fill(Iso.sumPhotonEt/pt);
		//cout<<"*** photon: "<<Iso.sumPhotonEt<<endl;
		pileup->Fill(Iso.sumPUPt/pt);
		//cout<<"*** pileup: "<<Iso.sumPUPt<<endl;
		//cout <<"****************************************"<<endl;
	}
	TString name;
        TH1D * iso;
        TH1D * charged;
        TH1D * neutral;
        TH1D * photon;
        TH1D * pileup;
};



class DiMuonReader : public BaseEventReader< pat::MuonCollection > {
public:
  DiMuonReader( edm::ParameterSet const& iConfig, edm::ConsumesCollector && iC , bool isData , string SetupDir);
  enum SelectionStatus{
    LessThan2Muons,
    NoPairWithChargeReq,
    LowMassPair,
    UnderTheZPeak,
    Pass
  };
  SelectionStatus Read( const edm::Event& iEvent, const reco::Vertex* PV );
  Isolation * myIso;
  pat::MuonCollection goodMus;
  pat::MuonCollection goodMusOS;
  pat::DiObjectProxy DiMuon;
  double W;

  std::vector<float> goodMuId;
  std::vector<float> goodMuIso;

  std::vector<float> goodMuIsoChargedHadronPt;
  std::vector<float> goodMuIsoNeutralHadronEt;
  std::vector<float> goodMuIsoPhotonEt;
  std::vector<float> goodMuIsoPUPt;
  inline bool SignalStudy(){
	return isSignalStudy;
  }
private :
  /* MUON SF TOOLS */
  double MuonSFMedium( double etaL , double ptL , double etaSL , double ptSL );
  double MuonSFLoose( double etaL , double ptL , double etaSL , double ptSL );
  double MuonTrkEff(double abseta);
public:
  double MuonSFHltMu17Mu8( double ptL , double ptSL );
  double MuonSFHltMu17Mu8_DZ( double ptL , double ptSL );
  double MuonSFHltEta( double eta1 , double eta2 );
private:
  int uncert;
  TH2* hMuSFID;
  TH2* hMuSFIso;
  TH2* hMuHltMu17Mu8;
  TH2* hMuHltMu17Mu8_DZ;
  TGraphAsymmErrors* hTrk;
  /* MUON SF TOOLS */

  /* MUON SELECTION PARAMS */
  double MuonLeadingPtCut, MuonSubLeadingPtCut , MuonIsoCut, MuonEtaCut , DiMuLowMassCut, DiMuZMassWindow ;
  int MuonID , DiMuCharge;
  bool IsData, isHamb, isSignalStudy;
  /* MUON SELECTION PARAMS */


};
#endif
