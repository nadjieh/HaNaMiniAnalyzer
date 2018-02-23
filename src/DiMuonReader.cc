#include "Haamm/HaNaMiniAnalyzer/interface/DiMuonReader.h"

using namespace edm;
using namespace pat;

DiMuonReader::DiMuonReader( edm::ParameterSet const& iConfig, edm::ConsumesCollector && iC , bool isData , string SetupDir) :
  BaseEventReader< pat::MuonCollection >( iConfig , &iC ),
  MuonLeadingPtCut( iConfig.getParameter<double>( "MuonLeadingPtCut" ) ),
  MuonSubLeadingPtCut( iConfig.getParameter<double>( "MuonSubLeadingPtCut" ) ),
  MuonIsoCut( iConfig.getParameter<double>( "MuonIsoCut" ) ),
  MuonEtaCut( iConfig.getParameter<double>( "MuonEtaCut" ) ),
  DiMuLowMassCut( iConfig.getParameter<double>( "DiMuLowMassCut" ) ),
  DiMuZMassWindow( iConfig.getParameter<double>( "DiMuZMassWindow" ) ),
  MuonID( iConfig.getParameter<int>( "MuonID" ) ), // 0 no id, 1 loose, 2 medium, 3 tight, 4 soft
  DiMuCharge( iConfig.getParameter<int>( "DiMuCharge" ) ),
  IsData(isData),
  isHamb(iConfig.getParameter<bool>( "isHamb" )),
  isSignalStudy(iConfig.getParameter<bool>( "isSignalStudy" )),
  uncert( iConfig.getParameter<int>( "HLTUnc" ) )
{
  if( !IsData ){
    TFile* f1 = TFile::Open( TString(SetupDir + "/MuonIDSF.root") );
    gROOT->cd();
    hMuSFID = NULL;
    if(MuonID == 1 ) // Loose ID
      hMuSFID = (TH2*)( f1->Get("MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio")->Clone("MuSFID") );
    else if(MuonID == 2 ) // Medium ID
      hMuSFID = (TH2*)( f1->Get("MC_NUM_MediumID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio")->Clone("MuSFID") );
    else if(MuonID == 3 ) // Tight ID
      hMuSFID = (TH2*)( f1->Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/pt_abseta_ratio")->Clone("MuSFID") );
    //else if(MuonID == 4 ) // Soft ID
    //  hMuSFID = (TH2*)( f1->Get("MC_NUM_SoftID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio")->Clone("MuSFID") );
    else
      cout << "No scale factor is availabel for Muon ID " << MuonID << endl;
    f1->Close();
    
    f1 = TFile::Open( TString(SetupDir + "/MuonIsoSF.root") );
    gROOT->cd();
    if( MuonIsoCut == 0.15 )
      hMuSFIso = (TH2*)( f1->Get("TightISO_TightID_pt_eta/pt_abseta_ratio")->Clone("MuSFIso") );
    else if( MuonIsoCut == 0.25 )
      hMuSFIso = (TH2*)( f1->Get("LooseISO_TightID_pt_eta/pt_abseta_ratio")->Clone("MuSFIso") );
    else
      cout << "No scale factor is availabel for Muon Iso " << MuonIsoCut << endl;
    f1->Close();

    f1 = TFile::Open(TString(SetupDir + "/DiMuonHLTs.root"));
    gROOT->cd();
    hMuHltMu17Mu8 = (TH2*)( f1->Get("scalefactor_eta2d_with_syst")->Clone("scalefactor_eta2d_with_syst_") );
    //hMuHltMu17Mu8_DZ = (TH2*)( f1->Get("Mu17Mu8_DZ")->Clone("Mu17Mu8_DZ_") );
    f1->Close();
    /* According to Reza's calculations: https://indico.cern.ch/event/640550/contributions/2601786/attachments/1465253/2264977/EFT_Dilepton_2.pdf 
     * ** SingleMu Trigger should be added
     * ** If necessary at analysis level the muon topologic cut should be applied
     * ** Only one of the two weights below is sufficient
    */
    

    /* Tracking efficiency 
     * https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults#Results_on_the_full_2016_data
     */
    f1 = TFile::Open(TString(SetupDir + "/Tracking.root")); 
    hTrk = (TGraphAsymmErrors*)((TGraphAsymmErrors*) f1->Get("ratio_eff_aeta_dr030e030_corr"))->Clone("hTrk");
    f1->Close(); 
  }
  myIso = new Isolation("TestIso");
  goodMuIso.clear();
  goodMuId.clear();
  goodMuIsoChargedHadronPt.clear();
  goodMuIsoNeutralHadronEt.clear();
  goodMuIsoPhotonEt.clear();
  goodMuIsoPUPt.clear();

  cout << MuonSubLeadingPtCut << "  " << MuonEtaCut << "  " << MuonLeadingPtCut << "    " << MuonIsoCut << "    " << MuonID << endl;
}


DiMuonReader::SelectionStatus DiMuonReader::Read( const edm::Event& iEvent, const reco::Vertex* PV ){ 
  BaseEventReader< pat::MuonCollection >::Read( iEvent );
    
  W = 1.0;
  goodMus.clear();
  goodMuIso.clear();
  goodMuIsoChargedHadronPt.clear();
  goodMuIsoNeutralHadronEt.clear();
  goodMuIsoPhotonEt.clear();
  goodMuIsoPUPt.clear();
  goodMuId.clear();
  
  for (const pat::Muon &mu : *handle) {
    if (mu.pt() < MuonSubLeadingPtCut || fabs(mu.eta()) > MuonEtaCut )
      continue;
    reco::MuonPFIsolation iso = mu.pfIsolationR04();
    myIso->Fill(iso, mu.pt());
    if( (goodMus.size() == 0) && (mu.pt() < MuonLeadingPtCut) )
      continue;
    //cout << "---- Loose: "<< muon::isLooseMuon( mu )
    //     << "\tMedium: "<<muon::isMediumMuon( mu )
	// << "\tTight: "<<muon::isTightMuon(mu ,*PV)
	 //<< "\tSoft: "<<muon::isSoftMuon( mu ,*PV)<<endl;
    if( MuonID == 1 ){
      if (!muon::isLooseMuon( mu ) ) continue;
    }
    else if(MuonID == 2){
      if (!muon::isMediumMuon( mu ) ) continue;
    }
    else if(MuonID == 3){
      if (!muon::isTightMuon(mu ,*PV) ) continue;
    }
    else if(MuonID == 4){
      if (!muon::isSoftMuon( mu ,*PV) ) continue;
    }
    //cout<<"In muon loop, isolation is ";
    double reliso = (iso.sumChargedHadronPt+TMath::Max(0.,iso.sumNeutralHadronEt+iso.sumPhotonEt-0.5*iso.sumPUPt))/mu.pt();
    //cout<<reliso<<" to be compared with "<<MuonIsoCut<<endl;
    if( reliso > MuonIsoCut) continue;
    goodMus.push_back( mu );

    //Filling additional Info
    goodMuIso.push_back(reliso);
    goodMuIsoChargedHadronPt.push_back(iso.sumChargedHadronPt);
    goodMuIsoNeutralHadronEt.push_back(iso.sumNeutralHadronEt);
    goodMuIsoPhotonEt.push_back(iso.sumPhotonEt);
    goodMuIsoPUPt.push_back(iso.sumPUPt);
    if(!isSignalStudy){
    	if( MuonID == 1 ){
	      goodMuId.push_back(muon::isLooseMuon( mu ) );
        } else if(MuonID == 2){
	      goodMuId.push_back(muon::isMediumMuon( mu ) );
        } else if(MuonID == 3){
	      goodMuId.push_back(muon::isTightMuon(mu ,*PV) );
        } else if(MuonID == 4){
	      goodMuId.push_back(muon::isSoftMuon( mu ,*PV) );
        }
    } else {
    /////
    //REDOING MuId Fill
    	if(muon::isTightMuon(mu ,*PV)){
		//cout<<"I am tight ------"<<endl;
		goodMuId.push_back(3);
    	} else if(muon::isMediumMuon( mu )){
		//cout<<"I am medium /////"<<endl;
		goodMuId.push_back(2);
    	} else if(muon::isLooseMuon( mu )){
		//cout<<"I am loose >>>>>>"<<endl;
		goodMuId.push_back(1);
    	} else if(muon::isSoftMuon( mu ,*PV)){
		//cout<<"I am soft +++++++"<<endl;
		goodMuId.push_back(4);
	}
    }
    /////
  }
   
  if( goodMus.size() < 2 ) return DiMuonReader::LessThan2Muons ;
  /*cout <<"---------- In DiMuReader vectors --------------"<<endl;
  cout <<"---- chargedIso 0: "<<goodMuIsoChargedHadronPt[0]<<",\tchargedIso 1: "<<goodMuIsoChargedHadronPt[1]<<endl;
  cout <<"---- neutralIso 0: "<<goodMuIsoNeutralHadronEt[0]<<",\tneutralIso 1: "<<goodMuIsoNeutralHadronEt[1]<<endl;
  cout <<"---- photonIso 0: "<<goodMuIsoPhotonEt[0]<<",\tphotonIso 1: "<<goodMuIsoPhotonEt[1]<<endl;
  cout <<"---- pilupIso 0: "<<goodMuIsoPUPt[0]<<",\tpileupIso 1: "<<goodMuIsoPUPt[1]<<endl;
  cout <<"-----------------------------------------------"<<endl; */
  for ( pat::MuonCollection::iterator i = goodMus.begin(); i != goodMus.end(); ++i) {
    goodMusOS.clear();
    int mu0charge= i->charge();
    goodMusOS.push_back( *i );
    for(pat::MuonCollection::iterator j = i ; j != goodMus.end(); ++j) 
      if( (mu0charge * j->charge()) == DiMuCharge ){
	goodMusOS.push_back( *j );
	break;
      }
    if( goodMusOS.size() == 2 )
      break;
  }
  if( goodMusOS.size() != 2 )
    return DiMuonReader::NoPairWithChargeReq;

  if( !IsData ){
    W = MuonTrkEff(fabs(goodMusOS[0].eta()))*MuonTrkEff(fabs(goodMusOS[1].eta())); 
    if(W == 0) W = 1;
    if( MuonIsoCut == 0.25 )
      W *= MuonSFLoose(  goodMusOS[0].eta() , goodMusOS[0].pt() , goodMusOS[1].eta() , goodMusOS[1].pt() ); 
    else if( MuonIsoCut == 0.15 )
      W *= MuonSFMedium( goodMusOS[0].eta() , goodMusOS[0].pt() , goodMusOS[1].eta() , goodMusOS[1].pt() );

    W *= MuonSFHltEta( goodMusOS[0].eta() , goodMusOS[1].eta() ); 
  }
    
  DiMuon = DiObjectProxy( goodMusOS[0] , goodMusOS[1] );
  
  if( DiMuon.totalP4().M() < DiMuLowMassCut ) return DiMuonReader::LowMassPair;

  if(!isHamb){  
  	if( DiMuon.totalP4().M() > (91.0-DiMuZMassWindow) && DiMuon.totalP4().M() < (91.0+DiMuZMassWindow) ) return DiMuonReader::UnderTheZPeak;
  } else {
  	if( DiMuon.totalP4().M() > DiMuZMassWindow ) return DiMuonReader::UnderTheZPeak;
  }
  
  return DiMuonReader::Pass;
}

double DiMuonReader::MuonSFMedium( double etaL , double ptL , double etaSL , double ptSL ){
  // To accound for boundary effects
  if( ptSL < 20 ) ptSL = 20.01;
  if( ptL < 20 ) ptL = 20.01;
  if( ptSL > 120 ) ptSL = 119;
  if( ptL > 120 ) ptL = 119;
  //AN2016_025_v7 Figure 6, Middle Row, Right for trigger
  double ret = 1.0;

  double el = fabs(etaL);
  double esl = fabs(etaSL);


  ret *= ( hMuSFID->GetBinContent( hMuSFID->FindBin( ptL , el ) ) * hMuSFID->GetBinContent( hMuSFID->FindBin( ptSL , esl ) ) );
  ret *= (hMuSFIso->GetBinContent(hMuSFIso->FindBin(ptL ,el ) ) * hMuSFIso->GetBinContent( hMuSFIso->FindBin( ptSL , esl ) ) );

  return ret;
}
double DiMuonReader::MuonSFLoose( double etaL , double ptL , double etaSL , double ptSL ){
  // To accound for boundary effects
  if( ptSL < 20 ) ptSL = 20.01;
  if( ptL < 20 ) ptL = 20.01;
  if( ptSL > 120 ) ptSL = 119;
  if( ptL > 120 ) ptL = 119;

  //AN2016_025_v7 Figure 19, Middle Row, Right for trigger
  double ret = 1.0;
    
  double el = fabs(etaL);
  double esl = fabs(etaSL);

  if( ptSL < 20 || ptL < 20 )
    return ret;

  ret *= ( hMuSFID->GetBinContent( hMuSFID->FindBin( ptL , el ) ) * hMuSFID->GetBinContent( hMuSFID->FindBin( ptSL , esl ) ) );
  ret *= (hMuSFIso->GetBinContent(hMuSFIso->FindBin(ptL ,el ) ) * hMuSFIso->GetBinContent( hMuSFIso->FindBin( ptSL , esl ) ) );

  return ret;
}
double DiMuonReader::MuonSFHltMu17Mu8( double ptL , double ptSL ){
  double ret = 1.0;
  return ret;
  if(ptL < 20 )
	ptL = 20.01;
  if(ptSL < 18)
	ptSL = 20.01;
  ret *= (hMuHltMu17Mu8->GetBinContent(hMuHltMu17Mu8->FindBin(ptL,ptSL)));
  return ret;
}
double DiMuonReader::MuonSFHltMu17Mu8_DZ( double ptL , double ptSL ){
  double ret = 1.0;
  return ret; // Very close to one. The effect will be considered as uncertainty (1-2%)
  if(ptL < 20 )
        ptL = 20.01;
  if(ptSL < 18)
        ptSL = 20.01;
  ret *= (hMuHltMu17Mu8_DZ->GetBinContent(hMuHltMu17Mu8_DZ->FindBin(ptL,ptSL)));
  return ret;
}

double DiMuonReader::MuonSFHltEta( double eta1 , double eta2 ){

  int bin_id = hMuHltMu17Mu8->FindBin(fabs(eta1),fabs(eta2));
  double ret = hMuHltMu17Mu8->GetBinContent(bin_id);
  if(uncert != 0){
    double error = hMuHltMu17Mu8->GetBinError(bin_id);
    ret += (uncert*error);
  }
  return ret;
}
double DiMuonReader::MuonTrkEff(double abseta){
    double x,y;
    int iPoint = -1;
    if(abseta < 0.2) iPoint = 0;
    else if (abseta < 0.4) iPoint = 1;
    else if (abseta < 0.6) iPoint = 2;
    else if (abseta < 0.8) iPoint = 3;
    else if (abseta < 1.0) iPoint = 4;
    else if (abseta < 1.2) iPoint = 5;
    else if (abseta < 1.4) iPoint = 6;
    else if (abseta < 1.6) iPoint = 7;
    else if (abseta < 1.8) iPoint = 8;
    else if (abseta < 2.0) iPoint = 9;
    else if (abseta < 2.2) iPoint = 10;
    else iPoint = 11;
    hTrk->GetPoint(iPoint,x,y);
    return y*9.2/35.9;
}
