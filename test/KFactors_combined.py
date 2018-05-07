import ROOT as root
from Haamm.HaNaMiniAnalyzer.Property import *
import math


selections = [ "PreselectionLL" , "PreselectionTL", "PreselectionMM", "PreselectionTM", "PreselectionTT" ]

low_DYmass = 35.
low_DYmass_window_size = 15.0

ZMass = 91.
window_size = 10.0

f_in = root.TFile.Open( "out_FinalPlots_Hambcentral.root" )

for selection in selections:
        #print "Processing " + selection
	dir_in = f_in.GetDirectory( selection + "/General/amuMass")
        #print "Retrieved directory " + selection + "/General/amuMass" + " sucessfully"
	amuMass = Property.FromDir( dir_in )
	dataMbkg=amuMass.SubtractDataMC(["Top" , "DiBoson"])
	DY = amuMass.Bkg["DY"]
        #find bins for low DY mass
        low_mass_bin_1 = DY.FindBin(low_DYmass - low_DYmass_window_size)
        low_mass_bin_2 = DY.FindBin(low_DYmass + low_DYmass_window_size)
        #find bins for high DY mass
	bin_1 = DY.FindBin( ZMass - window_size )
	bin_2 = DY.FindBin( ZMass + window_size )

	low_Err_DY = root.Double()
	Err_DY = root.Double()

        DY_NotInZPeak = DY.IntegralAndError(low_mass_bin_1, low_mass_bin_2, low_Err_DY)
	DY_InZPeak = DY.IntegralAndError(bin_1 , bin_2 , Err_DY)

	low_Err_Data = root.Double()
	Err_Data = root.Double()
	Data_NotInZPeak = dataMbkg.IntegralAndError( low_mass_bin_1 , low_mass_bin_2, low_Err_Data )
	Data_InZPeak = dataMbkg.IntegralAndError( bin_1 , bin_2 , Err_Data )
	#print  "Lower bin is %f and upper bin is %f " %(bin_1, bin_2) 
        #print  "Error on data is %f and Error on DY is %f" %(Err_Data , Err_DY)
	kfactorlow = Data_NotInZPeak/DY_NotInZPeak
	kfactorhigh = Data_InZPeak/DY_InZPeak
	print selection + " Low Mass KFactor is %.2f +- %.2f " % (kfactorlow, kfactorlow*sqrt( (low_Err_Data.real/Data_NotInZPeak)*(low_Err_Data.real/Data_NotInZPeak) + (low_Err_DY.real/DY_NotInZPeak)* (low_Err_DY.real/DY_NotInZPeak) ) )
	print selection + " High Mass KFactor is %.2f +- %.2f " % (kfactorhigh, kfactorhigh*sqrt( (Err_Data.real/Data_InZPeak)*(Err_Data.real/Data_InZPeak) + (Err_DY.real/DY_InZPeak)* (Err_DY.real/DY_InZPeak) ) )


