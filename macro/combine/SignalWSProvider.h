/* 
 * File:   SignalWSProvider.h
 * Author: nadjieh
 *
 * Created on May 24, 2015, 2:22 PM
 */

#ifndef SIGNALWSPROVIDER_H
#define	SIGNALWSPROVIDER_H
#include <iostream>
#include <sstream>
#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooExponential.h"
#include "RooConstVar.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "RooBernstein.h"
#include "RooSimultaneous.h"
#include "RooFitResult.h"
#include "RooCategory.h"
#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include <vector>
#include <sstream>
#include <iostream>
#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooFitResult.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1.h"
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
#include "RooWorkspace.h"
#include <fstream>
#include "RooCategory.h"
#include "RooWorkspace.h"
#include "RooRandom.h"
#include "../interface/RooMultiPdf.h"
#include <iostream>
#include <sstream>
#include <vector>
#include "TFile.h"
#include "TArrow.h"
#include "TPaveText.h"
#include "TLatex.h"
#include "TH1D.h"
#include "TProfile.h"
#include "TCanvas.h"
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
#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooPolynomial.h"
#include "RooExponential.h"
#include "RooArgList.h"
#include "RooGenericPdf.h"
#include "RooExtendPdf.h"
#include "RooFitResult.h"
#include "RooChebychev.h"
#include "RooDataHist.h"
#include "RooVoigtian.h"
#include "RooPlot.h"
#include <stdio.h>
#include <math.h>
#include <map>
typedef std::map<TString, std::pair<double, std::pair<double, double> > > MeanErr;
typedef std::map<TString, double> FixedParams;

using namespace std;
using namespace RooFit;

class SignalWSProvider {
public:

    SignalWSProvider(MeanErr systYield, FixedParams fixed_, double UncSig) : sigNormUnc(UncSig) {
        RooRandom::randomGenerator()->SetSeed(35);
        for (auto& x : systYield) {
            MeanErrors[x.first] = make_pair(x.second.first, make_pair(x.second.second.first, x.second.second.second));
        }

        for (auto& x : fixed_) {
            Fixeds[x.first] = x.second;
        }
        w = new RooWorkspace("w", "w");
        var = new RooRealVar("aMuMass", "aMuMass", 20, 70);
        w->import(*var);
        w->factory("MH[20,70]");
	(w->var("MH"))->setConstant();
        w->factory("Br[0.00017,-0.1,0.1]");
        w->factory("Sigma[19.3,10,30]");
	//if(sigNormUnc != 0)	
	//	(w->var("Sigma"))->setConstant();
	w->factory("IL[19700]");
        w->factory("y0[0.102448]");
        w->factory("y1[-0.0026199]");
        w->factory("y2[3.39914e-05]");
        w->factory("FormulaVar::efficiency(\"@1+(@2*@0)+(@3*TMath::Power(@0,2))\",{MH,y0,y1,y2})");
	w->factory("FormulaVar::signal_norm(\"@0*@1*@2*@3\",{Sigma,Br,IL,efficiency})");

        stringstream s;
        s << Fixeds["alpha"];
        TString Val = s.str().c_str();
        w->factory("alpha[" + Val + "]");

        s.str("");
        s << Fixeds["n"];
        Val = s.str().c_str();
        w->factory("n[" + Val + "]");

        s.str("");
        s << Fixeds["width"];
        Val = s.str().c_str();
        w->factory("width[" + Val + "]");

        s.str("");
        s << Fixeds["frac"];
        Val = s.str().c_str();
        w->factory("frac[" + Val + "]");

        s.str("");
        s << MeanErrors["a1"].first;
        Val = s.str().c_str();
        w->factory("a1[" + Val + ",0 , 0.5]");

	cout<<"a1: "<<Val<<endl;
        s.str("");
        s << MeanErrors["b1"].first;
        Val = s.str().c_str();
        w->factory("b1[" + Val + ",0 , 0.1]");

	cout<<"b1: "<<Val<<endl;
        s.str("");
        s << MeanErrors["m1"].first;
        Val = s.str().c_str();
	cout<<"m1: "<<Val<<endl;
        w->factory("m1[" + Val + ",0 , 0.1]");

	w->factory("FormulaVar::mean(\"@1+@0\",{MH,m1})");
	w->factory("FormulaVar::sigma_cb(\"0.017+@1*@0\",{MH,b1})");
	w->factory("FormulaVar::sigma(\"0.02+@1*@0\",{MH,a1})");
        //        Yield = new TF1("Yield", " 5.80131+(x*-0.138701)+(x*x*0.00187576)", 20, 70);
        w->factory("RooCBShape::CB(aMuMass, mean, sigma_cb, alpha, n)");
        w->factory("RooVoigtian::Voig(aMuMass, mean, width, sigma)");
        w->factory("RooAddPdf::signal(Voig,CB,frac)");

    };

    void BackgroundConstructor(double myBkg) {
        RooCategory pdfindex("pdfindex", "c");

        RooArgList storedPdfs("store");

        RooDataHist * dataHist = 0;
        stringstream poly;

        //PolyNomial
        TFile * fpoly = TFile::Open("ws.root");
        if (fpoly != NULL) {
            cout << "Polynomial is included" << endl;
            RooWorkspace * WS = (RooWorkspace*) fpoly->Get("WS");
            dataHist = (RooDataHist*) WS->data("hist");
            w->import(*dataHist);
            for (int x = 0; x < 30; x++) {
                poly.str("");
                poly << "PolyPdf_" << x;
                TString PolyName = poly.str().c_str();
                RooPolynomial * pdf = (RooPolynomial*) WS->pdf(PolyName);
                if (pdf == NULL)
                    continue;
                cout << "************************************" << PolyName << " *******************" << endl;
                RooRealVar * myvar = (RooRealVar*) WS->var("p21");
                cout << myvar->getVal() << "\tMin: " << myvar->getMin() << "\tMax: " << myvar->getMax() << "\tErrL: " << myvar->getErrorLo() << "\tErrH: " << myvar->getErrorHi() << endl;
                //pdf->fitTo(*dataHist);
                storedPdfs.add(*pdf);
            }
        }

        //Chebychev in case one of the two above fail
        TFile * fcheb = TFile::Open("wsChb.root");
        if (fcheb != NULL) {
            RooWorkspace * ChebWS = (RooWorkspace*) fcheb->Get("ChebWS");
            for (int x = 0; x < 30; x++) {
                poly.str("");
                poly << "Chebychev_" << x;
                TString PolyName = poly.str().c_str();
                RooChebychev * pdf = (RooChebychev*) ChebWS->pdf(PolyName);
                if (pdf == NULL)
                    continue;
                cout << "************************************" << PolyName << " *******************" << endl;
                if (dataHist == 0) {
                    dataHist = (RooDataHist*) ChebWS->data("hist");
                }
                pdf->fitTo(*dataHist);
                storedPdfs.add(*pdf);
            }

        }

        //Inverted PolyNomial
        TFile * finvpoly = TFile::Open("wsInv.root");
        if (finvpoly != NULL) {
            RooWorkspace * InvWS = (RooWorkspace*) finvpoly->Get("InvWS");
            for (int x = 0; x < 30; x++) {
                poly.str("");
                poly << "InvPolyPdf_" << x;
                TString PolyName = poly.str().c_str();
                RooGenericPdf * pdf = (RooGenericPdf*) InvWS->pdf(PolyName);
                if (pdf == NULL)
                    continue;
                cout << "************************************" << PolyName << " *******************" << endl;
                if (dataHist == 0) {
                    dataHist = (RooDataHist*) InvWS->data("hist");
                }
                pdf->fitTo(*dataHist);
                storedPdfs.add(*pdf);
            }
        }
        //Bernstein 
        TFile * fbern = TFile::Open("wsBern.root");
        if (fbern != NULL) {
            RooWorkspace * BernWS = (RooWorkspace*) fbern->Get("BernWS");
            cout << "--------------------  " << BernWS << endl;
            for (int x = 0; x < 30; x++) {
                poly.str("");
                poly << "Bernstein_" << x;
                TString PolyName = poly.str().c_str();
                RooBernstein * pdf = (RooBernstein*) BernWS->pdf(PolyName);
                if (pdf == NULL)
                    continue;
                cout << "************************************" << PolyName << " *******************" << endl;
                if (dataHist == 0) {
                    dataHist = (RooDataHist*) BernWS->data("hist");
                }
                pdf->fitTo(*dataHist);
                storedPdfs.add(*pdf);
            }

        }

        RooMultiPdf multipdfsbkg("bkgshape", "", pdfindex, storedPdfs);
        w->import(multipdfsbkg);
        stringstream NBKG;
        NBKG << myBkg << ", 0, " << 2 * myBkg;
        TString bkgName_ = NBKG.str().c_str();
        w->factory("bkgshape_norm[" + bkgName_ + "]");
    }

    void cardMaker() {
        stringstream Mass_;
        if (sigNormUnc == 0)
            Mass_ << "SignalSigmaBr";
        else
            Mass_ << "SignalBr";

        TString Val = Mass_.str().c_str();
        TString outname = "hamb_shape_"+Val+"_ws.txt";
        int N = MeanErrors.size() + YieldErrors.size();
        int I = 1;
        if (sigNormUnc == 0)
            I = 1;
        ofstream myfile;
        myfile.setf(ios_base::fixed);
        myfile.precision(4);

        myfile.open(outname);
        myfile << "imax 1" << endl;
        myfile << "jmax 1  number of backgrounds" << endl;
        myfile << "kmax " << N + I << "  number of nuisance parameters (sources of systematical uncertainties)" << endl;

        myfile << "\n------------" << endl;
        myfile << "shapes\tsignal\tdimu\thamb-shapes-UnbinnedParam-" + Val + "-Data-fit.root w:signal" << endl; //$PROCESS_$CHANNEL w:$PROCESS_$CHANNEL_$SYSTEMATIC" << endl;
        myfile << "shapes\tbkg\tdimu\thamb-shapes-UnbinnedParam-" + Val + "-Data-fit.root w:bkgshape" << endl;
        myfile << "shapes\tdata_obs\tdimu\thamb-shapes-UnbinnedParam-" + Val + "-Data-fit.root w:data" << endl;
        myfile << "------------" << endl;
        myfile << "bin\tdimu" << endl;
        myfile << "observation\t-1.0" << endl;
        myfile << "------------" << endl;
        myfile << "bin\tdimu\tdimu" << endl;
        myfile << "process\tsignal\tbkg" << endl;
        myfile << "process\t0\t1" << endl;
        myfile << "rate\t1.0\t1.0" << endl;
        myfile << "------------" << endl;
        myfile << "lumi_8TeV\tlnN\t1.026\t-" << endl;
        //if (sigNormUnc != 0)
        //    myfile << "signalTHunc\tlnN\t" << 1 + sigNormUnc << "\t-" << endl;
        for (auto& x : YieldErrors) {
	    if(x.second.first == x.second.second )
		myfile << x.first << "\tlnN\t" << x.second.first << "\t-" << endl;
	    else
		myfile << x.first << "\tlnN\t" << x.second.first << "/" << x.second.second << "\t-" << endl;
        }
        for (auto& x : MeanErrors) {
	    if(x.second.second.first == x.second.second.second )
		myfile << x.first << "\tparam\t" << x.second.first << "\t"<<x.second.second.first << endl;
	    else
		myfile << x.first << "\tparam\t" << x.second.first << "\t" << x.second.second.first << "/+" << x.second.second.second << endl;
        }
	myfile <<"Sigma\tparam\t19.3\t0.13"<<endl;
        myfile << "pdfindex\tdiscrete" << endl;
        myfile.close();
    }

    void YieldSystMaker() {
        YieldErrors["btag"] = make_pair(0.969, 1.031);
        YieldErrors["JES"] = make_pair(0.934, 1.065);
        YieldErrors["JER"] = make_pair(1.005, 0.998);
        YieldErrors["muon"] = make_pair(0.958, 1.042);
        YieldErrors["pileup"] = make_pair(0.959, 0.959);
        YieldErrors["PDF"] = make_pair(0.989, 1.008);
    }

    void WriteWS(bool blind = true) {
	TFile * f = 0;
	if(!blind)
		f = new TFile("DoubleMu2012_Summer12_final_4_4.root", "READ");
	else
        	f = new TFile("DoubleMu2012_Summer12_final_CR_4_4.root", "READ");
        TTree* hh = (TTree*) f->Get("rds_zbb");
        RooDataSet data("data", "data", hh, *var, "");
        w->import(data);
        //TH1D * hData = (TH1D*) data.createHistogram("data_obs", *var, Binning(50));
        //double frac_ = (double) hData->Integral() / (double) 50;
        //this->BackgroundConstructor(hData->Integral() - (2 * frac_));
        this->BackgroundConstructor(hh->GetEntries());
        this->YieldSystMaker();
        this->cardMaker();


        stringstream S;
        //S << mass;
        if (sigNormUnc == 0)
            S << "SignalSigmaBr";
        else
            S << "SignalBr";
        TString fname = S.str().c_str();
        fname = "hamb-shapes-UnbinnedParam-" + fname + "-Data-fit.root";
        w->writeToFile(fname);
    }

    virtual ~SignalWSProvider() {
    };
private:
    double sigNormUnc;
    FixedParams Fixeds;
    MeanErr MeanErrors;
    std::map<TString, std::pair <double, double> > YieldErrors;
    RooRealVar * var;
    RooWorkspace * w;
};

#endif	/* SIGNALWSPROVIDER_H */

