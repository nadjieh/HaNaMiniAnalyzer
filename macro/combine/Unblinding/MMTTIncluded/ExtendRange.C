void ExtendRange(TString fname){
  TFile* f=TFile::Open( fname + ".root");
  RooWorkspace* w = (RooWorkspace*)f->Get("w");
  w->var("aMuMass")->setRange(18,62.5);
  w->SaveAs(fname+"Mod.root");
}
