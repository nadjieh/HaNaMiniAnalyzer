const double ALPHA = 1.06269e+00;
const double ALPHAERROR = 7.34041e-02;
const double FRAC = 6.07076e-01;
const double FRACERROR = 3.78748e-02;
const double WIDTH = 3.52681e-02;
const double WIDTHERROR = 8.18268e-03;
const double N = 3.22465e+00;
const double NERROR = 2.61430e-01;
const double A0 = -2.62883e-02;
const double A1 = 0.0092;
const double A1err = 0.0003;
const double B0 = -5.11135e-02;
const double B1 = 0.0166;
const double B1err = 0.00059;
const double M0 = -0.0629325;
const double M0err = 0.0041;
const double M1 = 9.97791e-01;
using namespace std;
using namespace RooFit;
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <stdio.h>
#include <ios>
#include <fstream>
#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "TH2.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooExponential.h"
#include "RooDataHist.h"
#include "RooAbsReal.h"
#include "RooConstVar.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooSimultaneous.h"
#include "RooFitResult.h"
#include "RooPolyVar.h"
#include "RooFormulaVar.h"
#include "RooCategory.h"
#include "TGraphErrors.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include <vector>
#include <sstream>
#include <fstream>
#include <iostream>
#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooFitResult.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1.h"
#include "TF1.h"
#include "TString.h"
#include "TCanvas.h"
#include "TColor.h"
#include "TColorWheel.h"
#include "TColorGradient.h"
#include "RooVoigtian.h"
#include "RooCBShape.h"
#include "RooPlot.h"
#include "RooAddPdf.h"
#include "RooRandom.h"
#include <algorithm>
#include <map>
const int nPar = 8;
const TString ParNames[]={"sigma","sigma_cb","frac","n","alpha","width","mS","a1"};
//const TString ParNames[]={/*"sigma",*/"sigma_cb"};

struct VarInfo{
	TString name;
	bool isCommon;
	bool isFixed;
	float val;
	float xD;
	float xU;
};
std::vector<VarInfo> CardReader(TString card){
	ifstream f(card);
	std::vector<VarInfo> ret;
    string line;
    int iLine = 0;
	if (f.is_open()) {
    	while (getline(f, line)) {
    	    iLine++;
            TString linestr(line.c_str());
            if (iLine == 1) {
               continue;
            }
            //frac	1	0	-1000	0	1
            VarInfo tmp;
            tmp.name = line.substr(0,line.find("\t")).c_str();
            string subline = line.substr(line.find("\t")+1);
            tmp.isCommon = (subline.substr(0,subline.find("\t")) == string("1"));
            subline = subline.substr(subline.find("\t")+1);
            tmp.isFixed = (subline.substr(0,subline.find("\t")) == string("1"));
            subline = subline.substr(subline.find("\t")+1);
            tmp.val = std::atof(subline.substr(0,subline.find("\t")).c_str());
            subline = subline.substr(subline.find("\t")+1);
            tmp.xD = std::atof(subline.substr(0,subline.find("\t")).c_str());
            subline = subline.substr(subline.find("\t")+1);
            tmp.xU = std::atof(subline.substr(0,subline.find("\t")).c_str());            
            ret.push_back(tmp);
        }
            f.close();
    }

	return ret;
}


std::pair<double, double> GraphRangeSetter(TGraphErrors * g) {
    int n = g->GetN();
    std::vector<double> valsup;
    std::vector<double> valsdown;
    double x, y, e;
    for (int i = 0; i < n; i++) {
        g->GetPoint(i, x, y);
        e = g->GetErrorY(i);
        valsup.push_back(y + e);
        valsdown.push_back(y - e);
    }
    sort(valsup.begin(), valsup.end());
    sort(valsdown.begin(), valsdown.end());
    return make_pair((1 - (valsdown[0]*0.2 / fabs(valsdown[0]))) * valsdown[0],
            (1 + (valsup[valsup.size() - 1]*0.2 / fabs(valsup[valsup.size() - 1]))) * valsup[valsup.size() - 1]);
}

TGraph * GoodRangeGraph(TGraphErrors * g) {
    std::pair<double, double> points = GraphRangeSetter(g);
    double x[4] = {30, 40, 50, 60};
    double y[4] = {points.first, points.second, points.first, points.second};
    TGraph * good = new TGraph(4, x, y);
    good->SetLineColor(kWhite);
    good->SetMarkerColor(kWhite);
    good->SetNameTitle(g->GetName(), g->GetTitle());
    return good;
}

TGraph * GoodRangeGraph(TGraphErrors * g, TGraphErrors * g2) {
    std::pair<double, double> points = GraphRangeSetter(g);
    std::pair<double, double> points2 = GraphRangeSetter(g2);
    if (points.first < points2.first)
        points2.first = points.first;
    if (points.second < points2.second)
        points2.second = points.second;
    double x[4] = {30, 40, 50, 60};
    double y[4] = {points2.first, points2.second, points2.first, points2.second};
    TGraph * good = new TGraph(4, x, y);
    good->SetLineColor(kWhite);
    good->SetMarkerColor(kWhite);
    good->SetNameTitle(g2->GetName(), g2->GetTitle());
    cout << good << endl;
    return good;
}

typedef std::pair<double, std::vector<int> > PerMassParameRange;

class RangesPerSyst {
public:

    RangesPerSyst(TString name, std::vector<PerMassParameRange> input) : Name(name) {
        for (unsigned int i = 0; i < input.size(); i++) {
            info.push_back(input[i]);
        }
        paramIndex["alpha"] = 0;
        paramIndex["frac"] = 1;
        paramIndex["width"] = 2;
        paramIndex["n"] = 3;
    }

    RangesPerSyst() {
        paramIndex["alpha"] = 0;
        paramIndex["frac"] = 1;
        paramIndex["width"] = 2;
        paramIndex["n"] = 3;
    }

    ~RangesPerSyst() {
    }

    int GetMassIndex(double mass) {
        int ret = -1;
        for (unsigned int i = 0; i < info.size(); i++) {
            if (info[i].first == mass) {
                ret = i;
                break;
            }
        }
        return ret;
    }

    PerMassParameRange GetPerMassRaramRange(double mass) {
        int massIndex = this->GetMassIndex(mass);
        if (massIndex == -1) {
            cout << "ERROR: BAD MASS VALUE FOR RANGE" << endl;
            std::vector<int> c;
            c.clear();
            return make_pair(mass, c);
        }
        return info[massIndex];
    }

    int GetParamSystRange(double mass, int iPar) {
        int massIndex = this->GetMassIndex(mass);
        if (massIndex == -1)
            return 10;
        return info[massIndex].second[iPar];
    }

    int GetParamSystRange(double mass, TString iParChr) {
        int iPar = paramIndex[iParChr];
        return this->GetParamSystRange(mass, iPar);
    }

    void SetParamSystRange(double mass, int iPar, int range) {
        int massIndex = this->GetMassIndex(mass);
        if (massIndex == -1) {
            cout << "ERROR: BAD MASS VALUE FOR RANGE, SET TO 10" << endl;
            info[massIndex].second[iPar] = 10;
            return;
        }
        //        cout << "Index: " << iPar << ", range: " << range << endl;
        info[massIndex].second[iPar] = range;
    }

    void SetParamSystRange(double mass, TString iParChr, int range) {
        int iPar = paramIndex[iParChr];
        this->SetParamSystRange(mass, iPar, range);
    }

    TString GetSystName() {
        return Name;
    }
private:
    TString Name;
    std::vector<PerMassParameRange> info;
    std::map<TString, int> paramIndex;
};

typedef std::map< TString, RangesPerSyst> SystRanges;

void PrintFr(RooFitResult * fr, std::vector<int> tmpMasspoints, std::vector<VarInfo> varInfo, TString option = "") {

	
	std::vector<TString> All;
  	stringstream S;    
    for (unsigned int i = 0; i < tmpMasspoints.size(); i++) {
        for (unsigned int j = 0; j < varInfo.size(); j++) {
			S.str("");
        	if(varInfo[j].isFixed) continue;
        	if(!varInfo[j].isCommon )
        		S << varInfo[j].name<<"_M"<<tmpMasspoints[i];
        	else
        		S << varInfo[j].name;
            All.push_back(S.str().c_str());     
            cout << All[All.size() - 1] << endl;
        }
        for(int ipar = 0; ipar <(nPar-varInfo.size()); ipar++ ){
            S.str("");
        	S << ParNames[ipar]<<"_M"<<tmpMasspoints[i];
            All.push_back(S.str().c_str());     
        }
    	//}
    }	

    cout<<"In Print Out ------"<<endl;

    
    TH2D * h = new TH2D("correlations", "correlations", All.size(), 0., (double) (All.size()),
            All.size(), 0., (double) (All.size()));
    TH2D * h2 = new TH2D("abscorrelations", "abscorrelations", All.size(), 0., (double) (All.size()),
            All.size(), 0., (double) (All.size()));


    for (unsigned int i = 0; i < All.size(); i++) {
        h->GetXaxis()->SetBinLabel(i + 1, All[i]);
        h->GetYaxis()->SetBinLabel(i + 1, All[i]);
        h2->GetXaxis()->SetBinLabel(i + 1, All[i]);
        h2->GetYaxis()->SetBinLabel(i + 1, All[i]);
        cout << "Bin " << i + 1 << "- " << All[i] << "\tIn FitResult: "<< ((RooRealVar*) fr->floatParsFinal().find(All[i]))<< endl;
    }


    int n = 0;
    for (unsigned int i = 0; i < All.size(); i++) {
        for (unsigned int j = 0; j < All.size(); j++) {
            n++;
            cout << i + 1 << "- " << j + 1 << ": " << h->GetXaxis()->GetBinLabel(j + 1) << "\tvs\t" << h->GetYaxis()->GetBinLabel(i + 1) << endl;
            h->SetBinContent(j + 1, i + 1, fr->correlation(h->GetXaxis()->GetBinLabel(j + 1), h->GetYaxis()->GetBinLabel(i + 1)));
            h2->SetBinContent(j + 1, i + 1, fabs(fr->correlation(h->GetXaxis()->GetBinLabel(j + 1), h->GetYaxis()->GetBinLabel(i + 1))));
        }
    }


    TFile * f = new TFile("correlations_" + option + ".root", "recreate");
    f->cd();
    h->Write();
    h2->Write();
    f->Close();
}



RooCBShape * CBMaker(double Mass, RooRealVar * mass, RooAbsReal * mean,
        RooAbsReal * sigma_cb = 0, RooRealVar * n = 0, RooRealVar * alpha = 0, RooRealVar * b0 = 0, RooRealVar * b1 = 0,
        RooRealVar * MH = 0) {
    stringstream s;
    s << "_M" << Mass;
    TString Name = s.str().c_str();
    if (n == 0) {
	    n = new RooRealVar("n" + Name, "" + Name,0,10 );//2.31 
    }
    if (alpha == 0) {
	    alpha = new RooRealVar("alpha" + Name, "" + Name, 0,5);//1.25
    }
    if (sigma_cb == 0) {
    	cout<< "sigma_cb is zero" <<endl;
        if (/*b0 != 0 &&*/ b1 != 0) {
            if (MH == 0)
                sigma_cb = new RooPolyVar("sigma_cb" + Name, "sigma_cb" + Name, *mean, RooArgSet(*b0, *b1));
            else {
                sigma_cb = new RooFormulaVar("sigma_cb" + Name, "-0.0089+@1*@0", RooArgSet(*MH, *b1));
            }
        } else {
        	cout << "sigma_cb is defined"<<endl;
            sigma_cb = new RooRealVar("sigma_cb" + Name, "sigma_cb" + Name, 0, 2);
        }
    }
    RooCBShape * CB = new RooCBShape("cball" + Name, "crystal ball" + Name, *mass, *mean, *sigma_cb, *alpha, *n);

    return CB;
}

RooVoigtian * VoigMaker(double Mass, RooRealVar * mass, RooAbsReal * mean,
        RooAbsReal * sigma = 0, RooRealVar * width = 0, RooRealVar * a0 = 0, RooRealVar * a1 = 0, 
        RooRealVar * MH = 0) {
    stringstream s;
    s << "_M" << Mass;
    TString Name = s.str().c_str();
    if (sigma == 0) {
        if (a1 != 0 /*&& a0 != 0*/) {
            if (MH == 0)
                sigma = new RooPolyVar("sigma" + Name, "sigma" + Name, *mean, RooArgSet(*a0, *a1));
            else {
                sigma = new RooFormulaVar("sigma" + Name, "-0.029+@1*@0", RooArgSet(*MH, *a1));
            }
        } else {
            sigma = new RooRealVar("sigma" + Name, "sigma" + Name, 0,1);
        }
    }
    if (width == 0) {
        width = new RooRealVar("width" + Name, "width" + Name, 0,2);//0.048
    }
    RooVoigtian * Voig = new RooVoigtian("tmp" + Name, "" + Name, *mass, *mean, *width, *sigma);

    return Voig;
}

RooAddPdf * VoigCBMaker(double Mass, RooRealVar * mass, std::map< TString, RooRealVar*> inputs,
        RooRealVar * frac = 0, TString option = "") {
    stringstream s;
    s << "_M" << Mass;
    TString Name = s.str().c_str();
    RooAbsReal * mean = 0;
    RooAbsReal * mean_cb = 0;    
    RooRealVar * MH = new RooRealVar("MH" + Name, "MH" + Name, Mass);
    if (inputs["mS"] == 0 && inputs["mcbS"] == 0) {
    	cout<< "No mS and mcbS"<<endl;
        mean = new RooRealVar("mean" + Name, "mean" + Name, Mass, 10,70);
        mean_cb = new RooRealVar("mean_cb" + Name, "mean_cb" + Name, Mass, 10,70);
    } else {
    	cout<<"A linear mean with m"<<endl;
        mean = new RooFormulaVar("mean" + Name, "@0+@1", RooArgSet(*MH, *inputs["mS"]));
        //mean_cb = new RooFormulaVar("mean_cb" + Name, "@0+@1", RooArgSet(*MH, *inputs["mcbS"]));        
    }
    
    RooVoigtian * Voig = VoigMaker(Mass, mass, mean, inputs["sigma"], inputs["width"], inputs["a0"], inputs["a1"], MH);
    RooCBShape * CB = CBMaker(Mass, mass, mean, inputs["sigma_cb"], inputs["n"],
            inputs["alpha"], inputs["b0"], inputs["b1"], MH);
    if (frac == 0) {
        frac = new RooRealVar("frac" + Name, "frac" + Name, 0.5, 0, 1);
    }
    RooAddPdf * Voig2 = new RooAddPdf("sum" + Name, "Gaussian crystal ball and Voig PDF" + Name, RooArgList(*Voig, *CB), RooArgList(*frac));

    return Voig2;
}

void DrawEvolutions(RooFitResult * fr, std::vector<int> tmpMasspoints, std::vector<VarInfo> varInfo, TString option){
	const unsigned int Nmass = tmpMasspoints.size();
    double x[Nmass];
    double x_e[Nmass];
    double Mean[Nmass];
    double MeanE[Nmass];
	for(int i = 0; i < Nmass; i++){
		x[i] = tmpMasspoints[i];
		x_e[i] = 0;
	}  
	int Npar = nPar - varInfo.size();

	std::vector<TGraphErrors*> gs;

    	
    
    	for(int iPar = 0; iPar < Npar; iPar++){
    		stringstream S;
    		TGraphErrors * g = 0;
    		bool exist = true;
       		for(int i = 0; i < Nmass; i++){
        	    S.str("");
      	    	S << ParNames[iPar] <<"_M" <<tmpMasspoints[i];
        	    cout << S.str().c_str() << endl;
        	    if (((RooRealVar*) fr->floatParsFinal().find(S.str().c_str())) != NULL){
        	    	cout<<"Parameter "<<S.str().c_str() << " found" <<endl;
        	    	Mean[i] = ((RooRealVar*) fr->floatParsFinal().find(S.str().c_str()))->getVal();
        	    	MeanE[i] = ((RooRealVar*) fr->floatParsFinal().find(S.str().c_str()))->getError();
        	    } else {
        	    	cout<<"Parameter "<<S.str().c_str() << " NOT found" <<endl;
        	    	exist = false;
        	    	//Mean[i] = 0;
        	    	//MeanE[i] = 0;        	    
        	    }
        	    cout<< Mean[i]<<endl;
        	}
        	if(exist){
	        	g = new TGraphErrors(Nmass, x, Mean, x_e, MeanE);
    	    	g->SetNameTitle(ParNames[iPar], ParNames[iPar]);
    	    	gs.push_back(g);
    	    }
    	}
    	
    	for(unsigned int iPar = 0; iPar < varInfo.size(); iPar++){
    		cout << "--- "<<iPar <<" "<<varInfo[iPar].name <<endl;
       	    if(varInfo[iPar].isFixed) continue;
    		stringstream S;
    		TGraphErrors * g = 0;
       		for(int i = 0; i < Nmass; i++){
        	    S.str("");
        	    if(!varInfo[iPar].isCommon)
      	    		S << varInfo[iPar].name <<"_M" <<tmpMasspoints[i];
      	    	else 
      	    		S << varInfo[iPar].name;
        	    cout << S.str().c_str() << endl;
        	    if (((RooRealVar*) fr->floatParsFinal().find(S.str().c_str())) != NULL){
        	    	Mean[i] = ((RooRealVar*) fr->floatParsFinal().find(S.str().c_str()))->getVal();
        	    	MeanE[i] = ((RooRealVar*) fr->floatParsFinal().find(S.str().c_str()))->getError();
        	    } else {
        	    	Mean[i] = 0;
        	    	MeanE[i] = 0;        	    
        	    }
        	    cout<< Mean[i]<<endl;
        	}
        	g = new TGraphErrors(Nmass, x, Mean, x_e, MeanE);
        	g->SetNameTitle(varInfo[iPar].name, varInfo[iPar].name);
        	gs.push_back(g);   	
    	}
    	
    
    TCanvas * C = new TCanvas("ParaEvolution", "ParaEvolution",0,0,700,500);
    C->Divide(4,2);
    for(int iPar = 0; iPar < gs.size(); iPar ++){
    	C->cd(iPar+1);    
    	cout<<gs[iPar]->GetName()<<endl;
    	gs[iPar]->Draw("apl");
    }	
    C->SaveAs("ParaEvolution"+option+".C");
}

void DrawPostFitMasses(RooRealVar * mass, RooDataSet * combDataWeighted, RooSimultaneous * simPdfWeighted, RooCategory * sampleWeighted, std::vector<TString> massPointsStr, TString option = "", TString sys = "", int nBin=110){
	cout << "DrawFitComponentsPerSample --------------------- " << endl;
	
	std::vector<RooPlot*> frames;
	for(unsigned int i = 0; i < massPointsStr.size(); i++){
		RooPlot * frame = mass->frame(Name(massPointsStr[i] + "_frame"),  Title(massPointsStr[i] +" GeV sample"));
		combDataWeighted->plotOn(frame, DataError(RooAbsData::SumW2), Cut("sampleWeighted==sampleWeighted::sample" + massPointsStr[i]), RooFit::Binning(nBin));
    	simPdfWeighted->plotOn(frame, Slice(*sampleWeighted, "sample" + massPointsStr[i]), ProjWData(*sampleWeighted, *combDataWeighted));
    	simPdfWeighted->plotOn(frame, Slice(*sampleWeighted, "sample" + massPointsStr[i]), Components("tmp_M" + massPointsStr[i]), ProjWData(*sampleWeighted, *combDataWeighted), LineStyle(kDashed));
    	simPdfWeighted->plotOn(frame, Slice(*sampleWeighted, "sample" + massPointsStr[i]), Components("cball_M" + massPointsStr[i]), ProjWData(*sampleWeighted, *combDataWeighted), LineStyle(kDashed), LineColor(kRed));	
    	frames.push_back(frame);	
	}

	const unsigned int nPoints = massPointsStr.size(); 
    TCanvas* c = new TCanvas("SimultaneousFit", "SimultaneousFit", 1600, 800);
    if(nPoints % 2 == 0)
    	c->Divide(nPoints/2,2);
    else
    	c->Divide(1 + (nPoints/2),2);
    for(unsigned int iM = 0; iM < nPoints; iM++){
    	c->cd(iM+1);
		gPad->SetLeftMargin(0.05);
		frames[iM]->GetYaxis()->SetTitleOffset(0.9);
		frames[iM]->Draw();    
    }
    c->SaveAs(sys + "PostFitMasses" + option + ".C");
}


