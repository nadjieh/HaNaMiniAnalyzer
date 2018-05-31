import ROOT
import os
import stat
import numpy

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
cwd = os.getcwd()


def GetFileName( pdfId , nbins , region ):
    name = ""
    if pdfId==0:
        name = "gen"
    elif pdfId==1:
        name = "Inv"
    elif pdfId==2:
        name="Cheb"
    elif pdfId==3:
        name="bern"

    region_n = region
    if region in ["T" , "TT" , "t" , "tt" ] :
        region_n = "TT"
    elif region in ["TM" , "M" , "tm" , "m" ] :
        region_n = "TMexc"
    elif region in ["TL" , "L" , "tl" , "l" ] :
        region_n = "TLexc"
        
    fName = "%s_nbins%d_%s.root" % (name , nbins , region_n)
    return fName

Datasets = {}
aMuMass = ROOT.RooRealVar("aMuMass", "aMuMass", 20, 62.5)
aMuMass.setBins( 100000 )

def MakeDataset(region):
    input = ROOT.TFile.Open(region + ".root")
    tree = input.Get("Hamb/Trees/Events")
    data = ROOT.RooDataSet("Dataset_" + region, "The original control data for " + region, tree, ROOT.RooArgSet(aMuMass), "")

    Datasets[ region ] = data
    return data

AuxPDF = []
def GetPdf( pdfId , nbins , region , pdfIndex ):
    fName = GetFileName( pdfId , nbins , region )
    f_ = ROOT.TFile.Open( fName )

    if pdfId==0:
        name = "WS"
        pdfName = "PolyPdf" 
    elif pdfId==1:
        name = "InvWS"
        pdfName = "InvPoly"
    elif pdfId==2:
        name="ChebWS"
        pdfName = "Chebychev" 
    elif pdfId==3:
        name="BernWS"
        pdfName = "Bernstein"

    ws = f_.Get( name )
    pdf = ws.pdf( "%s_%d" % (pdfName , pdfIndex) )

    AuxPDF.append( pdf )
    return pdf

AuxMultiPdfs = []
def MakeMultiPdf(region , nbins , IdIndices ):
    cat = ROOT.RooCategory( "pdfIndex" , "%s_Category" % (region) )
    args = ROOT.RooArgList()
    for Id in IdIndices:
        for index in IdIndices[Id] :
            args.add( GetPdf( Id , nbins , region , index ) )
    AuxMultiPdfs.append( cat )
    AuxMultiPdfs.append( args )

    ret = ROOT.RooMultiPdf( "BkgShape" , region , cat , args )
    AuxMultiPdfs.append( ret )

    return ret



ws = ROOT.RooWorkspace("HMuMubbWS")
getattr( ws , "import")( aMuMass )

TT_IdIndices = { 0:[1,2] , 1:[1] , 2:[] , 3:[1] }
TT_MPdf = MakeMultiPdf( "TT" , 20 , TT_IdIndices )
TT_Dataset = MakeDataset("TT")
TT_Norm = ROOT.RooRealVar("BkgShape_TT_norm" , "TT_norm" , TT_Dataset.numEntries() , 0 , 10*TT_Dataset.numEntries() )

getattr( ws , "import")( TT_MPdf , ROOT.RooFit.RenameAllVariablesExcept("TT" , "m1,a1,b1,aMuMass,MH") , ROOT.RooFit.RenameAllNodes("TT") , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TT_Norm , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TT_Dataset )


TM_IdIndices = { 0:[1,2,3,4] , 1:[1,2,3] , 2:[2,3] , 3:[3,4] }
TM_MPdf = MakeMultiPdf( "TMexc" , 40 , TM_IdIndices )
TM_Dataset = MakeDataset("TMexc")
TM_Norm = ROOT.RooRealVar("BkgShape_TMexc_norm" , "TMexc_norm" , TM_Dataset.numEntries() , 0 , 10*TM_Dataset.numEntries() )

getattr( ws , "import")( TM_MPdf , ROOT.RooFit.RenameAllVariablesExcept("TMexc" , "m1,a1,b1,aMuMass,MH") , ROOT.RooFit.RenameAllNodes("TMexc") , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TM_Norm , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TM_Dataset )


TL_IdIndices = { 0:[3,4,5] , 1:[2,3,4] , 2:[2] , 3:[] }
TL_MPdf = MakeMultiPdf( "TLexc" , 50 , TL_IdIndices )
TL_Dataset = MakeDataset("TLexc" )
TL_Norm = ROOT.RooRealVar("BkgShape_TLexc_norm" , "TLexc_norm" , TL_Dataset.numEntries() , 0 , 10*TL_Dataset.numEntries() )

getattr( ws , "import")( TL_MPdf , ROOT.RooFit.RenameAllVariablesExcept("TLexc" , "m1,a1,b1,aMuMass,MH") , ROOT.RooFit.RenameAllNodes("TLexc") , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TL_Norm , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TL_Dataset )


fOut = ROOT.TFile.Open( "UnblindedWS.root" , "recreate" )
ws.Write()
fOut.Close()
