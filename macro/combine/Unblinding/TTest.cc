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
#include "RooArgusBG.h"
#include "RooWorkspace.h"
#include <stdio.h>
#include <math.h>
#include "TTest.h"
using namespace RooFit;
using namespace std;

double CHI2_THRESHOLD = 0.2;
double P_DNLL_THRESHOLD = 0.05;

class TTestBase {
public :
  TTestBase(TString name_, int Nbins_, int dop, RooRealVar * var_, RooDataSet * data_) :
    name(name_),
    Nbins(Nbins_),
    degreeOfPolyNom(dop){
    var = var_;
    var->setBin(Nbins);
    data = data_;
    hdata = (TH1D*) data->createHistogram("hdata", *var, RooFit::Binning(Nbins));
    Ndata = data->sumEntries(0);
    FillCOsMap( COs );
  };
  
  ~TTestBase() {
  };

  virtual RooAbsPdf* GetPdf() = 0;
  virtual string GetName() = 0;
  string GetTitle(){
    stringstream fName;
    fName << GetName() << "_" << degreeOfPolyNom ;
    return fName.str();
  };
  
  RooAbsPdf * pBestFit;
  RooRealVar* n_BestFit;
  RooExtendPdf * pext_BestFit;
  RooFitResult* res_BestFit;
  RooDataHist* datahist_BestFit;
  RooArgList * Pars;
  RooExtendPdf* pBestChi2Fit;
  RooFitResult* res_BestChi2Fit;

  RooExtendPdf* pBestOldFit;
  RooFitResult* res_BestOldFit;

  void BestFit(bool writeCanvas = false) {//0: pol, 1: inv, 2: chb
    RooAbsPdf * p = GetPdf();
    pBestFit = p ;
    n_BestFit = new RooRealVar("n", "n", 0., 2 * Ndata);
    pext_BestFit = new RooExtendPdf("pext", "pext", *p, *n_BestFit);
    RooExtendPdf* pext = pext_BestFit ;

    datahist_BestFit = new RooDataHist("datahist", "datahist", RooArgSet(*var), hdata);
    RooFitResult* res = pext->fitTo(*datahist_BestFit, RooFit::Save());
    res_BestFit = res;

    pBestChi2Fit = (RooExtendPdf*) pext_BestFit->clone("chi2_pext") ;
    res_BestChi2Fit = pBestChi2Fit->chi2FitTo(*datahist_BestFit, RooFit::Save());
    
    pBestOldFit = (RooExtendPdf*) pext_BestFit->clone("old_pext") ;
    res_BestOldFit = pBestOldFit->fitTo(*datahist_BestFit, RooFit::Save() , RooFit::Minimizer("OldMinuit" , "migrad") );
    
    if(writeCanvas){
      RooPlot * p2 = var->frame();
      data->plotOn(p2, Binning(Nbins));
      pext->plotOn(p2);
      TCanvas c;
      p2->Draw();
      stringstream fName;
      fName <<"Shape_"<<GetName()<<"_"<<degreeOfPolyNom<<"_fit";
      TString fNameStr = fName.str().c_str();
      c.SetName(fNameStr);
      c.Write();
    }
  }


  virtual RooAbsPdf* MakeFinalPdf(){
    for(int ii = 0 ; ii < Pars->getSize() ; ii++ ){
      RooRealVar * arg = (RooRealVar*)( Pars->at( ii ) );
      arg->setRange(  arg->getVal() - 2*arg->getError() , arg->getVal() + 2*arg->getError() );
    }
    return pBestFit;
  };
  
  double getChi2(bool normalized = true){
    double devide = 1.0;
    if(normalized)
      devide = (Nbins+degreeOfPolyNom-1.0);
    return res_BestChi2Fit->minNll()/devide ;
  };
  
  double getNLL(bool oldMinimizer = false){
    if(oldMinimizer)
      return res_BestOldFit->minNll();
    else
      return res_BestFit->minNll();
  };

  void Print() {
  }

  void FillAllVals( TTestBase* previousOne ){
    AllVals.Chi2 = getChi2(false);
    AllVals.NormChi2 = getChi2(true);
    AllVals.NLL = getNLL();
    AllVals.PChi2 = TMath::Prob( AllVals.Chi2 , Nbins+degreeOfPolyNom-1.0 );
    AllVals.PNormChi2 = TMath::Prob( AllVals.NormChi2 ,1.0 );
    AllVals.OldNLL = getNLL(true);
    if(previousOne){
      AllVals.DeltaPChi2 = AllVals.PChi2 - previousOne->AllVals.PChi2;
      AllVals.DeltaPNormChi2 = AllVals.PNormChi2 - previousOne->AllVals.PNormChi2;
      AllVals.PDeltaNormChi2 = TMath::Prob( AllVals.NormChi2 - previousOne->AllVals.NormChi2 , 1 );
      AllVals.PDeltaNLL = TMath::Prob( -2*( AllVals.NLL - previousOne->AllVals.NLL )  , 1 );
      AllVals.PLogDeltaNLL = TMath::Prob( -2*TMath::Log( AllVals.NLL/previousOne->AllVals.NLL ) , 1 );
      AllVals.PDeltaOldNLL = TMath::Prob( -2*( AllVals.OldNLL - previousOne->AllVals.OldNLL ) , 1 );
    }
  }
  struct allVals{
    double Chi2;
    double NormChi2;
    double NLL;
    double PChi2;
    double PNormChi2;
    double DeltaPChi2;
    double DeltaPNormChi2;
    double PDeltaNormChi2;
    double PDeltaNLL;
    double PLogDeltaNLL;
    double OldNLL;
    double PDeltaOldNLL;
    allVals(){
      Chi2= 0;	
      NormChi2=0;	
      NLL=0;		
      PChi2=0;	
      PNormChi2=0;	
      DeltaPChi2=0;	
      DeltaPNormChi2=0;
      PDeltaNormChi2=0;
      PDeltaNLL=0;	
      PLogDeltaNLL=0;
      OldNLL = 0 ;
      PDeltaOldNLL = 0 ;
    };
  };
  allVals AllVals;
  
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


class PolynomialTest : public TTestBase {
public:
  PolynomialTest(TString name_, int Nbins_, int dop, RooRealVar * var_, RooDataSet * data_) : TTestBase( name_ ,Nbins_ , dop , var_ , data_ ){
  };
  ~PolynomialTest(){};

  virtual RooAbsPdf* GetPdf(){
    stringstream s;
    s << GetName() << "_" << degreeOfPolyNom;
    TString Name = s.str().c_str();
    s.str("");
    Pars = new RooArgList("Pars");
    for (int i = 0; i < degreeOfPolyNom ; i++) {
      s.str("");
      s << "p" << degreeOfPolyNom << i + 1;
      TString parName = s.str().c_str();
      RooRealVar * par = new RooRealVar(parName, parName, -10 , 10 );
      Pars->add(*par);
    }
    RooPolynomial * ret = new RooPolynomial(Name, Name, *var, *Pars);
    return ret;
  };
  virtual string GetName() {return "PolyPdf"; };
};

class ChebychevTest : public TTestBase {
public:
  ChebychevTest(TString name_, int Nbins_, int dop, RooRealVar * var_, RooDataSet * data_) : TTestBase( name_ ,Nbins_ , dop , var_ , data_ ){
  };
  ~ChebychevTest(){};

  virtual RooAbsPdf* GetPdf(){
    stringstream s;
    s << GetName() << "_" << degreeOfPolyNom;
    TString Name = s.str().c_str();
    s.str("");
    Pars = new RooArgList("Pars");
    for (int i = 0; i < degreeOfPolyNom; i++) {
      s.str("");
      s << "c" << degreeOfPolyNom << i;
      TString parName = s.str().c_str();
      RooRealVar * par = new RooRealVar(parName , parName , -10 , 10 ) ;
      Pars->add(*par);
    }
    RooChebychev * ret = new RooChebychev(Name, Name, *var, *Pars);
    return ret;
  };
  virtual string GetName() {return "Chebychev"; };
};

class BernsteinTest : public TTestBase {
public:
  BernsteinTest(TString name_, int Nbins_, int dop, RooRealVar * var_, RooDataSet * data_) : TTestBase( name_ ,Nbins_ , dop , var_ , data_ ){
  };
  ~BernsteinTest(){};

  virtual RooAbsPdf* GetPdf(){
    stringstream s;
    s << GetName() << "_" << degreeOfPolyNom;
    TString Name = s.str().c_str();
    s.str("");
    Pars = new RooArgList("Pars");
    for (int i = 0; i < degreeOfPolyNom; i++) {
      s.str("");
      s << "b" << degreeOfPolyNom << i;
      TString parName = s.str().c_str();
      RooRealVar * par = new RooRealVar(parName , parName , -10 , 10 ) ;
      Pars->add(*par);
    }
    RooBernstein * ret = new RooBernstein(Name, Name, *var, *Pars);
    return ret;
  };
  virtual string GetName() {return "Bernstein"; };
};



class InvPolyTest : public TTestBase {
public:
  InvPolyTest(TString name_, int Nbins_, int dop, RooRealVar * var_, RooDataSet * data_) : TTestBase( name_ ,Nbins_ , dop , var_ , data_ ){
  };
  ~InvPolyTest(){};

  virtual RooAbsPdf* GetPdf(){
    stringstream s;
    s << GetName() << "_" << degreeOfPolyNom;
    TString Name = s.str().c_str();
    s.str("");
    Pars = new RooArgList("Pars");
    for (int i = 0; i < degreeOfPolyNom; i++) {
      s.str("");
      s << "i" << degreeOfPolyNom << i;
      TString parName = s.str().c_str();
      RooRealVar * par;
      // if(i==0)
      // 	par = new RooRealVar(parName , parName , 1.0 ) ;
      // else
      par = new RooRealVar(parName , parName , -10 , 10 ) ;
      Pars->add(*par);
    }
    RooInvPoly * ret = new RooInvPoly(Name, Name, *var, *Pars);
    return ret;
  };
  virtual string GetName() {return "InvPoly"; };

  virtual RooAbsPdf* MakeFinalPdf(){
    TTestBase::MakeFinalPdf();
    stringstream s2;
    s2 << "1.0/(1.0" ;
    for (int i = 0; i < degreeOfPolyNom; i++) {
      s2 << "+" << Pars->at(i)->GetName() << "*" << var->GetName() << "^" << i + 1;
    }
    s2 << ")";
    TString formul( s2.str().c_str() );
    cout << formul << endl;
    Pars->add( *var );
    RooGenericPdf * ret = new RooGenericPdf(pBestFit->GetName(), "Name", formul, *Pars);
    return ret;
  };
};



class ListBase {
public :
  virtual void Finalize(RooWorkspace* w) = 0 ;
  virtual TTestBase* addNewPdf(int dop) = 0;
};

template< class c >
class ListOfTests : public vector<c> , public ListBase{
public:
  TString name;
  int Nbins;
  RooDataSet * data;
  RooRealVar * var;
  vector<short int> Colors;
  ListOfTests( TString name_, int Nbins_, RooRealVar * var_, RooDataSet * data_ ) :
    name(name_),
    Nbins(Nbins_),
    data(data_),
    var(var_){
    Colors = { kBlue , kRed , kOrange, kYellow , kGreen , kAzure , kBlack };
  };

  TTestBase* addNewPdf(int dop){
    this->emplace_back(name, Nbins, dop, var, data);
    return &(this->at( this->size() -1 ));
  };

  TTestBase::allVals valsForTree ;
  TTree* tree;
  
  void Finalize(RooWorkspace* w){
    double x = 0.0;
    int pass = 0;
    int pass_old = 0;

    RooPlot * p_allSelectedOnes = var->frame();
    data->plotOn(p_allSelectedOnes, Binning(Nbins));

    
    tree = new TTree("tree" , "tree");
    tree->Branch( "degree" , &x );
    tree->Branch( "pass" , &pass );
    tree->Branch( "pass_old" , &pass_old );
    tree->Branch( "Chi2" ,  &valsForTree.Chi2 );
    tree->Branch( "NormChi2" , &valsForTree.NormChi2 );
    tree->Branch( "NLL" , &valsForTree.NLL );
    tree->Branch( "OldNLL" , &valsForTree.OldNLL );
    tree->Branch("PChi2" , &valsForTree.PChi2 );
    tree->Branch("PNormChi2" , &valsForTree.PNormChi2 );
    tree->Branch("DeltaPChi2" ,&valsForTree.DeltaPChi2 );
    tree->Branch("DeltaPNormChi2" , &valsForTree.DeltaPNormChi2 );
    tree->Branch("PDeltaNormChi2" , &valsForTree.PDeltaNormChi2 );
    tree->Branch("PDeltaNLL" , &valsForTree.PDeltaNLL );
    tree->Branch("PLogDeltaNLL" , &valsForTree.PLogDeltaNLL );
    tree->Branch("PDeltaOldNLL" , &valsForTree.PDeltaOldNLL );
    
    TGraph * gNLL = new TGraph(this->size()-1);
    gNLL->SetName("NLLProb");
    TGraph * gChi2 = new TGraph(this->size());
    gChi2->SetName("Chi2");

    
    for(int i = 0 ; i < this->size() ; i++){
      c* a = &this->at(i);
      x = a->degreeOfPolyNom;
      if( i == 0 )
	a->FillAllVals( NULL );
      else
	a->FillAllVals( &(this->at( i-1 )) );
      
      valsForTree = a->AllVals;
      
      gChi2->SetPoint( i , x , valsForTree.NormChi2 );
      if( i!=0 ){
	gNLL->SetPoint( i-1 , x , valsForTree.PDeltaNLL );
      }

      if(pass==0){
	if( abs(valsForTree.NormChi2 - 1.0)< CHI2_THRESHOLD )
	  pass = 1;
      }else if(pass == 1){
	if( valsForTree.PDeltaNLL < P_DNLL_THRESHOLD )
	  pass = 2;
      }
      if(pass_old==0){
	if( abs(valsForTree.NormChi2 - 1.0)<CHI2_THRESHOLD )
	  pass_old = 1;
      }else{
	if( valsForTree.PDeltaOldNLL < P_DNLL_THRESHOLD )
	  pass_old = 2;
      }

      if(pass_old == 1 ){
	RooAbsPdf* fPdf = a->MakeFinalPdf();
	w->import(*fPdf );
	a->pext_BestFit->plotOn( p_allSelectedOnes , RooFit::LineColor( Colors[i] ) )->getCurve()->SetTitle( a->GetTitle().c_str()  );
      }	
      
      tree->Fill();
    }

    TCanvas CSelectedOnes("SelectedOnes");
    p_allSelectedOnes->Draw();
    CSelectedOnes.Write();
    
    gNLL->Write();
    gChi2->Write();
    tree->Write();
  };
};

int main(int argc, char** argv) {
    RooMsgService::instance().setGlobalKillBelow(RooFit::FATAL);
    int nbins = 50;
    double minpar = -10.;
    double maxpar = 10.;
    double mL = 20.;
    double mH = 63.;
    vector<double> degrees;
    int pdfId = 0;
    TString inputFileName = "";
    for (int f = 1; f < argc; f++) {
        string arg_fth(*(argv + f));
	if (arg_fth == "chi2t") {
            f++;
            string in(*(argv + f));
            CHI2_THRESHOLD = stof(in.c_str());
        }else if (arg_fth == "pnllt") {
            f++;
            string in(*(argv + f));
            nbins = stof(in.c_str());
        }else if (arg_fth == "nBins") {
            f++;
            string in(*(argv + f));
            nbins = atof(in.c_str());
        } else if (arg_fth == "minpar") {
            f++;
            string in(*(argv + f));
            minpar = atof(in.c_str());
        } else if (arg_fth == "maxpar") {
            f++;
            string in(*(argv + f));
            maxpar = atof(in.c_str());
        } else if (arg_fth == "vdop") {
            f++;
            string in(*(argv + f));
	    std::vector<string> from_to = split( in , ':' );
	    for(int i = atof( from_to[0].c_str() ) ; i < atof( from_to[1].c_str() ) + 1 ; i++){
	      if( pdfId == 1 && i== 0 )
		continue;
	      if( pdfId == 2 && i > 6 )
		continue;
	      degrees.push_back(i);
	    }
        } else if (arg_fth == "pdfId") {
            f++;
            string in(*(argv + f));
            pdfId = atof(in.c_str());
	    std::cout<<"pdfId "<<pdfId<<std::endl;
        } else if (arg_fth == "input") {
            f++;
            string in(*(argv + f));
            inputFileName = in.c_str();
        }
    }
    stringstream s;
    s << "_nbins" << nbins << "_" ;
    TString name = "";
    TCanvas * c = 0;
    gErrorIgnoreLevel = kError;
    RooRealVar * aMuMass = new RooRealVar("aMuMass", "aMuMass", mL, mH);
    TFile * input = TFile::Open(inputFileName);
    TTree * tree = (TTree*) input->Get("Hamb/Trees/Events");
    RooDataSet * data = new RooDataSet("ControlData", "The original control data", tree, *aMuMass, "");
    TH1* Hist = (TH1D*) data->createHistogram("hdata", *aMuMass, RooFit::Binning(nbins) ) ;
    RooDataHist * dataHist = new RooDataHist("hist", "hist", *aMuMass, Hist );
    RooWorkspace * w = 0;
    TString Name ="";

    ListBase* allFunctions = NULL;
    if (pdfId == 0){
        w = new RooWorkspace("WS", "WS");
	Name ="gen"+ s.str() + inputFileName;
	allFunctions = new ListOfTests<PolynomialTest>( "test" , nbins , aMuMass , data );
    } else if (pdfId == 1){
        w = new RooWorkspace("InvWS", "InvWS");
	Name = "Inv"+ s.str()+ inputFileName;
	allFunctions = new ListOfTests<InvPolyTest>( "test" , nbins , aMuMass , data );
    } else if (pdfId == 2){
        w = new RooWorkspace("ChebWS", "ChebWS");
	Name = "Cheb"+ s.str()+ inputFileName;
	allFunctions = new ListOfTests<ChebychevTest>( "test" , nbins , aMuMass , data );
    } else if (pdfId == 3){
	std::cout<<"BERN"<<std::endl;
	Name = "bern"+ s.str()+ inputFileName;
        w = new RooWorkspace("BernWS", "BernWS");
	allFunctions = new ListOfTests<BernsteinTest>( "test" , nbins , aMuMass , data );
    }
    s.str();
    w->import(*data);
    w->import(*aMuMass);
    w->import(*dataHist);
    std::vector<double> probs;
    std::vector<double> nlls;
    TGraph * gNLL = new TGraph(degrees.size()-1);
    gNLL->SetName("NLLProb");
    TGraph * gChi2 = new TGraph(degrees.size());
    gChi2->SetName("Chi2");


    TFile fPlots(Name , "recreate");
    fPlots.cd();
    for (unsigned int i = 0; i < degrees.size(); i++) {
        int dop = degrees[i];
	TTestBase* mytest ;
	mytest = allFunctions->addNewPdf( dop ) ;
        mytest->BestFit(true);
    }
    fPlots.cd();
    allFunctions->Finalize(w);
    w->Write();
    fPlots.Close();
};
