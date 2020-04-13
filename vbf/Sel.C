#define Selector_cxx

#include <TFile.h>
#include "Sel.h"
#include <fstream>
using namespace std;

void Sel::SetCutAndWeight( TString cut_ , TString weight_){
  cutArg.Parse( cut_ , "" ,"" ) ;
  weightArg.Parse( weight_ , "" , "" );
}

void Sel::AddPlot( TString name , TString formula){
  variables_formula.Add( new TTreeDrawArgsParser() );
  ((TTreeDrawArgsParser*)variables_formula.Last())->Parse( formula , "" , "" );
  variables_name.push_back( name );
  //cout << name << "added" << endl;
}

void Sel::SetTree(TTree* tree){
  if( tree == 0 )
    return;
  fChain = tree;
  this->cut = new TTreeFormula( "cut" , cutArg.GetVarExp() , tree );
  if(!this->IsData)
    this->weight = new TTreeFormula( "weight" , weightArg.GetVarExp() , tree );

  this->variables.Delete();
  //this->variables_name.clear();
  //this->variables_formula.Delete();
  for(uint i=0; i< variables_name.size() ; i++){
    this->variables.Add( new TTreeFormula( variables_name[i].Data() , ((TTreeDrawArgsParser*)variables_formula.At(i))->GetVarExp() , tree ) );
  }
}

void Sel::Init( TTree* tree ){
  //cout << "init start"<< endl;
  TString options(fOption);
  TObjArray* optParts = options.Tokenize(":");
  TString infilename = ((TObjString*)optParts->At(0))->String();
  std::ifstream infile(infilename.Data());
  TString sample = ((TObjString*)optParts->At(1))->String();
  this->dsname = sample;
  this->IsData = ((TObjString*)optParts->At(2))->String().Atoi();
  //cout << fOption << "  " << infilename << "   " << sample << "   " << IsData << "   "  << ((TObjString*)optParts->At(2))->String() << endl;
  std::string line;
  int lineNumber = 0;
  variables_formula.Delete();
  variables_name.clear();
  while (std::getline(infile, line))
    {
      TString lne(line);
      //cout << lne << endl;
      lineNumber++;
      if(lineNumber==1)
	cutArg.Parse( lne , "" ,"" ) ;
      else if( lineNumber==2 )
	weightArg.Parse( lne , "" ,"" ) ;
      else{
	int separator = lne.First(',');
	TString name = lne( 0 , separator );
	TString formula = lne( separator+1 , lne.Length() );
	formula.ReplaceAll("{SN}", sample );
	//cout << name << "  " << formula << endl;
	this->AddPlot( name , formula );
      }
    }
  SetTree( tree );
  //cout << "init end"<< endl;
}

void Sel::SlaveBegin(TTree *tree){
  //cout << "sb start"<< endl;
  //cout << fOption << endl;
  //SetTree( tree );
  Init( tree );
  
  for(uint i=0; i< variables_name.size() ; i++){
    TTreeDrawArgsParser* var = ((TTreeDrawArgsParser*)variables_formula.At(i));
    Histograms.Add( new TH1D( var->GetObjectName() , var->GetObjectTitle() , var->GetParameter(0) ,var->GetParameter(1) ,var->GetParameter(2) ) );
  }
  //cout << "sb end"<< endl;
}

Bool_t Sel::Process(Long64_t entry){
  GetEntry( entry );
  if( this->cut->EvalInstance() != 0.0 ){
    //cout << this->cut->EvalInstance() << "  " << flush;
    double w = 1.0;
    if(!IsData){
      w = this->weight->EvalInstance() ;
    }//cout << w << " " << flush;
    for(uint i=0; i< variables_name.size() ; i++){
      //cout << variables_name[i] << flush;
      double val = ((TTreeFormula*)variables.At(i))->EvalInstance();
      //cout << ":" << val << flush ;
      //cout << ":" << Histograms.At(i)->GetName() << "  " << flush ;
      ((TH1*)Histograms.At(i))->Fill( val , w );
    }
    //cout << endl;
  }
  return true;
}

void Sel::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.
  ImportOutput( &Histograms );
  Histograms.Delete();
  variables.Delete();
  variables_formula.Delete();
  //delete cut;
  //delete weight;
}

void Sel::Terminate()
{
  Histograms.Delete();
  return;
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.
  TFile* fout = TFile::Open("fout.root" , "recreate");
  for(uint i=0; i< variables_name.size() ; i++){
    Histograms.At(i)->Write();
  }
  fout->Close();
}

