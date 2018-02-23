#include <sstream>
void SignalYieldReader(){
	TFile * f = TFile::Open("/home/nadjieh/cernbox/Hamb13/June06_Full2016_MassProd/Results/out_FinalPlots_temp.root");
	TGraphErrors * g = new TGraphErrors(10);
	TDirectory * d = (TDirectory*)f->Get("SR/amuMass/signals");
	d->ls();
	TList * l = d->GetListOfKeys();
	double yE;
	for(int i = 0; i< 9; i++){
		double mass = 20 + 5*i;
		TH1F * h = (TH1F*)d->Get(l->At(i)->GetName());
		cout << h->GetName() <<endl;
		h->Print("all");
		cout<<h->GetXaxis()->GetNbins()<<endl;
		double y = h->IntegralAndError(-1,56,yE);
		g->SetPoint(i, mass, y);	
		g->SetPointError(i, 0, yE);
	}
	g->SetPoint(9, 62.5, 8.861);	
	g->SetPointError(9, 0, yE);
	TCanvas s;
	s.cd();
	g->Draw("ap");
	s.SaveAs("yields2016.C");

//SR_amuMass_Signal20


}
