/* 
 * File:   TemplateFit.C
 * Author: nadjieh
 *
 * Created on June 9, 2012, 3:57 PM
 */

#include<iostream>
#include "TFile.h"
#include "TTree.h"

#include "TString.h"
#include "TCanvas.h"
#include "TH1.h"
#include "TH2.h"
#include "TDirectory.h"
#include "TString.h"
#include "TLorentzVector.h"
#include <string>
#include <vector>
#include <sstream>
#define HambTree_cxx
#include "../interface/HambTree.h"
using namespace std;
template <class G>
class btagSort{
public:
  btagSort(){}
  ~btagSort(){}
  bool operator()(G o1 ,G o2 ){
    return (o1.second>o2.second);
  }
};

/*
 * 
 */
struct particleinfo{
  float pt, eta, phi , mass, b1Index , b2Index; 
    particleinfo( double pt_=-999, double eta_ =-999, double phi_=-999 , double mass_ = -999 , double b1_ = -999, double b2_ = -999 ){
      pt = pt_;
      eta= eta_;
      phi = phi_;
      mass = mass_;
      b1Index = b1_;
      b2Index = b2_;
    };
  void set( double pt_=-999, double eta_ =-999, double phi_=-999 , double mass_ = -999 , double b1_ = -999, double b2_ = -999 ){
      pt = pt_;
      eta= eta_;
      phi = phi_;
      mass = mass_;
      b1Index = b1_;
      b2Index = b2_;
  };
};
int main(int argc, char** argv) {
  HambTree * rds;
  TString names;
  TString treename = "/Trees/Events";
  TH1D * cutflow = 0;
  TString Mode = "";
  TString dir ="";
  bool blind = false;
  for (int f = 1; f < argc; f++) {
    std::string arg_fth(*(argv + f));
    if (arg_fth == "mc") {
      f++;
      std::string out(*(argv + f));
      //TFile * fdata = TFile::Open((string("eos_cb/user/a/ajafari/Hamb13/Oct14_8020_Opt/Trees/")+out).c_str());
      TFile * fdata = TFile::Open(out.c_str());            
      rds = new HambTree((TTree*) fdata->Get(dir+treename));
      int pos = out.find(".root");
      names = (out.substr(0, pos).c_str());
      TDirectory * d = (TDirectory*)fdata->Get(dir+"/CutFlowTable");
      TList * dlist = d->GetListOfKeys();
      //cutflow = new TH1D(*(TH1D*) fdata->Get(string("Hamb/CutFlowTable/CutFlowTable_").c_str()+names+string("_0").c_str()));
      cutflow = new TH1D(*(TH1D*) d->Get(dlist->At(0)->GetName()));
    } else if(arg_fth == "Mode"){
      f++;
      std::string out(*(argv + f));
      Mode = out.c_str();       
    } else if(arg_fth == "dir"){
      f++;
      std::string out(*(argv + f));
      dir = out.c_str();       
    }
  }

  
  TFile * fout = new TFile("out/"+dir+names + ".root", "recreate");
  fout->cd();
  TDirectory* hamb = fout->mkdir(dir);
  hamb->mkdir("Trees")->cd();
  
  particleinfo mH, mHReg, mHb, mHbReg;
  float amuMass, bWTL, bWLL, chiB, chiH, chiSum,higgsMass,abMass,higgsPt,abPt,amPt;
  float bWTT, bWTM, bWMM;
  bool passTL, passJetSize, passMuSize, passJet1Pt, passJet2Pt, passMu1Pt, passMu2Pt;
  bool passTT, passTM, passMM;
  
  TTree * newTree = rds->fChain->CloneTree(0);
  if(Mode == "Opt"){
    newTree->Branch("mH", &mH, "pt:eta:phi:mass:b1Index:b2Index");
    newTree->Branch("mHb", &mHb, "pt:eta:phi:mass:b1Index:b2Index");
    newTree->Branch("mHReg", &mHReg, "pt:eta:phi:mass:b1Index:b2Index");
    newTree->Branch("mHbReg", &mHbReg, "pt:eta:phi:mass:b1Index:b2Index");
    newTree->Branch("aMuMass", &amuMass);
  }  else if (Mode == "mHcut") {
    newTree->Branch("chi2B", &chiB);
    newTree->Branch("chi2H", &chiH);
    newTree->Branch("chi2Sum", &chiSum);
    newTree->Branch("higgsMass", &higgsMass);
    newTree->Branch("abMass", &abMass);
    newTree->Branch("higgsPt", &higgsPt); 
    newTree->Branch("abPt", &abPt);
    newTree->Branch("amPt", &amPt);
    newTree->Branch("passTL", &passTL); 
    newTree->Branch("passTT", &passTT);     	    
    newTree->Branch("passTM", &passTM);
    newTree->Branch("passMM", &passMM);
    newTree->Branch("bWeightTL", &bWTL);
    newTree->Branch("bWeightTT", &bWTT);				        			
    newTree->Branch("bWeightTM", &bWTM);
    newTree->Branch("bWeightMM", &bWMM);	    	    	             	    
    newTree->Branch("passJetSize", &passJetSize);
    newTree->Branch("passMuSize", &passMuSize);
    newTree->Branch("passJet1Pt", &passJet1Pt);
    newTree->Branch("passJet2Pt", &passJet2Pt);
    newTree->Branch("passMu1Pt", &passMu1Pt);
    newTree->Branch("passMu2Pt", &passMu2Pt);
  } else {
    newTree->Branch("aMuMass", &amuMass);
    newTree->Branch("bWeightTL", &bWTL);				        			
    newTree->Branch("bWeightLL", &bWLL);
  }
  cout << rds->fChain->GetEntriesFast() << endl;
  for (int eventNumber = 0; eventNumber < rds->fChain->GetEntriesFast(); eventNumber++) {
    particleinfo tmp;
    mH = mHReg = mHb = mHbReg = tmp;
    rds->GetEntry(eventNumber);
    TLorentzVector m1,m2,a;
    m1.SetPtEtaPhiM(rds->muPt->at(0),rds->muEta->at(0),rds->muPhi->at(0),0);
    int myIndex = -1;    	        
    for(unsigned int i = 1; i < rds->muEta->size(); i++){
      if((!rds->muCharge->at(i) && rds->muCharge->at(0)) || (rds->muCharge->at(i) && !rds->muCharge->at(0))){
	myIndex = i;
	break;
      }    	        
    }
    if(myIndex == -1){
      cout<<"ERROR WITH MU CHARGE"<<endl;
      return -1;  
    }      
    m2.SetPtEtaPhiM(rds->muPt->at(myIndex),
		    rds->muEta->at(myIndex),
		    rds->muPhi->at(myIndex),0);                   
    a = m1+m2;       
    if (a.M() < 15 || a.M() > 70) continue;
    
    if(Mode == "Opt"){
      if (rds->muPt->size() <  2)  continue;
      if (rds->muPt->at(0) < 20 ) continue; //25
      if (rds->muPt->at(1) < 9 )  continue; //10
      std::vector<int> JetIndecies;
      std::vector<int> bQuarkJetIndecies;    	          	      
      for (unsigned int iJet = 0; iJet < rds->jetsPt->size(); iJet++){
	if (rds->jetsPt->at(iJet) < 15) continue;
	TLorentzVector jet;
	jet.SetPtEtaPhiM(rds->jetsPt->at(iJet),rds->jetsEta->at(iJet),rds->jetsPhi->at(iJet),rds->jetsE->at(iJet));
	if (jet.DeltaR(m1) < 0.4 || jet.DeltaR(m2) < 0.4) continue;
	JetIndecies.push_back(iJet);
	if (rds->jetsBtag->at(iJet) > 0.5426) 
	  bQuarkJetIndecies.push_back(iJet);
      }
      if (JetIndecies.size()<2) continue;    	      
      if (rds->jetsPt->at(JetIndecies.at(0)) < 20 ) continue;
      
      
      
      amuMass = a.M();

      TLorentzVector bJet1,bJet2, H, ab;
      bJet1.SetPtEtaPhiE(rds->jetsPt->at(0), rds->jetsEta->at(0), rds->jetsPhi->at(0), rds->jetsE->at(0));
      bJet2.SetPtEtaPhiE(rds->jetsPt->at(1), rds->jetsEta->at(1), rds->jetsPhi->at(1), rds->jetsE->at(1));
      ab = bJet1+bJet2;
      H = bJet1+bJet2+a;
      mH.set(H.Pt(), H.Eta(), H.Phi(), H.M(), 0,1);
      mHb.set(ab.Pt(), ab.Eta(), ab.Phi(), ab.M(), 0,1);
      double R = a.M()/(bJet1+bJet2).M();
      bJet1 = R*bJet1;
      bJet2 = R*bJet2;
      ab = bJet1+bJet2;		    
      H = bJet1+bJet2+a;
      mHReg.set(H.Pt(), H.Eta(), H.Phi(), H.M(), 0,1);
      mHbReg.set(ab.Pt(), ab.Eta(), ab.Phi(), ab.M(), 0,1);

      newTree->Fill();
    } else if(Mode == "mHcut"){
      //if(fabs(rds->higgsReg_mass - 125)>20)
      //	continue;
      
      // These cuts follow the optimization on Dec 15 (https://twiki.cern.ch/twiki/bin/viewauth/CMS/HigAmumuAbb#Optimization)
      if (rds->muPt->size() <  2){
	passMuSize = false;
	//continue;
      } else  passMuSize = true;
      
      if (rds->jetsPt->size() <  2){
	passJetSize = false;
	//continue;
      } else passJetSize = true;
      
      
      if (rds->muPt->at(0) < 20 ) {
	passMu1Pt = false;
	//continue;
      } else passMu1Pt = true;
      
      if (rds->muPt->at(1) < 9 ) {
	passMu2Pt = false;
	//continue;
      } else passMu2Pt = true;
      
      if (rds->jetsPt->at(0) < 20 ) {
	passJet1Pt = false;
	//continue;
      } else passJet1Pt = true;
      
      if (rds->jetsPt->at(1) < 15 )  {
	passJet2Pt = false;
	//continue;
      } passJet2Pt = true;
      //if (rds->met > 60 )  continue;  
      
      //TL condition
      std::vector<int> bQuarkJetIndecies;
      std::vector<std::pair<TLorentzVector,float> > bQuarkJets;
      std::vector<std::pair<TLorentzVector,float> > bQuarkJetsBtagOrderd;
      for(unsigned int iJet = 0; iJet < rds->jetsPt->size(); iJet++){
	if(!(rds->jetsBtag->at(iJet) > 0.5426)) continue;
	bQuarkJetIndecies.push_back(iJet);
	TLorentzVector b;
	b.SetPtEtaPhiE(rds->jetsPt->at(iJet), rds->jetsEta->at(iJet), rds->jetsPhi->at(iJet), rds->jetsE->at(iJet));
	bQuarkJets.push_back(make_pair(b,rds->jetsBtag->at(iJet)));	
	bQuarkJetsBtagOrderd.push_back(make_pair(b,rds->jetsBtag->at(iJet)));
      }
      
      //TL condition Check
      if(bQuarkJets.size() >= 2){
	if ((bQuarkJets[0].second > 0.9535 && bQuarkJets[1].second >0.5426 ) || (bQuarkJets[1].second > 0.9535 && bQuarkJets[0].second >0.5426 ) ) 
	  passTL = true;
	else {
	  passTL = false;
	  //continue;
	}
      }
      
      //TM condition Check
      if(bQuarkJets.size() >= 2){
	if ((bQuarkJets[0].second > 0.9535 && bQuarkJets[1].second >0.8484 ) || (bQuarkJets[1].second > 0.9535 && bQuarkJets[0].second >0.8484 ) ) 
	  passTM = true;
	else {
	  passTM = false;
	  //continue;
	}
      }
      
      //TT condition Check
      if(bQuarkJets.size() >= 2){
	if (bQuarkJets[0].second > 0.9535 && bQuarkJets[1].second >0.9535  ) 
	  passTT = true;
	else {
	  passTT = false;
	  //continue;
	}
      }    		  
      
      
      //MM condition Check
      if(bQuarkJets.size() >= 2){
	if (bQuarkJets[0].second > 0.8484 && bQuarkJets[1].second >0.8484  ) 
	  passMM = true;
	else {
	  passMM = false;
	  //continue;
	}
      }    		  
      
      
      bWTM = rds->bWs_W1M1T;
      bWTT = rds->bWs_W2T;
      bWMM = rds->bWs_W2M;
      bWTL = rds->bWs_W1L1T; 
      
      
      // Chi2 Evaluations and selections
      abMass = (bQuarkJets[0].first+bQuarkJets[1].first).M();
      higgsMass = ((bQuarkJets[0].first+bQuarkJets[1].first)+a).M();
      abPt = (bQuarkJets[0].first+bQuarkJets[1].first).Pt();
      higgsPt = ((bQuarkJets[0].first+bQuarkJets[1].first)+a).Pt();
      amPt = a.Pt();
      
      double dmassB = fabs(abMass-a.M());
      double dmassH = fabs(higgsMass-125);
      
      double width = 0.18 + 0.175*a.M();
      
      chiB = (dmassB*dmassB)/(width*width);
      chiH = (dmassH*dmassH)/(10.6*10.6);
      chiSum = chiB+chiH;
      
      //if(chiSum > 5) continue;
      
      newTree->Fill();		
    } else {
      
      //amuMass = rds->aMu_mass;
      //according to optimization of Dec. 2016
      if(rds->jetsPt->at(0) < 20) continue;
      //
      amuMass = a.M();
      bWTL = rds->bWs_W1L1T;
      bWLL = rds->bWs_W2L;
      newTree->Fill();			
    }
  }
  newTree->Write();
  hamb->mkdir("CutFlowTable")->cd();
  cutflow->Write();
  fout->cd();
  fout->Save();
  fout->Close();
  
  return 1;
}


