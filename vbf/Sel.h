#ifndef Sel_h
#define Sel_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TTreeFormula.h>
#include <TTreeDrawArgsParser.h>
#include <vector>
#include <map>
#include <string>
#include <TH1.h>
#include <TList.h>
#include <iostream>
// Headers needed by this particular selector


class Sel : public TSelector {
public:
  std::vector<TString> variables_name;
  TList variables_formula;
  TTreeDrawArgsParser cutArg;
  TTreeDrawArgsParser weightArg;

  TTreeFormula* cut;
  TTreeFormula* weight;
  TList variables;

  TList Histograms;
  TTree* fChain;
  int IsData;
  TString dsname;
  Sel(TTree * =0) { }
  virtual ~Sel() { std::cout << "deleting sel object: " << dsname << " cut  " << cut << "we" << weight << " isdata:" << IsData << " ch " << fChain << " ve" << variables.GetEntries() << " he" << Histograms.GetEntries() << std::endl ;}
  virtual Int_t   Version() const { return 1; }
  virtual void    SlaveBegin(TTree *tree);
  virtual void    Init(TTree *tree);
  void SetCutAndWeight( TString cut_ , TString weight_);
  void AddPlot( TString name , TString formula);
  void SetTree(TTree* t);
  virtual Bool_t  Notify(){return true;};
  virtual Bool_t  Process(Long64_t entry);
  virtual Int_t   GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
  virtual void    SetOption(const char *option) { fOption = option; }
  virtual void    SetObject(TObject *obj) { fObject = obj; }
  virtual void    SetInputList(TList *input) { fInput = input; }
  virtual TList  *GetOutputList() const { return fOutput; }
  virtual void    SlaveTerminate();
  virtual void    Terminate();

  ClassDef(Sel,0);

};
#endif
