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
    cat = ROOT.RooCategory( "%s_Category" % (region) , "%s_Category" % (region) )
    args = ROOT.RooArgList()
    for Id in IdIndices:
        for index in IdIndices[Id] :
            args.add( GetPdf( Id , nbins , region , index ) )
    AuxMultiPdfs.append( cat )
    AuxMultiPdfs.append( args )

    ret = ROOT.RooMultiPdf( region , region , cat , args )
    AuxMultiPdfs.append( ret )

    return ret


TT_IdIndices = { 0:[1,2] , 1:[1] , 3:[1] }
TT_MPdf = MakeMultiPdf( "TT" , 20 , TT_IdIndices )

