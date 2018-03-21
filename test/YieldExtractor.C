TString prefix[4] = {"SRTL","SRTL", "SRTM", "SRTT"};


TString histname = "/General/amuMass/signals/";
TString bkgname = "/General/amuMass/cats/SumMC";

TString sigs[9] = {"20","25","30","35","40","45","50","55","60"};
void YieldExtractor(){
	cout<<"| ";
	for (int j = 0; j < 4; j++)
		cout<<" *"<<prefix[j]<<"* |";
	cout<<endl;
	//TFile * f = TFile::Open("out_FinalPlots_defaults.root");
	TFile * f = TFile::Open("out_FinalPlots_allBtags.root");
	for (int i = 0; i < 9; i++){	
		for (int j = 0; j < 4; j++){
			if(j == 0)
				cout<< "| "<<((TH1D*)f->Get(prefix[j]+histname+prefix[j]+"_amuMass_Signal"+sigs[i]))->Integral()<<"|";
			else
				cout<< ((TH1D*)f->Get(prefix[j]+histname+prefix[j]+"_amuMass_Signal"+sigs[i]))->Integral()<<"|";
		}
		cout<<endl;
	}

	cout<<"| ";
	for (int j = 0; j < 4; j++)
		cout<<" *"<<prefix[j]<<"* |";
	cout<<endl;
	for (int j = 0; j < 4; j++){
		if(j == 0)
			cout<< "| "<<((TH1D*)f->Get(prefix[j]+bkgname))->Integral()<<"|";
		else
			cout<< ((TH1D*)f->Get(prefix[j]+bkgname))->Integral()<<"|";
	}
	cout<<endl;
}
