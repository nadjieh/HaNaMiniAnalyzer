

/*
 * File:   SimultaneousFit.C
 * Author: nadjieh
 *
 * Created on May 20, 2015, 2:47 PM
 */

/*
 * *OPTIONS*
 * scratch: all peremters are free and mean is not shifting.
 * meanshift: only mean is shifting but the rest are free.
 * sgimaline: mean is shifting, sigma is linear
 * sigmaCBline: as sigmaline + linear sigma_cb
 * a1b1: as sigmaCBline with sigma's modeled w/o intercept
 */

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
#include "../interface/SignalShapeHelpers.h"

using namespace std;
using namespace RooFit;


/*
 * 
 *
/*SimultaneousFit*/

int main(int argc, char** argv) {
	std::map< TString, RooRealVar *> inputVars;
    RooRealVar* frac = 0;    
    std::map<TString,bool> isParFixed;
    std::map<TString,bool> isParCommon;    
    std::vector<VarInfo> varInfo;
    TString option = "scratch";
	for (int f = 1; f < argc; f++) {
        std::string arg_fth(*(argv + f));
		if (arg_fth == "option") {
            f++;
            std::string out(*(argv + f));
            option = out.c_str();
        } else if(arg_fth == "card"){
        	f++;
        	std::string out(*(argv + f));
            varInfo = CardReader(out.c_str());
        }
    }
    stringstream optionStr;
    for(unsigned int i =0; i < varInfo.size(); i++){
    	cout<<varInfo[i].name<<"\t"<<varInfo[i].isCommon <<"\t"<<varInfo[i].isFixed<<"\t"<<varInfo[i].val<<"\t"<<varInfo[i].xD<<"\t"<<varInfo[i].xU<<endl;
    	if(varInfo[i].isCommon && varInfo[i].name != "mS" && varInfo[i].name != "a0" && varInfo[i].name != "a1" && varInfo[i].name != "b0"){
    		optionStr << varInfo[i].name <<"Common";
    	}
    	if(varInfo[i].isFixed){
    		optionStr << varInfo[i].name <<"Fixed"<<varInfo[i].val;
    	}
    	if(varInfo[i].name == "frac") {
    		if(varInfo[i].isFixed) frac = new RooRealVar(varInfo[i].name, varInfo[i].name, varInfo[i].val);
    		else frac = new RooRealVar(varInfo[i].name, varInfo[i].name, varInfo[i].xD,	varInfo[i].xU);
    	} else {
    		if(varInfo[i].isFixed) inputVars[varInfo[i].name]  = new RooRealVar(varInfo[i].name, varInfo[i].name, varInfo[i].val);
    		else if(varInfo[i].isCommon) inputVars[varInfo[i].name] = new RooRealVar(varInfo[i].name, varInfo[i].name, varInfo[i].xD,	varInfo[i].xU);
    		else  inputVars[varInfo[i].name] = 0;
    	}
    }
    option = optionStr.str().c_str();
    inputVars["sigma"] = 0;
    inputVars["sigma_cb"] = 0;

   	RooRealVar * mass = new RooRealVar("aMuMass", "aMuMass", 10, 70);
    RooRealVar * leptonWeight = new RooRealVar("hltWeight_Mu17Mu8_DZ", "hltWeight_Mu17Mu8_DZ", -2, 2.);
    RooRealVar * btagWeightTL = new RooRealVar("bWeightTL", "bWeightTL", -2., 2.);
    RooRealVar * otherWeights = new RooRealVar("Weight", "Weight", -2, 2.);
    RooFormulaVar * WeightGlobal = new RooFormulaVar("WeightGlobal", "@0*@1*@2", RooArgSet(*leptonWeight, *btagWeightTL, *otherWeights));    
	std::vector<TTree*> trees;
	std::vector<RooRealVar*> wVars;
	std::vector<RooFormulaVar*> weights;					
	std::vector<RooDataSet*> datas;	
	std::vector<RooDataSet*> Wdatas;	
	std::vector<RooAddPdf*> pdfs;		
    RooCategory sampleWeighted("sampleWeighted", "sampleWeighted");	
	stringstream fname;
	for(int i = 0; i < 9; i++){
		fname.str("");
		fname << "GGH" << 20 + (5*i) <<".root";
		TFile * f = TFile::Open(fname.str().c_str());
		trees.push_back((TTree*) f->Get("Hamb/Trees/Events"));
		fname.str("");	
		fname << "Weights" << 20 + (5*i);
		weights.push_back(new RooFormulaVar(fname.str().c_str(), "@0*@1*@2", RooArgSet(*leptonWeight, *btagWeightTL, *otherWeights)));
		fname.str("");
		fname << "sample"<<	20 + (5*i);
		sampleWeighted.defineType(fname.str().c_str());
	    pdfs.push_back(VoigCBMaker(20 + (5*i), mass, inputVars, frac, option));		
	}

	for(unsigned int i = 0; i < trees.size(); i++){
		fname.str("");
		fname << "data" << 20 + (5*i);		
		datas.push_back(new RooDataSet(fname.str().c_str(), fname.str().c_str(),trees[i], RooArgSet(*mass, *leptonWeight, *btagWeightTL, *otherWeights), ""));
		datas[datas.size()-1]->Print();
		wVars.push_back((RooRealVar*)datas[datas.size()-1]->addColumn(*weights[i]));
		Wdatas.push_back(new RooDataSet(fname.str().c_str(), fname.str().c_str(),datas[datas.size()-1],*datas[datas.size()-1]->get(),0, wVars[wVars.size()-1]->GetName()));
		Wdatas[Wdatas.size()-1]->Print();		
	}

	
	cout << "begin ..." << endl;
	
	 RooDataSet combData("combDataWeighted", "combined data", RooArgSet(*mass, *leptonWeight, *btagWeightTL, *otherWeights), Index(sampleWeighted),
            Import("sample20", *Wdatas[0]),
            Import("sample25", *Wdatas[1]),
            Import("sample30", *Wdatas[2]),
            //Import("sample35", *Wdatas[3]),
            Import("sample40", *Wdatas[4]),
            //Import("sample45", *Wdatas[5]),
            Import("sample50", *Wdatas[6]),
            Import("sample55", *Wdatas[7]),
            Import("sample60", *Wdatas[8])
            );

    RooRealVar * weightGlobal = (RooRealVar*) combData.addColumn(*WeightGlobal);
    RooDataSet combDataWeighted(combData.GetName(), combData.GetTitle(), &combData, *combData.get(), 0, weightGlobal->GetName());

    cout << ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" << endl;
    combDataWeighted.Print();
    cout << ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" << endl;
    RooSimultaneous simPdfWeighted("simPdfWeighted", "simultaneous pdf", sampleWeighted);
	for(int i = 0; i < 9; i++){
		if( i == 3 || i == 5) continue;
		fname.str("");
		fname << "sample"<<	20 + (5*i);
		simPdfWeighted.addPdf(*pdfs[i], fname.str().c_str());		
	}
    RooFitResult * fr = 0;

    fr = simPdfWeighted.fitTo(combDataWeighted, RooFit::Save(), RooFit::SumW2Error(kTRUE));
   	cout<<"1- "<<((RooRealVar*) fr->floatParsFinal().find("alpha_M25"))<<endl;
    std::vector<int> tmpMasspoints;
	std::vector<TString> massPointsStr;   
	for(int i = 0; i < 9; i++){
		if( i == 3 || i == 5) continue;
		tmpMasspoints.push_back(20 + (5*i));
		stringstream S;
		S << 20 + (5*i);
		massPointsStr.push_back(S.str().c_str());
	}      
    DrawEvolutions(fr,tmpMasspoints,varInfo, option);
    DrawPostFitMasses(mass, &combDataWeighted, &simPdfWeighted, &sampleWeighted, massPointsStr, option);
	//PrintFr(fr, tmpMasspoints, "frac", option);
	PrintFr(fr, tmpMasspoints, varInfo, option);	
	cout<<"2- "<<((RooRealVar*) fr->floatParsFinal().find("alpha_M25"))<<endl;

    
}

