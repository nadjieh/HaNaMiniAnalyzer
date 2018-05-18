#include <iostream>
#include <sstream>
#include <string>

#include "TFile.h"
#include "TArrow.h"
#include "TH1D.h"
#include "TProfile.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TString.h"
#include "TStyle.h"
#include "TChain.h"
#include "TH2.h"
#include "TH1.h"
#include "TF1.h"
#include "TTree.h"
#include "TKey.h"
#include "Riostream.h"
#include "TMath.h"
#include "TRandom.h"
#include "TRandom3.h"
#include "TVirtualFitter.h"
#include "RooMsgService.h"
#include "RooExtendPdf.h"
#include "RooWorkspace.h"
#include "RooChebychev.h"
#include "RooExponential.h"
#include <stdio.h>
#include <math.h>
#include "ForFtest.h"

int main(int argc, char** argv) {
    using namespace RooFit;
    using namespace std;
    RooMsgService::instance().setGlobalKillBelow(RooFit::FATAL);
    int nbins = 50;
    int dop = 1;
    double minpar = -10.;
    double maxpar = 10.;
    double mL = 20.;
    double mH = 63.;
    vector<double> degrees;
    int inv = 0;
    TString inputFileName = "";
    for (int f = 1; f < argc; f++) {
        string arg_fth(*(argv + f));
        if (arg_fth == "nBins") {
            f++;
            string in(*(argv + f));
            nbins = atof(in.c_str());
        } else if (arg_fth == "degree") {
            f++;
            string in(*(argv + f));
            dop = atof(in.c_str());
        } else if (arg_fth == "minpar") {
            f++;
            string in(*(argv + f));
            minpar = atof(in.c_str());
        } else if (arg_fth == "maxpar") {
            f++;
            string in(*(argv + f));
            maxpar = atof(in.c_str());
        } else if (arg_fth == "lowmass") {
            f++;
            string in(*(argv + f));
            mL = atof(in.c_str());
        } else if (arg_fth == "highmass") {
            f++;
            string in(*(argv + f));
            mH = atof(in.c_str());
        } else if (arg_fth == "vdop") {
            f++;
            string in(*(argv + f));
            degrees.push_back(atof(in.c_str()));
        } else if (arg_fth == "inversePdf") {
            f++;
            string in(*(argv + f));
            inv = atof(in.c_str());
	    std::cout<<"Inv is "<<inv<<std::endl;
        } else if (arg_fth == "input") {
            f++;
            string in(*(argv + f));
            inputFileName = in.c_str();
        }
    }
    stringstream s;
    TString name = "";
    TCanvas * c = 0;
    gErrorIgnoreLevel = kError;
    RooRealVar * aMuMass = new RooRealVar("aMuMass", "aMuMass", mL, mH);
    TFile * input = TFile::Open(inputFileName);
    TTree * tree = (TTree*) input->Get("Hamb/Trees/Events");
    RooDataSet * data = new RooDataSet("ControlData", "The original control data", tree, *aMuMass, "");
    RooDataHist * dataHist = 0;
    RooWorkspace * w = 0;
    TString Name ="";
    if (inv == 0){
        w = new RooWorkspace("WS", "WS");
	Name ="gen.root";
    } else if (inv == 1){
        w = new RooWorkspace("InvWS", "InvWS");
	Name = "Inv.root";
    } else if (inv == 2){
        w = new RooWorkspace("ChebWS", "ChebWS");
	Name = "Cheb.root";
    } else if (inv == 3){
	std::cout<<"BERN"<<std::endl;
	Name = "bern.root";
        w = new RooWorkspace("BernWS", "BernWS");
    }
    w->import(*data);
    w->import(*aMuMass);
    std::vector<double> probs;
    std::vector<double> nlls;
    TGraph * gNLL = new TGraph(degrees.size()-1);
    gNLL->SetName("NLLProb");
    TGraph * gChi2 = new TGraph(degrees.size());
    gChi2->SetName("Chi2");

    for (unsigned int i = 0; i < degrees.size(); i++) {
        dop = degrees[i];
        cout << "================ Degree: " << dop << endl;
        Ttest mytest("test", nbins, dop, aMuMass, data, minpar, maxpar);
        mytest.getTtest(inv);
        mytest.Print(inv);
        if (i == 0) {
            dataHist = new RooDataHist("hist", "hist", *aMuMass, (TH1D*) mytest.getDataHist());
            w->import(*dataHist);
        }
        bool keep = mytest.keepPdf(inv);
	if (keep) {
            RooAbsPdf * genPdf;
            if (inv == 0)
                genPdf = mytest.getFinalPolynomial();
            else if (inv == 1)
                genPdf = mytest.getFinalInvPolynomial();
            else if (inv == 2)
                genPdf = mytest.getFinalChebychev();
            else if (inv == 3)
		genPdf = mytest.getFinalBernstein();
            s.str("");
            s << "n_" << dop;
            name = s.str().c_str();
            RooRealVar * n = new RooRealVar(name, name, tree->GetEntries(), 0, 2 * tree->GetEntries());
            s.str("");
            s << "pdfext_" << dop;
            name = s.str().c_str();
            RooExtendPdf * pdfext = new RooExtendPdf(name, name, *genPdf, *n);
            pdfext->fitTo(*data, Save());
            w->import(*n);
            w->import(*genPdf);
            w->import(*pdfext);
            if (inv == 0)
                w->writeToFile("ws.root");
            else if (inv == 1)
                w->writeToFile("wsInv.root");
            else if (inv == 2)
                w->writeToFile("wsChb.root");
            else if (inv == 3)
                w->writeToFile("wsBern.root");
            RooPlot * P = aMuMass->frame();
            data->plotOn(P, Binning(nbins));
            pdfext->plotOn(P);
            s.str("");
            if (inv == 0)
                s << "gen_" << dop;
            else if (inv == 1)
                s << "invx_" << dop;
            else if (inv == 2)
                s << "cheb_" << dop;
            else if (inv == 3)
                s << "bern_" << dop;
            name = s.str().c_str();
            c = new TCanvas(name, name, 600, 800);
            c->cd();
            P->Draw();
            name = name + ".C";
            c->SaveAs(name);
	}
	cout<<">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> With NLL Cross Check:"<<endl;
	double nll = mytest.getNLL(inv);
	cout<<">>>>>>> dop: "<< nll <<endl;
	nlls.push_back(nll);
	
        if(i > 0){
	  probs.push_back(TMath::Prob(2*(nlls[nlls.size()-2] - nlls[nlls.size()-1]),1));
	  gNLL->SetPoint(i-1,i,probs[probs.size()-1]);
	}	
	double chi2 = mytest.getChi2(inv);
	gChi2->SetPoint(i, i+1, chi2);
    }
    for(unsigned int i = 0; i < probs.size(); i++){
      cout<<"degree "<<degrees[i+1] <<" vs degree "<< degrees[i] <<": "<<probs[i]<<endl;
    }
    cout<<"=============================>>>>>>>>> Chi2s:"<<endl;
    for(unsigned int i = 0; i < degrees.size();i++){
      double x,y;
      gChi2->GetPoint(i,x,y);
      cout<<"degree "<<degrees[i]<<": "<<y<<endl;
    }
    TFile * f = new TFile(Name,"recreate");
    f->cd();
    gNLL->Write();
    gChi2->Write();
    /*dop = 6;

    RooRealVar a0("a0", "a0", 30., 10., 50.);
    RooRealVar a1("a1", "a1", -100., 100.);
    RooRealVar a2("a2", "a2", -10., 10.);
    RooRealVar a3("a3", "a3", -10., 10.);
    //    RooRealVar a4("a4", "a4", -10., 10.);
    RooGenericPdf ch("ch", "ch", "(aMuMass-a0)^4-(a1*(aMuMass-a0)^2)", RooArgSet(*aMuMass, a0, a1));
    ch.fitTo(*dataHist);
    RooPlot * Pexp = aMuMass->frame();
    dataHist->plotOn(Pexp);
    ch.plotOn(Pexp);
    s.str("");
    s << "poly_" << dop;
    name = s.str().c_str();
    c = new TCanvas(name, name, 600, 800);
    c->cd();
    Pexp->Draw();
    name = name + ".C";
    c->SaveAs(name);*/
    return 1;
}
