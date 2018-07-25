import ROOT
import math
from uncertainties import ufloat
import array

fIn = ROOT.TFile.Open("out_FinalPlots_HambbWsShape.root")
ROOT.gSystem.Load( "/home/hbakhshi/Desktop/tHq/HiggsAnalysis/CombinedLimit/libHiggsAnalysisCombinedLimit.so" )

TL_ggh = None
TL_vbf = None
TL_sum = None

xvals = array.array('d')
yvals = array.array('d')

for signal in [ "20" , "40" , "60" ] :
    print signal
    xvals.append( float( signal ) )
    for dirName in ["SRTL" ] : # , "SRTLexc" , "SRTMexc" , "SRTT"  ]:
        h_ggh = fIn.Get("%s/General/amuMass/signals/%s_amuMass_Signal%s" % (dirName , dirName , signal) )
        h_vbf = fIn.Get( "%s/General/amuMass/signals/%s_amuMass_SignalVBF%s" % (dirName , dirName , signal) )

        err_ggh = ROOT.Double()
        i_ggh = h_ggh.IntegralAndError( 0 , 1000 , err_ggh )

        err_vbf = ROOT.Double()
        i_vbf = h_vbf.IntegralAndError( 0 , 1000 , err_vbf )

        ggh = ufloat( i_ggh , err_ggh )
        vbf = ufloat( i_vbf , err_vbf )

        sum_signal = ggh+vbf
        ratio_ggh_vbf = sum_signal/ggh
        
        if dirName == "SRTL" :
            TL_ggh = ufloat( i_ggh , err_ggh )
            TL_vbf = ufloat( i_vbf , err_vbf )
            TL_sum = TL_ggh + TL_vbf

            yvals.append( ratio_ggh_vbf.n )
            
        ratio_ggh = ggh/TL_ggh
        ratio_vbf = vbf/TL_vbf
        ratio_sum = sum_signal/TL_sum
        
        print "\t" , dirName, ratio_ggh_vbf

aMuMass = ROOT.RooRealVar("aMuMass", "aMuMass", 20, 62.5)
spline = ROOT.RooSpline1D("test" , "title" , aMuMass , 3 , xvals , yvals )
frame = aMuMass.frame()
spline.plotOn( frame )
frame.Draw()
