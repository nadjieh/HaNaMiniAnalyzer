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
#include "RooChebychev.h"
#include "RooPolynomial.h"
#include "RooArgList.h"
#include "RooBernstein.h"
#include "RooGenericPdf.h"
#include "RooExtendPdf.h"
#include "RooFitResult.h"
#include "RooDataHist.h"
#include "RooPlot.h"
#include "RooNLLVar.h"
#include "RooMinuit.h"
#include "RooChi2Var.h"
#include <stdio.h>
#include <math.h>
using namespace RooFit;
using namespace std;

class Ttest {
public:

    Ttest(TString name_, int Nbins_, int dop, RooRealVar * var_, RooDataSet * data_, double parmin_ = -100.,
            double parmax_ = 100.) : name(name_), Nbins(Nbins_), degreeOfPolyNom(dop), parmin(parmin_), parmax(parmax_) {
        var = var_;
        data = data_;
        hdata = (TH1D*) data->createHistogram("hdata", *var, RooFit::Binning(Nbins));
        Ndata = data->sumEntries(0);
        COs[1] = 12.7065;
        COs[2] = 4.3026;
        COs[3] = 3.1824;
        COs[4] = 2.7764;
        COs[5] = 2.5706;
        COs[6] = 2.4469;
        COs[7] = 2.3646;
        COs[8] = 2.306;
        COs[9] = 2.2621;
        COs[10] = 2.2282;
        COs[11] = 2.201;
        COs[12] = 2.1788;
        COs[13] = 2.1604;
        COs[14] = 2.1448;
        COs[15] = 2.1314;
        COs[16] = 2.1199;
        COs[17] = 2.1098;
        COs[18] = 2.1009;
        COs[19] = 2.093;
        COs[20] = 2.086;
        COs[21] = 2.0796;
        COs[22] = 2.0739;
        COs[23] = 2.0686;
        COs[24] = 2.0639;
        COs[25] = 2.0596;
        COs[26] = 2.0555;
        COs[27] = 2.0518;
        COs[28] = 2.0484;
        COs[29] = 2.0452;
        COs[30] = 2.0423;
        COs[31] = 2.0395;
        COs[32] = 2.0369;
        COs[33] = 2.0345;
        COs[34] = 2.0322;
        COs[35] = 2.0301;
        COs[36] = 2.0281;
        COs[37] = 2.0262;
        COs[38] = 2.0244;
        COs[39] = 2.0227;
        COs[40] = 2.0211;
        COs[41] = 2.0196;
        COs[42] = 2.0181;
        COs[43] = 2.0167;
        COs[44] = 2.0154;
        COs[45] = 2.0141;
        COs[46] = 2.0129;
        COs[47] = 2.0117;
        COs[48] = 2.0106;
        COs[49] = 2.0096;
        COs[50] = 2.0086;
        COs[51] = 2.0076;
        COs[52] = 2.0066;
        COs[53] = 2.0057;
        COs[54] = 2.0049;
        COs[55] = 2.0041;
        COs[56] = 2.0032;
        COs[57] = 2.0025;
        COs[58] = 2.0017;
        COs[59] = 2.001;
        COs[60] = 2.0003;
        COs[61] = 1.9996;
        COs[62] = 1.999;
        COs[63] = 1.9983;
        COs[64] = 1.9977;
        COs[65] = 1.9971;
        COs[66] = 1.9966;
        COs[67] = 1.996;
        COs[68] = 1.9955;
        COs[69] = 1.995;
        COs[70] = 1.9944;
        COs[71] = 1.9939;
        COs[72] = 1.9935;
        COs[73] = 1.993;
        COs[74] = 1.9925;
        COs[75] = 1.9921;
        COs[76] = 1.9917;
        COs[77] = 1.9913;
        COs[78] = 1.9909;
        COs[79] = 1.9904;
        COs[80] = 1.9901;
        COs[81] = 1.9897;
        COs[82] = 1.9893;
        COs[83] = 1.9889;
        COs[84] = 1.9886;
        COs[85] = 1.9883;
        COs[86] = 1.9879;
        COs[87] = 1.9876;
        COs[88] = 1.9873;
        COs[89] = 1.987;
        COs[90] = 1.9867;
        COs[91] = 1.9864;
        COs[92] = 1.9861;
        COs[93] = 1.9858;
        COs[94] = 1.9855;
        COs[95] = 1.9852;
        COs[96] = 1.985;
        COs[97] = 1.9847;
        COs[98] = 1.9845;
        COs[99] = 1.9842;
        COs[100] = 1.984;
    }

    ~Ttest() {
    }

    RooPolynomial * pol() {
        if (degreeOfPolyNom == 0) {
            RooPolynomial * ret = new RooPolynomial(name + "_pol0", name + "_pol0", *var, RooArgList());
            RooPlot * p = var->frame();
            ret->plotOn(p);
            TCanvas c;
            p->Draw();
            c.SaveAs("a0.C");
            return ret;
        }
        RooArgList * pars = new RooArgList("pars");
        stringstream s;
        for (int i = 1; i < degreeOfPolyNom + 1; i++) {
            s.str("");
            s << "p" << degreeOfPolyNom << i;
            TString S = s.str().c_str();
            RooRealVar * par = new RooRealVar(S, S, parmin, parmax);
            cout << par->GetName() << endl;
            pars->add(*par);
        }
        s.str("");
        s << name + "_pol" << degreeOfPolyNom;
        TString S = s.str().c_str();
        RooPolynomial * ret = new RooPolynomial(S, S, *var, *pars);
        RooPlot * p = var->frame();
        ret->plotOn(p);
        TCanvas c;
        p->Draw();
        c.SaveAs("a.C");
        return ret;

    }

    RooGenericPdf * invPol() {
        TString formul = TString("1/(1 ") /*+ TString(var->GetName())*/;
        if (degreeOfPolyNom == 0) {
            cout << "FATAL ERROR: inverse polynomial for degree 0 is not supported" << endl;
            return 0;
        }
        RooArgList * pars = new RooArgList("pars");
        pars->add(*var);
        stringstream s;
//        if (degreeOfPolyNom != 1) {
            for (int i = 1; i < degreeOfPolyNom + 1; i++) {
                stringstream s2;
                s2 << "inva" << degreeOfPolyNom << i;
                TString parname = s2.str().c_str();
                RooRealVar * a = new RooRealVar(parname, parname, -10., 10.);
                pars->add(*a);
                s << "+inva" << degreeOfPolyNom << i << "*" << var->GetName() << "^" << i;
            }
//        }
        TString formul2 = s.str().c_str();
        formul = formul + formul2 + ")";
        cout << formul << endl;
        cout << pars->getSize() << endl;
        s.str("");
        s << "invPdf_" << degreeOfPolyNom;
        formul2 = s.str().c_str();
        RooGenericPdf * invPdf = new RooGenericPdf(formul2, formul2, formul, *pars);
        return invPdf;
    }

    RooChebychev * chebychev() {

        RooArgList * pars = new RooArgList("pars");
        stringstream s;
        for (int i = 0; i < degreeOfPolyNom + 1; i++) {
            s.str("");
            s << "c" << degreeOfPolyNom << i;
            TString S = s.str().c_str();
            RooRealVar * par = new RooRealVar(S, S, parmin, parmax);
            cout << par->GetName() << endl;
            pars->add(*par);
        }
        s.str("");
        s << name + "_chb" << degreeOfPolyNom;
        TString S = s.str().c_str();
        RooChebychev * ret = new RooChebychev(S, S, *var, *pars);
        return ret;

    }


    RooBernstein * bern() {

        RooArgList * pars = new RooArgList("pars");
        stringstream s;
        for (int i = 0; i < degreeOfPolyNom + 1; i++) {
            s.str("");
            s << "bern" << degreeOfPolyNom << i;
            TString S = s.str().c_str();
            RooRealVar * par = new RooRealVar(S, S, 0, 0.1);
            cout << par->GetName() << endl;
            pars->add(*par);
        }
        s.str("");
        s << name + "_bern" << degreeOfPolyNom;
        TString S = s.str().c_str();
        RooBernstein * ret = new RooBernstein(S, S, *var, *pars);
        return ret;

    }


    //NLL based F-test
    double getChi2(int inv = 0){
      RooAbsPdf * p = 0;
      if (inv == 0)
        p = this->pol();
      else if (inv == 1)
        p = this->invPol();
      else if (inv == 2)
        p = this->chebychev();
      else if (inv == 3)
        p = this->bern();
      RooDataHist datahistChi("datahistChi", "datahistChi", RooArgSet(*var), hdata);
      RooRealVar n("n", "n", 0., 2 * Ndata);
      RooExtendPdf pext("pext", "pext", *p, n);
      RooChi2Var chi2("chi2","chi2",pext,datahistChi) ;
      RooMinuit m(chi2) ;
      m.migrad() ;
      m.hesse() ;
      RooFitResult* r = m.save() ;
      cout << "result of chi2 fit" << endl ;
      //r3->Print("v") ;
      return chi2.getVal()/Nbins;
    }
    double getNLL(int inv = 0){
      RooAbsPdf * p = 0;
      if (inv == 0)
        p = this->pol();
      else if (inv == 1)
        p = this->invPol();
      else if (inv == 2)
        p = this->chebychev();
      else if (inv == 3)
        p = this->bern();
      RooRealVar n("n", "n", 0., 2 * Ndata);
      RooExtendPdf pext("pext", "pext", *p, n);
      RooNLLVar nll("nll","nll",pext,*data) ;
      RooMinuit m(nll) ;
      m.migrad() ;
      m.hesse() ;
      RooFitResult* r1 = m.save() ;
      cout << "result of binned likelihood fit" << endl ;
      r1->Print("v") ;
      cout<<r1->minNll()<<endl;      
      return r1->minNll();
    }


    void getTtest(int inv = 0) {//0: pol, 1: inv, 2: chb
      RooAbsPdf * p = 0;
      if (inv == 0)
	p = this->pol();
      else if (inv == 1)
	p = this->invPol();
      else if (inv == 2)
	p = this->chebychev();
      else if (inv == 3)
	p = this->bern();
      RooRealVar n("n", "n", 0., 2 * Ndata);
      RooExtendPdf pext("pext", "pext", *p, n);
      RooDataHist datahist("datahist", "datahist", RooArgSet(*var), hdata);
      RooFitResult* res = pext.fitTo(datahist, RooFit::Save());
      RooPlot * p2 = var->frame();
      data->plotOn(p2, Binning(Nbins));
      pext.plotOn(p2);
      TCanvas c;
      p2->Draw();
      stringstream fName;
      fName <<"Shape_"<<inv<<"_"<<degreeOfPolyNom<<"_fit.C";
      TString fNameStr = fName.str().c_str();
      c.SaveAs(fNameStr);
      if((inv == 0 && degreeOfPolyNom == 0) /*|| (inv == 1 && degreeOfPolyNom == 1)*/){
	cout << "I am here! "<<endl;
	TString S = "n";
	double ratio = n.getVal() / n.getError();
	cout << S <<": "<<ratio<<endl;
	ratios[S] = fabs(ratio);
	parVals[S] = n.getVal();
	parErrs[S] = n.getError();
	return;
      } 
      stringstream s;
      int N = degreeOfPolyNom;
      if (inv == 2 || inv == 3)
	N++;
      for (int i = 0; i < N; i++) {
	s.str("");
	if (inv == 0){
	  s << "p" << degreeOfPolyNom << i + 1;
	} else if (inv == 1) {
	  s << "inva" << degreeOfPolyNom << i + 1;//2;
	  if ((i + 1/*2*/) > degreeOfPolyNom)
	    continue;
	} else if (inv == 2) {
	  s << "c" << degreeOfPolyNom << i;
	} else if (inv == 3) {
                s << "bern" << degreeOfPolyNom << i;
	}
	TString S = s.str().c_str();
	RooRealVar* parI = (RooRealVar*) res->floatParsFinal().find(S);
	double ratio = parI->getVal() / parI->getError();
	ratios[S] = fabs(ratio);
	parVals[S] = parI->getVal();
	parErrs[S] = parI->getError();    
      }
    }

    void Print(int inv = 0) {//0: pol, 1: inv, 2: chb
        cout << "cut off is COs[" << Nbins - degreeOfPolyNom << "] = " << COs[Nbins - degreeOfPolyNom] << endl;
        stringstream s;
        cout << "Ratios size: "<<ratios.size() << endl;
        if((inv == 0 && degreeOfPolyNom == 0) /*|| (inv == 1 && degreeOfPolyNom == 1)*/){
	    cout << ratios["n"] <<"\t"<<COs[Nbins - degreeOfPolyNom] <<endl;
            if (ratios["n"] > COs[Nbins - degreeOfPolyNom]) {
                cout << "necessary -----" << endl;
                cout << parVals["n"] << ", " << parVals["n"] - 2 * parErrs["n"] << ", " << parVals["n"] + 2 * parErrs["n"] << endl;
            } else
                cout << "NOT necessary ////" << endl;
	    return;
	}
        for (int i = 0; i < ratios.size(); i++) {
            s.str("");
            if (inv == 0)
                s << "p" << degreeOfPolyNom << i + 1;
            else if (inv == 1) {
                s << "inva" << degreeOfPolyNom << i + 1;//2;
                if ((i + 1/*2*/) > degreeOfPolyNom)
                    continue;
            } else if (inv == 2) {
                s << "c" << degreeOfPolyNom << i;
            } else if (inv == 3) {
                s << "bern" << degreeOfPolyNom << i;
            }
            TString S = s.str().c_str();
            cout << S << endl;
            cout << S << ": " << ratios[S] << " which is ";
            if (ratios[S] > COs[Nbins - degreeOfPolyNom]) {
                cout << "necessary -----" << endl;
                cout << parVals[S] << ", " << parVals[S] - 2 * parErrs[S] << ", " << parVals[S] + 2 * parErrs[S] << endl;
            } else
                cout << "NOT necessary ////" << endl;
        }
    }

    RooPolynomial * getFinalPolynomial() {
	if(degreeOfPolyNom == 0){
	    return (new RooPolynomial("PolyPdf_0", "PolyPdf_0", *var, RooArgList()));
	}
        stringstream s;
        s << "PolyPdf_" << degreeOfPolyNom;
        TString Name = s.str().c_str();
        s.str("");
        RooArgList * Pars = new RooArgList("Pars");
        for (int i = 0; i < ratios.size(); i++) {
            s.str("");
            s << "p" << degreeOfPolyNom << i + 1;
            TString parName = s.str().c_str();
            RooRealVar * par = 0;
            if (ratios[parName] > COs[Nbins - degreeOfPolyNom]) {
                par = new RooRealVar(parName, "", parVals[parName], parVals[parName] - 2 * fabs(parErrs[parName]), parVals[parName] + 2 * fabs(parErrs[parName]));
            } else {
                par = new RooRealVar(parName, "", 0.);
            }
            Pars->add(*par);
        }
        if (Pars->getSize() == 0) {
            cout << "No parameter!" << endl;
            return 0;
        }
        RooPolynomial * ret = new RooPolynomial(Name, "", *var, *Pars);
        return ret;
    }

    RooChebychev * getFinalChebychev() {
        stringstream s;
        s << "Chebychev_" << degreeOfPolyNom;
        TString Name = s.str().c_str();
        s.str("");
        RooArgList * Pars = new RooArgList("Pars");
        for (int i = 0; i < ratios.size(); i++) {
            s.str("");
            s << "c" << degreeOfPolyNom << i;
            TString parName = s.str().c_str();
            RooRealVar * par = 0;
            if (ratios[parName] > COs[Nbins - degreeOfPolyNom]) {
                par = new RooRealVar(parName, "", parVals[parName], parVals[parName] - 10 * fabs(parErrs[parName]), parVals[parName] + 10 * fabs(parErrs[parName]));
            } else {
                par = new RooRealVar(parName, "", 0.);
            }
            Pars->add(*par);
        }
        if (Pars->getSize() == 0) {
            cout << "No parameter!" << endl;
            return 0;
        }
        RooChebychev * ret = new RooChebychev(Name, "", *var, *Pars);
        return ret;
    }

    RooBernstein * getFinalBernstein() {
        stringstream s;
        s << "Bernstein_" << degreeOfPolyNom;
        TString Name = s.str().c_str();
        s.str("");
        RooArgList * Pars = new RooArgList("Pars");
        for (int i = 0; i < ratios.size(); i++) {
            s.str("");
            s << "bern" << degreeOfPolyNom << i;
            TString parName = s.str().c_str();
            RooRealVar * par = 0;
            if (ratios[parName] > COs[Nbins - degreeOfPolyNom]) {
                par = new RooRealVar(parName, "", parVals[parName], 0, parVals[parName] + 100 * fabs(parErrs[parName]));
		cout<<"---- Final: "<<parVals[parName]<<"\t"<<parVals[parName] - 100 * fabs(parErrs[parName])<<"\t"<<parVals[parName] + 100 * fabs(parErrs[parName])<<endl;
            } else {
                par = new RooRealVar(parName, "", 0.);
            }
            Pars->add(*par);
        }
        if (Pars->getSize() == 0) {
            cout << "No parameter!" << endl;
            return 0;
        }
        RooBernstein * ret = new RooBernstein(Name, "", *var, *Pars);
        return ret;
    }


    bool keepPdf(int inv = 0) {//0: pol, 1: inv, 2: chb
        int sizeOfUnNecessary = 0;
        bool ret = true;
        stringstream s;
        cout<<"------>> "<<ratios.size()<<endl;
        if(inv == 0 && degreeOfPolyNom == 0){
	    if(ratios["n"] > COs[Nbins - degreeOfPolyNom]){
	    	cout << "I keep this polynom: " << degreeOfPolyNom << endl;
        	cout << " ----- " << endl;
            	return true;
	    }
	    return false;
        }

        for (int i = 0; i < ratios.size(); i++) {
            s.str("");
            if (inv == 1) {
                s << "inva" << degreeOfPolyNom << i + 2;
                if ((i + 2) > degreeOfPolyNom)
                    continue;
            } else if (inv == 0) {
                s << "p" << degreeOfPolyNom << i + 1;
            } else if (inv == 2) {
                s << "c" << degreeOfPolyNom << i;
            } else if (inv == 3) {
                s << "bern" << degreeOfPolyNom << i;
            }
            TString parName = s.str().c_str();
            if (!(ratios[parName] > COs[Nbins - degreeOfPolyNom])) {
                sizeOfUnNecessary++;
            }
        }
        if (inv == 1) {
            if (sizeOfUnNecessary >= (degreeOfPolyNom - 1)) {
                cout << "I don't keep this inverted polynom: " << degreeOfPolyNom << endl;
                return false;
            } else {
                int lastUnNecessary = 0;
                for (int i = degreeOfPolyNom; i > (degreeOfPolyNom - sizeOfUnNecessary); i--) {
                    s.str("");
                    s << "inva" << degreeOfPolyNom << i;
                    if (!(ratios[s.str().c_str()] > COs[Nbins - degreeOfPolyNom]))
                        lastUnNecessary++;
                }
                if (lastUnNecessary == sizeOfUnNecessary && (sizeOfUnNecessary != 0)) {
                    cout << "I don't keep this inverted polynom: " << degreeOfPolyNom << endl;
                    return false;
                }
            }
        } else if (inv == 0) {
            //            cout << ">>>>>>>>> Not inverted: " << endl;
            if (sizeOfUnNecessary >= degreeOfPolyNom) {
                cout << "I don't keep this polynom: " << degreeOfPolyNom << endl;
                return false;
            } else {
                int lastUnNecessary = 0;
                for (int i = degreeOfPolyNom; i > (degreeOfPolyNom - sizeOfUnNecessary); i--) {
                    s.str("");
                    s << "p" << degreeOfPolyNom << i;
                    if (!(ratios[s.str().c_str()] > COs[Nbins - degreeOfPolyNom]))
                        lastUnNecessary++;
                }
                //                cout << ">>>>>> N last unnecessary: " << lastUnNecessary << endl;
                if (lastUnNecessary == sizeOfUnNecessary && (sizeOfUnNecessary != 0)) {
                    cout << "I don't keep this polynom: " << degreeOfPolyNom << endl;
                    return false;
                }
            }
        } else if (inv == 2) {
            cout << sizeOfUnNecessary << endl;
            if (sizeOfUnNecessary > degreeOfPolyNom) {
                cout << "I don't keep this Chebychev: " << degreeOfPolyNom << endl;
                return false;
            } else {
                int lastUnNecessary = 0;
                for (int i = degreeOfPolyNom; i > (degreeOfPolyNom - sizeOfUnNecessary); i--) {
                    s.str("");
                    s << "c" << degreeOfPolyNom << i;
                    if (!(ratios[s.str().c_str()] > COs[Nbins - degreeOfPolyNom]))
                        lastUnNecessary++;
                }
                if (lastUnNecessary == sizeOfUnNecessary && (sizeOfUnNecessary != 0)) {
                    cout << "I don't keep this Chebychev: " << degreeOfPolyNom << endl;
                    return false;
                }
            }
        } else if (inv == 3) {
            cout << sizeOfUnNecessary << endl;
            if (sizeOfUnNecessary > degreeOfPolyNom) {
		cout << "size of unNecessary: "<<sizeOfUnNecessary<<"\t"<<degreeOfPolyNom<<endl;
                cout << "I don't keep this Bernstein:: " << degreeOfPolyNom << endl;
                return false;
            } else {
                int lastUnNecessary = 0;
                for (int i = degreeOfPolyNom; i > (degreeOfPolyNom - sizeOfUnNecessary); i--) {
                    s.str("");
                    s << "bern" << degreeOfPolyNom << i;
                    if (!(ratios[s.str().c_str()] > COs[Nbins - degreeOfPolyNom]))
                        lastUnNecessary++;
                }
                if (lastUnNecessary == sizeOfUnNecessary && (sizeOfUnNecessary != 0)) {
                    cout << "I don't keep this Bernstein: " << degreeOfPolyNom << endl;
                    return false;
                }
            }
        }
        if (inv == 1)
            cout << "I keep this inverted polynom: " << degreeOfPolyNom << endl;
        else if (inv == 0)
            cout << "I keep this polynom: " << degreeOfPolyNom << endl;
        else if (inv == 2)
            cout << "I keep this Chebychev: " << degreeOfPolyNom << endl;
        else if (inv == 3)
            cout << "I keep this Bernstein: " << degreeOfPolyNom << endl;
        cout << " ----- " << endl;
        return ret;
    }

    RooGenericPdf * getFinalInvPolynomial() {
        if (degreeOfPolyNom < 1){//2) {
            cout << "FATAL ERROR: final inverse polynomial for degree < 1 is not supported" << endl;
            return 0;
        }
        stringstream s;
        s << "InvPolyPdf_" << degreeOfPolyNom;
        TString Name = s.str().c_str();
        s.str("");
        RooArgList * Pars = new RooArgList("Pars");
        Pars->add(*var);
        TString formul = TString("1/(1") /*+ TString(var->GetName())*/;
        stringstream s2;
        for (int i = 0; i < ratios.size(); i++) {
            s.str("");
            s << "inva" << degreeOfPolyNom << i + 1;//2;
            if ((i + 1/*2*/) > degreeOfPolyNom)
                continue;
            TString parName = s.str().c_str();
            RooRealVar * par = 0;
            if (ratios[parName] > COs[Nbins - degreeOfPolyNom]) {
                par = new RooRealVar(parName, "", parVals[parName], parVals[parName] - 10 * fabs(parErrs[parName]), parVals[parName] + 10 * fabs(parErrs[parName]));
                s2 << "+" << parName << "*" << var->GetName() << "^" << i + 1/*2*/;
            }
            Pars->add(*par);
        }
        s2 << ")";
        formul = formul + s2.str().c_str();
        cout << formul << endl;
        if (Pars->getSize() == 0) {
            cout << "No parameter!" << endl;
            return 0;
        }
        RooGenericPdf * ret = new RooGenericPdf(Name, "", formul, *Pars);
        return ret;
    }

    TH1D * getDataHist()const {
        return hdata;
    }
private:
    TString name;
    int Nbins, degreeOfPolyNom, Ndata;
    double parmin, parmax;
    RooDataSet * data;
    TH1D * hdata;
    RooRealVar * var;
    std::map<unsigned int, double> COs;
    std::map<TString, double> ratios;
    std::map<TString, double> parVals;
    std::map<TString, double> parErrs;
};

class FtestTwoBody {
public:

    FtestTwoBody(TString name_, int Nbins_, int NbinsF_, double xmaxF_, int dop, double xmin_, double xmax_,
            RooRealVar var, RooDataSet data) : name(name_), Nbins(Nbins_), NbinsF(NbinsF_), xmaxF(xmaxF_),
    degreeOfPolyNom(dop), xmin(xmin_), xmax(xmax_) {
        //        gStyle->SetOptFit(1111);
        //        gStyle->SetOptStat(0);
        stringstream s;
        s << degreeOfPolyNom + 1 << degreeOfPolyNom;
        TString name1 = name + "_Data1" + s.str().c_str();
        data1 = (TH1D*) data.createHistogram(name1, var, RooFit::Binning(Nbins));
        data1->SetTitle("");
        data1->SetName(name1);
        data1->SetStats(kTRUE);
        for (int j = 0; j < Nbins; j++) {
            y1[j] = data1->GetBinContent(j + 1);
        }
        name1 = name + "_Data2" + s.str().c_str();
        data2 = (TH1D*) data.createHistogram(name1, var, RooFit::Binning(Nbins));
        data2->SetTitle("");
        data2->SetName(name1);
        data2->SetStats(kTRUE);
        for (int j = 0; j < Nbins; j++) {
            y2[j] = data2->GetBinContent(j + 1);
        }
        name1 = name + "_pol1" + s.str().c_str();
        TString func = formul(degreeOfPolyNom + 1);
        pol1 = new TF1(name1, func, xmin, xmax);
        pol1->SetParameter(0, 1.);
        for (int j = 0; j < degreeOfPolyNom; j++) {
            pol1->SetParameter(j + 1, 0);
        }
        name1 = name + "_pol2" + s.str().c_str();
        func = formul(degreeOfPolyNom + 2);
        pol2 = new TF1(name1, func, xmin, xmax);
        pol2->SetParameter(0, 1.);
        for (int j = 0; j < degreeOfPolyNom + 1; j++) {
            pol2->SetParameter(j + 1, 0);
        }
        data1->Fit(pol1, "QNL");
        data1->Fit(pol1, "QNL");
        data1->Fit(pol1, "QNL");
        data1->Fit(pol1, "QNL");
        chi2N1 = pol1->GetChisquare() / (double) pol1->GetNDF();
        for (int i = 0; i < degreeOfPolyNom + 1; i++) {
            double d = pol1->GetParameter(i);
        }
        data2->Fit(pol2, "QNL");
        data2->Fit(pol2, "QNL");
        data2->Fit(pol2, "QNL");
        data2->Fit(pol2, "QNL");
        chi2N2 = pol2->GetChisquare() / (double) pol2->GetNDF();
        for (int i = 0; i < degreeOfPolyNom + 2; i++) {
            double d = pol2->GetParameter(i);
        }
        name1 = name + "Fdistr" + s.str().c_str();
        Fdistr = new TH1D(name1, "", NbinsF, 0., xmaxF);
        name1 = name + "Fdistrextr" + s.str().c_str();
        Fdistrextr = new TH1D(name1, "", NbinsF, 0., xmaxF);
        name1 = name + "Finteg" + s.str().c_str();
        Finteg = new TH1D(name1, "", NbinsF, 0., xmaxF);
    }

    TString formul(int n) {
        stringstream s;
        for (int i = 0; i < n; i++) {
            s.str("");
            for (int j = 0; j < i + 1; j++) {
                if (j == 0)
                    s << "[" << j << "]";
                else
                    s << "+[" << j << "]";
                for (int p = 0; p < j; p++) {
                    s << "*x";
                }
            }
        }
        TString func = s.str().c_str();
        cout << func << endl;
        return func;
    }

    void getResSumSquared() {
        rss0 = 0;
        rss1 = 0;
        for (int i = 0; i < Nbins; i++) {
            double x = (i + 0.5) * xmax / (double) Nbins;
            rss0 += pow(y1[i] - pol1->Eval(x), 2);
            rss1 += pow(y2[i] - pol2->Eval(x), 2);
        }
    }

    void calcFtest() {
        getResSumSquared();
        double p1_10 = pol2->GetNpar() - pol1->GetNpar();
        double p2_10 = Nbins - pol2->GetNpar();
        Ftest = (rss0 - rss1) / p1_10 / (rss1 / p2_10);
    }

    void getGood_CL() {
        calcFtest();
        double p1_10 = pol2->GetNpar() - pol1->GetNpar();
        double p2_10 = Nbins - pol2->GetNpar();
        good_CL = 1. - TMath::FDistI(Ftest, p1_10, p2_10);
    }

    double calcPvalue() {
        double dndf = 1.;
        double dChi2 = pol1->GetChisquare() - pol2->GetChisquare();
        return TMath::Prob(dChi2, dndf);
    }

    double getAlternativeFtest(int which = 0) {
        double ret = (pol1->GetChisquare() / pol1->GetNDF()) / (pol2->GetChisquare() / pol2->GetNDF());
        if (which != 0)
            return 1. / ret;
        return ret;
    }

    void Print() {
        cout << "\tF - test value: " << Ftest << endl;
        cout << "\tProbabilty: " << good_CL << endl;
        cout << "Normalized chi2 pol. 1: " << chi2N1 << endl;
        cout << "Normalized chi2 pol. 2: " << chi2N2 << endl;

    }

    void CanvasMaker() {
        fillHists();
        //        gStyle->SetOptStat(1);
        //        gStyle->SetOptFit(1111);
        stringstream s;
        s.str("");
        s << "FtestCanv" << degreeOfPolyNom + 1 << degreeOfPolyNom;
        TString nameCanv = s.str().c_str();
        s.str("");
        s << "F test " << degreeOfPolyNom + 1 << degreeOfPolyNom;
        TString titleCanv = s.str().c_str();
        FTestCanv = new TCanvas(nameCanv, titleCanv, 750, 750);
        FTestCanv->Divide(2, 2);
        FTestCanv->cd(1);
        data1->SetStats(kTRUE);
        data1->SetMinimum(0);
        data1->SetMarkerStyle(20);
        data1->SetMarkerSize(0.7);
        data1->Draw("PE");
        pol1->SetLineColor(kRed);
        pol1->SetLineWidth(1);
        pol1->Draw("SAME");
        cout << "--- pol1 in ftest " << degreeOfPolyNom + 1 << degreeOfPolyNom << endl;
        for (int i = 0; i < pol1->GetNpar(); i++)
            cout << "par[" << i << "] = " << pol1->GetParameter(i) << " +/- " << pol1->GetParError(i) << endl;

        FTestCanv->cd(2);
        data2->SetStats(kTRUE);
        data2->SetMinimum(0);
        data2->SetMarkerStyle(20);
        data2->SetMarkerSize(0.7);
        data2->Draw("PE");
        pol2->SetLineColor(kRed);
        pol2->SetLineWidth(1);
        pol2->Draw("SAME");
        cout << "--- pol2 in ftest " << degreeOfPolyNom + 1 << degreeOfPolyNom << endl;
        for (int i = 0; i < pol2->GetNpar(); i++)
            cout << "par[" << i << "] = " << pol2->GetParameter(i) << " +/- " << pol2->GetParError(i) << endl;
        FTestCanv->cd(3);

        //        TLatex * tex = new TLatex(0.7855228, 0.8712121, "sk[2qk[s");
        //        tex->SetLineWidth(2);
        //        tex->Draw();
        FTestCanv->GetPad(3)->SetLogy();
        Fdistr->Draw();
        Fdistrextr->SetFillColor(kBlue);
        Fdistrextr->Draw("SAME");
        FTestCanv->cd(4);
        Finteg->SetMinimum(0);
        Finteg->Draw();
        Arrow = new TArrow(Ftest, 0.8, Ftest, 0.1);
        ArrowI = new TArrow(Ftest, 0.1, Ftest, 0.8);
        Arrow->SetLineWidth(2);
        Arrow->SetLineColor(kBlue);
        ArrowI->SetLineWidth(2);
        ArrowI->SetLineColor(kBlue);
        ArrowI->Draw();
    }

    TCanvas * getConv() {
        CanvasMaker();
        return FTestCanv;
    }

    void fillHists() {
        double p1_10 = pol2->GetNpar() - pol1->GetNpar();
        double p2_10 = Nbins - pol2->GetNpar();
        //        gStyle->SetOptStat(1);
        //        gStyle->SetOptFit(1111);
        for (int i = 0; i < NbinsF; i++) {
            double x = (i + 0.5) * xmaxF / (double) NbinsF;
            double Fvalue10 = TMath::FDist(x, p1_10, p2_10);
            double Fsum10 = TMath::FDistI(x, p1_10, p2_10);
            Fdistr->SetBinContent(i + 1, Fvalue10);
            if (x > Ftest) Fdistrextr->SetBinContent(i + 1, Fvalue10);
            Finteg->SetBinContent(i + 1, Fsum10);
        }
    }

    double getFtest()const {
        return Ftest;
    }

    double getGoodCL()const {
        return good_CL;
    }

    double getRss0()const {
        return rss0;
    }

    double getRss1()const {
        return rss1;
    }
private:
    TString name;
    int Nbins, degreeOfPolyNom, NbinsF;
    double xmin, xmax, xmaxF, chi2N1, chi2N2;
    TH1D * data1;
    TH1D * data2;
    TF1 * pol1;
    TF1 * pol2;
    TH1D* Fdistr;
    TH1D* Fdistrextr;
    TH1D* Finteg;
    double y1[1000];
    double y2[1000];
    double rss0, rss1, Ftest, good_CL;
    TArrow* Arrow;
    TArrow* ArrowI;
    TCanvas* FTestCanv;
};
