import ROOT
import os
import stat
import Haamm.HaNaMiniAnalyzer.SummaryPlots.MuMu_bb as mmbb
import numpy
import os.path

cwd = os.getcwd()

efficiencies = mmbb.EfficiencyReader()
limitReader = mmbb.LimitReader( "../bTagSR2016Systs/myLimitXsec.root" )
modeltype = 3

tanbetas = numpy.linspace( 0.01 , 10.01 , 100 , endpoint=False )
masses = numpy.linspace( 20 , 62.5 , 17 , endpoint=False )

h2d = ROOT.TH2D("hLimitMedian" , "#tau#tau + #mu#mu in type %d" %modeltype , len(masses) , 20 , 62.5 , len(tanbetas) , 0.01 , 10.01 )

for tanbeta in tanbetas:
    print tanbeta
    dirName = "%s/model%d/tanbeta%d" % (cwd , modeltype , tanbeta*100)
    mass_indices = []
    for mass_i in range(len(masses)):
        mass = masses[mass_i]

        bin_id = h2d.FindBin( mass+0.1 , tanbeta+0.01 )

        if int(mass)-mass == 0 :
            fName = dirName + "/higgsCombineTest.Asymptotic.mH%d.root" % int(mass)
        else:
            fName = dirName + "/higgsCombineTest.Asymptotic.mH%.1f.root" % mass


        if os.path.isfile( fName ):
            fffIn = ROOT.TFile.Open( fName )
            if fffIn :
                h2d.SetBinContent( bin_id , limitReader.ExtractLimit( fName ) )
            else:
                h2d.SetBinContent( bin_id , -1. )
        else:
            newupperbound, tb_ratio , old_limit = limitReader.GetModelLimitTTNormalized(modeltype , mass , tanbeta , index = 0 )
            h2d.SetBinContent( bin_id , newupperbound )
            

fOut = ROOT.TFile.Open("limits%d.root" % modeltype , "recreate")
h2d.Write()
fOut.Close()
