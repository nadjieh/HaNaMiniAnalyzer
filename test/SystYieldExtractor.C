TString prefix[5] = {"SRTL","SRTLexc", "SRTMexc", "SRTT","SRMM"};
//TString syst[13]={"Hamb", "HambPUUp", "HambPUDown", "HambJECUP", "HambJECDOWN", "HambJERUP", "HambJERDOWN", "HambBUP", "HambBDOWN", "HambMETUnClusDOWN", "HambMETUnClusUP", "HambHLTUP", "HambHLTDOWN"};
//TString syst[3]={"Hamb", "HambBUP", "HambBDOWN"};
//TString syst[13]={"Hambcentral", "HambPUUp", "HambPUDown", "HambJECUP", "HambJECDOWN", "HambJERUP", "HambJERDOWN", "HambBUP", "HambBDOWN", "HambMETUnClusDOWN", "HambMETUnClusUP", "HambHLTUP", "HambHLTDOWN"};
const int nSyst = 19;
TString syst[nSyst]={"HambBShapecentral","HambBShapeup_hfstats1",  "HambBShapedown_hfstats1",  "HambBShapeup_hfstats2",  "HambBShapedown_hfstats2",  "HambBShapeup_lfstats1",  "HambBShapedown_lfstats1",  "HambBShapeup_lfstats2",  "HambBShapedown_lfstats2",  "HambBShapeup_jes",  "HambBShapedown_jes",  "HambBShapeup_lf",  "HambBShapedown_lf",  "HambBShapeup_cferr1",  "HambBShapedown_cferr1",  "HambBShapeup_cferr2",  "HambBShapedown_cferr2",  "HambBShapeup_hf","HambBShapedown_hf"};

TString histname = "/General/amuMass/signals/";

TString sigs[8] = {"20","25","30","40","45","50","55","60"};
void SystYieldExtractor(){
	for (int j = 0; j < 5; j++){
		cout<<"***** *"<<prefix[j]<<"*"<<endl;
		cout <<"\t||";
		for (int iSyst = 0; iSyst<nSyst;iSyst++){
			cout<<syst[iSyst]<<"|";
			if(iSyst>0)
				cout<<" relDiff |";
		}
		cout<<endl;
		for (int i = 0; i < 8; i++){
			cout<<"| ma = "<<sigs[i]<<"|";		
			int n = 0;
			for (int iSyst = 0; iSyst<nSyst;iSyst++){
				TFile * f = TFile::Open("out_FinalPlots_"+syst[iSyst]+".root");
				if(iSyst>0){
				  cout<< ((TH1D*)f->Get(prefix[j]+histname+prefix[j]+"_amuMass_Signal"+sigs[i]))->Integral()<<"| =($"<<iSyst+2+n<<"-$2)/$2|";
				  n++;
				}
				else
				  cout<< ((TH1D*)f->Get(prefix[j]+histname+prefix[j]+"_amuMass_Signal"+sigs[i]))->Integral()<<"|";
			}
			cout<<endl;
		}
	}
}
