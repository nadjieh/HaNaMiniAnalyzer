import ROOT
import math

#to install uncertainties :
#   1 : pip install --upgrade uncertainties
#or 2 : download it from https://pypi.org/project/uncertainties/#files
#       and run python setup.py install --user
from uncertainties import ufloat
import array

fIn = ROOT.TFile.Open("out_FinalPlots_HambbWsShape.root")
ROOT.gSystem.Load( "libHiggsAnalysisCombinedLimit.so" )

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

            yvals.append( 1.114*ratio_ggh_vbf.n )
            
        ratio_ggh = ggh/TL_ggh
        ratio_vbf = vbf/TL_vbf
        ratio_sum = sum_signal/TL_sum
        
        print "\t" , dirName, ratio_ggh_vbf
fIn.Close()

xvals.append(62.5)
yvals.append(yvals[-1])
#frame = aMuMass.frame()
#spline.plotOn( frame )
#frame.Draw()

fSignalOld = ROOT.TFile.Open("../macro/combine/Unblinding/LimitCalculations/HAMB2016GGFOnly.root")
fSignalNew = ROOT.TFile.Open("../macro/combine/Unblinding/LimitCalculations/HAMB2016.root" , "RECREATE")

for region in ["TT" , "TLexc" , "TMexc"]:
    wsOld = fSignalOld.Get("w%s" % region )
    ws = ROOT.RooWorkspace( wsOld )
    old_norm = ws.function( "signal_%s_norm" % region )
    old_norm.SetName(  "signal_ggh_%s_norm" % region )

    aMuMass = ws.arg("MH")
    correction_factor = ROOT.RooSpline1D("vbf_%s" % region , "vbf factor + 48/44 correction factor" , aMuMass , 4 , xvals , yvals )

    new_norm = ROOT.RooFormulaVar( "signal_%s_norm" % region , old_norm.GetTitle() , "@0*@1" , ROOT.RooArgList( correction_factor , old_norm ) )
    getattr( ws , 'import')( new_norm )


    fSignalNew.cd()
    ws.Write()
    ws.Print()

fSignalNew.Close()
fSignalOld.Close()
