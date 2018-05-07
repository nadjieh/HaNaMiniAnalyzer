import ROOT as root

  # m1        :   +0.000  -0.001/+0.001  [WARNING] Found [bern20] at boundary. 
  #      RooRealVar::bern20 = 0.0124407 +/- 0.121345  L(0 - 0.552814) 
  # [WARNING] Found [bern22] at boundary. 
  #      RooRealVar::bern22 = 0.0222458 +/- 0.247059  L(0 - 1.11937) 
  # [WARNING] Found [bern32] at boundary. 
  #      RooRealVar::bern32 = 0.0900485 +/- 0.591474  L(0 - 2.75342) 
  # [WARNING] Found [bern33] at boundary. 
  #      RooRealVar::bern33 = 0.00798176 +/- 0.254651  L(0 - 1.12387) 
  # [WARNING] Found [m0] at boundary. 
  #      RooRealVar::m0 = 65 +/- 0.614941  L(60 - 65) 


def changeBin(infName, nBin):
	inf = root.TFile.Open("%s.root" %(infName))
	myW = inf.Get("w").Clone("myW")
	inf.Close()
	myW.var("b1").setBins(nBin)
	myW.var("b1").removeRange()
	myW.var("b1").setConstant()
	# myW.var("bern20").setMin(-1.)
	# myW.var("bern20").setMax(2.)
	# myW.var("bern22").setMin(-1.)
	# myW.var("bern32").setMin(-2.)
	# myW.var("bern33").setMin(-1.)
	myW.var("m0").setMax(70)
	outf = root.TFile("%s-%s.root" %(infName,nBin),"recreate")
	outf.cd()
	myW.SetName("w")
	myW.Write()
	outf.Close()

def changeBkgNorm(infName, nBkg):
	inf = root.TFile.Open("%s.root" %(infName))
	myW = inf.Get("w").Clone("myW")                                                                                                                                                                                                     
	inf.Close()
	varName = ""
	if infName.find("TT") > 0:
		print "I am TT"
		print infName.find("TT")
		varName = "bkgshapeSRTT_norm"
	elif infName.find("TLexc") > 0:
		print "I am TLexc"
		print infName.find("TLexc") 
		varName = "bkgshapeSRTLexc_norm"
	elif infName.find("TMexc") > 0:
		print infName.find("TMexc") 
		print "I am TMexc"
		varName = "bkgshapeSRTMexc_norm"
	myW.Print()
	print varName
	myW.var(varName).setVal(nBkg)
        myW.var(varName).setRange(0, 2*nBkg)
	myW.factory("argus_norm[%d,0,%d]" %(1000,2000))
	myW.var("b1").removeRange()
	myW.var("b1").setConstant()
	# myW.var("bern20").setMin(-0.5)
	# myW.var("bern22").setMin(-0.5)
	# myW.var("bern32").setMin(-0.5)
	# myW.var("bern33").setMin(-0.5)
	myW.var("m0").setMax(70)
        outf = root.TFile("%s-Bkg-%s.root" %(infName,nBkg),"recreate")                                                                                                                                                                           
        outf.cd()                                                                                                                                                                                                                            
        myW.SetName("w")                                                                                                                                                                                                                     
        myW.Write()                                                                                                                                                                                                                          
        outf.Close()

root.gSystem.Load("RooFit")
root.gSystem.Load("~/work/tHq/CMSSW_7_4_7/lib/slc6_amd64_gcc491/libHiggsAnalysisCombinedLimit.so")
# changeBin("hamb-shapes-UnbinnedParam-BrSRTT-Data-fit",1000)
# changeBin("hamb-shapes-UnbinnedParam-BrSRTT-Data-fit",5000)
# changeBin("hamb-shapes-UnbinnedParam-BrSRTMexc-Data-fit",1000)
# changeBin("hamb-shapes-UnbinnedParam-BrSRTMexc-Data-fit",5000)
# changeBin("hamb-shapes-UnbinnedParam-BrSRTLexc-Data-fit",1000)
# changeBin("hamb-shapes-UnbinnedParam-BrSRTLexc-Data-fit",5000)

# changeBkgNorm("hamb-shapes-UnbinnedParam-BrSRTT-Data-fit",1000)
# changeBkgNorm("hamb-shapes-UnbinnedParam-BrSRTT-Data-fit",5000)
changeBkgNorm("hamb-shapes-UnbinnedParam-BrSRTMexc-Data-fit",1000)
#changeBkgNorm("hamb-shapes-UnbinnedParam-BrSRTMexc-Data-fit",5000)
# changeBkgNorm("hamb-shapes-UnbinnedParam-BrSRTLexc-Data-fit",1000)
# changeBkgNorm("hamb-shapes-UnbinnedParam-BrSRTLexc-Data-fit",5000)
