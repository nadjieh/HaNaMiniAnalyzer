#include <vector>
#include <iostream>
#include <TFile.h>
#include <TTree.h>
#include <TGraphAsymmErrors.h>
using namespace std;
const int nPoint = 86;
typedef std::vector<double> numbers;
numbers GetNumbers(TFile * f, double xsec = 1.){
	numbers ret;
	TTree * t = (TTree*) f->Get("limit");
	Double_t limit_ = 0;
	TBranch *limit  = t->GetBranch("limit");
    limit->SetAddress(&limit_);
    Float_t quant_ = 0;
	TBranch *quant  = t->GetBranch("quantileExpected");
    quant->SetAddress(&quant_);
    double res[6]={-1.,-1.,-1.-1.,-1.,-1.};
	for(int i = 0; i < t->GetEntriesFast(); i++){
		cout<<i<<endl;
		t->GetEntry(i);
		cout<<quant_<<" "<<limit_<<endl;
		if(fabs(quant_ - 0.5) < 0.001)
			res[2] = xsec*limit_;
		else if(fabs(quant_ - 0.025) < 0.001)
			res[0] = xsec*limit_;
		else if(fabs(quant_ - 0.16) < 0.001)
			res[1] = xsec*limit_;	
		else if(fabs(quant_ - 0.84) < 0.001)
			res[3] = xsec*limit_;
		else if(fabs(quant_ - 0.975) < 0.001)
			res[4] = xsec*limit_;
		else if(fabs(quant_ + 1) < 0.001)
			res[5] = xsec*limit_;
	}
	for(int i = 0; i<5; i++){
		if(i != 2)
			ret.push_back(fabs(res[i] - res[2]));
		else
			ret.push_back(res[i]);
	}
	//cout<<"bserved limit: "<<res[5]<<"\t";
	//ret.push_back(res[5]);
	cout<<ret[ret.size()-1]<<endl;
	return ret;
}
TGraph * GetObserved(std::vector<numbers> input, double * massesX){
	double y[nPoint];
	for(unsigned int iNumbers = 0; iNumbers < input.size(); iNumbers++){
		cout<<" --- >>> " << input[iNumbers][5] << endl;
		y[iNumbers] = input[iNumbers][5];
	}
	return new TGraph(nPoint, massesX,y);
}
TGraphAsymmErrors * GetGraph(std::vector<numbers> input, double * massesX, int nSigma = 1){
	double y[nPoint];
	double eyl[nPoint];
	double eyh[nPoint];	
	double exl[nPoint];
	double exh[nPoint];
	for(int i = 0; i < nPoint; i++){
		exl[i] = 0;
		exh[i] = 0;
	}
	
	for(unsigned int iNumbers = 0; iNumbers < input.size(); iNumbers++){
		y[iNumbers] = input[iNumbers][2];
		if(nSigma == 0){
			eyl[iNumbers] = 0;
			eyh[iNumbers] = 0;
		}
		if(nSigma == 1){
			eyl[iNumbers] = input[iNumbers][1];
			eyh[iNumbers] = input[iNumbers][3];
		}
		if(nSigma == 2){
			eyl[iNumbers] = input[iNumbers][0];
			eyh[iNumbers] = input[iNumbers][4];
		}
	}
	return new TGraphAsymmErrors(nPoint, massesX,y,exl,exh,eyl,eyh);
}

void limit(){

	double mass[nPoint];
	std::vector<TFile*> fs;
	stringstream STR;
	for(int num = 0; num<nPoint; num++){
		STR.str("");
		mass[num] = 20. + 0.5*num;
		if(num%2 == 0)	
			STR <<(int)mass[num];
		else
			STR <<(int)mass[num]<<".5";
		TString Mass = STR.str().c_str();
		if (TFile::Open("higgsCombineSigmaBr.Asymptotic.mH"+Mass+".root") != NULL)
		  fs.push_back( TFile::Open("higgsCombineSigmaBr.Asymptotic.mH"+Mass+".root"));
	}
	std::vector<numbers> mynumbers;
	std::vector<numbers> mynumbersXsec;	
	int n = (int)fs.size();
	
	for(unsigned int s = 0; s < fs.size(); s++){
		cout<<"--------------- "<<endl;
		mynumbers.push_back(GetNumbers(fs[s]));
		mynumbersXsec.push_back(GetNumbers(fs[s],0.00017));		
	}
	
	TGraphAsymmErrors * g0 = GetGraph(mynumbers,mass,0);
	g0->SetName("g0");
	g0->SetLineStyle(2);
	g0->SetLineWidth(2);
	g0->SetLineColor(kBlue);
	
	TGraphAsymmErrors * g00 = GetGraph(mynumbersXsec,mass,0);
	g00->SetName("g00");
	g00->SetLineStyle(2);
	g00->SetLineWidth(2);
	g00->SetLineColor(kBlue);

	
	TGraphAsymmErrors * g1 = GetGraph(mynumbers,mass,1);
	g1->SetName("g1");
	g1->SetFillColor(kYellow);
		
	TGraphAsymmErrors * g11 = GetGraph(mynumbersXsec,mass,1);
	g11->SetName("g1");
	g11->SetFillColor(kYellow);		
	g11->SetTitle("Expected 1 #sigma");
		
	TGraphAsymmErrors * g2 = GetGraph(mynumbers,mass,2);
	g2->SetName("g2");
	g2->SetFillColor(kGreen);
	
	TGraphAsymmErrors * g22 = GetGraph(mynumbersXsec,mass,2);
	g22->SetName("g2");
	g22->SetFillColor(kGreen);
	g22->SetTitle("Expected 2 #sigma");
	
	//TGraph * Obs = GetObserved(mynumbers,mass);
	//Obs->SetNameTitle("Obs","Observed");
	//Obs->SetFillColor(kWhite);
	//Obs->SetMarkerStyle(20);

	//TGraph * Obs2 = GetObserved(mynumbersXsec,mass);
        //Obs2->SetNameTitle("Obs2","Observed");
        //Obs2->SetFillColor(kWhite);
        //Obs2->SetMarkerStyle(20);
	
	TCanvas c;
	c.cd();
	
	g2->Draw("ap3");
	g1->Draw("p3");
	g0->Draw("p");
	//Obs->Draw("p");
	c.SaveAs("myLimitRSigmaBR.C");
	
	TCanvas c2;
	c2.cd();
	
	g22->Draw("ap3");
	g11->Draw("p3");
	g00->Draw("p");
	//Obs2->Draw("p");
	c2.SaveAs("myLimitXsec.C");

}
