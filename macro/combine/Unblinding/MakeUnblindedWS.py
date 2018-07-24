import ROOT
import os
import stat
import numpy
import re

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
aMuMass.setBins( 400 )

def MakeDataset(region):
    if region in Datasets :
        return Datasets[ region ]

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

def IsPositive( pdf , region ):
    return True
    hasNegativeParam = False

    data = MakeDataset( region )
    argset = pdf.getParameters( data )
    itr_params = argset.fwdIterator()
    for i_param in range(0 , argset.getSize() ) :
        param = itr_params.next()
        p_val = param.getValV()
        p_min = param.getMin()
        p_max = param.getMax()
        p_err = param.getError()
        if p_max < 0 :
            if abs(p_err / p_val ) > 0.2 :
                param.setRange( 0 , 10*p_err )
                param.setVal( 0 )
            else:
                param.Print()
                hasNegativeParam = True
        elif p_min < 0:
            param.setRange( 0 , p_max )
            param.setVal( p_max/2.0 )
    
    return not hasNegativeParam

AuxMultiPdfs = []
def MakeMultiPdf(region , nbins , IdIndices ):
    cat = ROOT.RooCategory( "pdfIndex" , "%s_Category" % (region) )
    args = ROOT.RooArgList()
    for Id in IdIndices:
        for index in IdIndices[Id] :
            pdf = GetPdf( Id , nbins , region , index )
            if IsPositive( pdf , region ):
                args.add( pdf )
            else:
                print "pdf %s was not added, as one of the parameters is negative" % pdf.GetName()
    AuxMultiPdfs.append( cat )
    AuxMultiPdfs.append( args )

    args.Print()
    ret = ROOT.RooMultiPdf( "BkgShape" , region , cat , args )
    AuxMultiPdfs.append( ret )

    return ret


AuxObjects = []
def PlotMultiPdf(frame , mpdf , data , header ):
    plot = data.plotOn( frame )
    h = plot.getHist()
    y = h.GetY()
    yh = h.GetEYhigh()
    for i in range(0 , h.GetN() ):
        if y[i] == 0:
            h.SetPointEYhigh( i , 1.8 )
    legend = ROOT.TLegend(0.1,0.7,0.48,0.9)
    legend.SetFillStyle(0)
    legend.SetLineColor(0)
    legend.SetHeader( header  )
    legend.AddEntry( plot.getHist() , "Data" , "lp" )
    AuxObjects.append( legend )
    colors = [ 2,3,4,5,6,7,8,9,28,46,41]
    for ipdf in range(0 , mpdf.getNumPdfs() ):
        pdf = mpdf.getPdf(ipdf)
        title = pdf.GetName()
        title_re = re.match( r'(.*)_(\d)' , title , re.M|re.I )
        print title_re.group(1) , title_re.group(2)
        title = "%s %s" % ( {"PolyPdf":"Polynomial" , "InvPoly":"Inv. Poly" , "Bernstein":"Bernstein" , "Chebychev":"Chebychev"}[title_re.group(1)] , 
                            {"1":"I" , "2":"II" , "3":"III" , "4":"IV" , "5":"V" , "6":"VI" , "7":"VII" , "8":"VIII" , "9":"IX" , "10":"X"}[title_re.group(2)] )

        plot = pdf.plotOn( frame , ROOT.RooFit.LineColor( colors[ipdf] ) )
        plot.getCurve().SetTitle(title)
        legend.AddEntry( plot.getCurve() , title , "l" )
    return legend

ws = ROOT.RooWorkspace("HMuMubbWS")
getattr( ws , "import")( aMuMass )

TT_IdIndices = { 0:[1,2] , 1:[1] , 2:[] , 3:[1] }
TT_MPdf = MakeMultiPdf( "TT" , 20 , TT_IdIndices )
TT_Dataset = MakeDataset("TT")
TT_Norm = ROOT.RooRealVar("BkgShape_TT_norm" , "TT_norm" , TT_Dataset.numEntries() , 0 , 10*TT_Dataset.numEntries() )

getattr( ws , "import")( TT_MPdf , ROOT.RooFit.RenameAllVariablesExcept("TT" , "m1,a1,b1,aMuMass,MH") , ROOT.RooFit.RenameAllNodes("TT") , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TT_Norm , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TT_Dataset )


aMuMass_TT = ROOT.RooRealVar("aMuMass", "aMuMass", 20, 62.5)
aMuMass_TT.setBins( 20 )

frame_TT = aMuMass_TT.frame()
legend = PlotMultiPdf( frame_TT , TT_MPdf , TT_Dataset , "TT Category" )
canvas_TT = ROOT.TCanvas("BkgPdfs_TT")
frame_TT.Draw()
legend.Draw()

TM_IdIndices = { 0:[1,2,3,4] , 1:[1,2,3] , 2:[2,3] , 3:[3,4] }
TM_MPdf = MakeMultiPdf( "TMexc" , 40 , TM_IdIndices )
TM_Dataset = MakeDataset("TMexc")
TM_Norm = ROOT.RooRealVar("BkgShape_TMexc_norm" , "TMexc_norm" , TM_Dataset.numEntries() , 0 , 10*TM_Dataset.numEntries() )

getattr( ws , "import")( TM_MPdf , ROOT.RooFit.RenameAllVariablesExcept("TMexc" , "m1,a1,b1,aMuMass,MH") , ROOT.RooFit.RenameAllNodes("TMexc") , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TM_Norm , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TM_Dataset )

aMuMass_TM = ROOT.RooRealVar("aMuMass", "aMuMass", 20, 62.5)
aMuMass_TM.setBins( 40 )

frame_TMexc = aMuMass_TM.frame()
legend = PlotMultiPdf( frame_TMexc , TM_MPdf , TM_Dataset , "TMexc Category" )
canvas_TMexc =ROOT.TCanvas("BkgPdfs_TMexc")
frame_TMexc.Draw()
legend.Draw()

TL_IdIndices = { 0:[3,4,5] , 1:[2,3,4] , 2:[2] , 3:[] }
TL_MPdf = MakeMultiPdf( "TLexc" , 50 , TL_IdIndices )
TL_Dataset = MakeDataset("TLexc" )
TL_Norm = ROOT.RooRealVar("BkgShape_TLexc_norm" , "TLexc_norm" , TL_Dataset.numEntries() , 0 , 10*TL_Dataset.numEntries() )

getattr( ws , "import")( TL_MPdf , ROOT.RooFit.RenameAllVariablesExcept("TLexc" , "m1,a1,b1,aMuMass,MH") , ROOT.RooFit.RenameAllNodes("TLexc") , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TL_Norm , ROOT.RooFit.RecycleConflictNodes() )
getattr( ws , "import")( TL_Dataset )

aMuMass_TL = ROOT.RooRealVar("aMuMass", "aMuMass", 20, 62.5)
aMuMass_TL.setBins( 50 )

frame_TLexc = aMuMass_TL.frame()
legend = PlotMultiPdf( frame_TLexc , TL_MPdf , TL_Dataset , "TLexc Category" )
canvas_TLexc = ROOT.TCanvas("BkgPdfs_TLexc")
frame_TLexc.Draw()
legend.Draw()

fOut = ROOT.TFile.Open( "UnblindedWS.root" , "recreate" )
ws.Write()
canvas_TT.Write()
canvas_TLexc.Write()
canvas_TMexc.Write()
fOut.Close()
