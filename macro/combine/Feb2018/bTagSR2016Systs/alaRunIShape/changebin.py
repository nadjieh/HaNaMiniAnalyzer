import ROOT as root

def changeBin(infName, nBin):
	inf = root.TFile.Open("%s.root" %(infName))
	myW = inf.Get("w").Clone("myW")
	inf.Close()
	myW.var("frac").setVal(0.57)
	myW.var("n").setVal(3.02)
	myW.var("width").setVal(0.008)
	myW.var("alpha").setVal(1.15)
	outf = root.TFile("%s-%s.root" %(infName,nBin),"recreate")
	outf.cd()
	myW.SetName("w")
	myW.Write()
	outf.Close()

root.gSystem.Load("RooFit")
root.gSystem.Load("~/work/tHq/CMSSW_7_4_7/lib/slc6_amd64_gcc491/libHiggsAnalysisCombinedLimit.so")
changeBin("hamb-shapes-UnbinnedParam-BrSRTT-Data-fit",200)
changeBin("hamb-shapes-UnbinnedParam-BrSRTMexc-Data-fit",200)
changeBin("hamb-shapes-UnbinnedParam-BrSRTLexc-Data-fit",200)
 #/
 # meanerrors["a1"] = make_pair(0.0091, make_pair(0.00085,0.00085));
 # meanerrors["b1"] = make_pair(0.0172, make_pair(0.0017, 0.0017));
 # meanerrors["m1"] = make_pair(-0.069, make_pair(0.0066,0.0066));
 # FixedParams fixes;
 # fixes["alpha"] = 1.15;
 # fixes["width"] = 0.008;
 # fixes["n"] = 3.02;
 # fixes["frac"] = 0.57;
 #/
