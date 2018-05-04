import ROOT
import os
import stat
import numpy

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
cwd = os.getcwd()

fInWS = ROOT.TFile.Open("hamb-shapes-UnbinnedParam-BrSRTT-Data-fit.root")
InWS = fInWS.Get("w")
bkg_norm = InWS.arg("bkgshapeSRTT_norm")
bkg_mpdf = InWS.pdf("bkgshapeSRTT")
pdf_index = InWS.arg("pdfindexSRTT")
bkg_mpdf.SetName("bkgshape")
pdf_index.SetName("pdfindex")
bkg_norm.setRange( 0 , 10000)
#bkg_norm.removeRange()
#bkg_norm.setConstant()
#bkg_norm.setRange(0,5000)

args = {}
for arg in ["bern20","bern21","bern22", "bern30","bern31","bern32","bern33", "m0" , "k" , "p" ] :
    args[ arg ] = InWS.var( arg )
    if arg == "m0" :
        args[arg].setRange( 60 , 80)
    #args[arg].removeRange()
    #args[arg].setConstant()

sig_norm = InWS.arg("signal_norm")
sig_shap = InWS.arg("signal")
for arg in ["alpha" , "n" ,"m1",  "b1" , "a1" ] :
    args[ arg ] = InWS.var( arg )
    print arg
    if arg in ["m1" ,  "b1" , "a1" ] : #, "n" , "alpha"] :
        args[arg].setBins(100000)
        args[arg].Print()
    else:
        args[arg].removeRange()
        args[arg].setConstant()
MH = InWS.arg("MH")
new_sigma_cb = InWS.arg("sigma_cb") #ROOT.RooFormulaVar( "sigma_cb" , "sigma_cb" , "-0.0089+@1*@0+0.11*@0" , ROOT.RooArgList( MH , args["b1"] ) )

aMuMass = InWS.arg("aMuMass")
aMuMass.setBins(100000)

data = InWS.data("data")

fOutWS = ROOT.TFile.Open("HAMB2016.root" , "recreate")
fOutWS.cd()

for ch in ["TT" , "TMexc" , "TLexc"] :
    OutWS = ROOT.RooWorkspace("w" + ch)
    getattr( OutWS , "import")( bkg_norm.Clone( "%s_%s_norm" % (bkg_mpdf.GetName(), ch ) )  , ROOT.RooFit.RecycleConflictNodes() )
    getattr( OutWS , "import")( bkg_mpdf , ROOT.RooFit.RenameAllVariablesExcept(ch , "m1,a1,b1,aMuMass,MH") , ROOT.RooFit.RenameAllNodes(ch) , ROOT.RooFit.RecycleConflictNodes() )
    getattr( OutWS , "import")( new_sigma_cb , ROOT.RooFit.RenameAllVariablesExcept(ch , "m1,a1,b1,aMuMass,MH") , ROOT.RooFit.RenameAllNodes(ch) , ROOT.RooFit.RecycleConflictNodes() )
    getattr( OutWS , "import")( sig_norm.Clone( "%s_%s_norm" % (sig_shap.GetName(), ch ) ) , ROOT.RooFit.RenameAllVariablesExcept(ch , "MH"), ROOT.RooFit.RecycleConflictNodes() )
    getattr( OutWS , "import")( sig_shap , ROOT.RooFit.RenameAllVariablesExcept(ch , "m1,a1,b1,aMuMass,MH") , ROOT.RooFit.RenameAllNodes(ch) , ROOT.RooFit.RecycleConflictNodes() )
    getattr( OutWS , "import")( data )
    OutWS.Write()


fOutWS.Close()


fInWS.Close()
