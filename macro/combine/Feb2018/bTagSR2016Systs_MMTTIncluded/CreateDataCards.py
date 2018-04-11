import ROOT
import os
import stat
import Haamm.HaNaMiniAnalyzer.SummaryPlots.MuMu_bb as mmbb

ROOT.gSystem.Load("~/Desktop/tHq/HiggsAnalysis/CombinedLimit/lib/libHiggsAnalysisCombinedLimit.so")
cwd = os.getcwd()

fInWS = ROOT.TFile.Open("hamb-shapes-UnbinnedParam-BrSRTT-Data-fit.root")
InWS = fInWS.Get("w")
signalNorm = InWS.arg("signal_norm")
mass_var = InWS.arg("MH")

efficiencies = mmbb.EfficiencyReader()
modeltype = 3

os.mkdir( "model%d" % modeltype )
submitLx = open( "model%d/submit.sh" % modeltype , "w")

masses = [20 , 30 , 40 , 45 , 50 , 55 , 60]

for tanbeta in [2.0 , 3.5, 4.0 , 4.5 , 5.5 ]:
    print tanbeta
    dirName = "%s/model%d/tanbeta%d" % (cwd , modeltype ,tanbeta*10)
    os.makedirs( dirName )

    with open("runOnLxbatch.sh", "rt") as fin:
        with open( dirName + "/runOnLxbatch.sh" , "wt") as fout:
            for line in fin:
                lout = line.replace( "MODEL" , "%d"%modeltype  ).replace( "TANBETA" , "%d"%tanbeta*10  )
                fout.write( lout )

    st = os.stat(dirName + "/runOnLxbatch.sh")
    os.chmod(dirName + "/runOnLxbatch.sh", st.st_mode | stat.S_IEXEC)

    submitLx.write( "cd " + dirName + "\n" )
    submitLx.write( 'bsub -q 1nh -J "HambCombine' + str(masses) + " -o HambCombine%I.out `pwd`/runOnLxbatch.sh"  + "\n" )
    
    for mass in masses:
        mass_var.setVal( float(mass) )
        yieldinws = signalNorm.getVal()
        totalyields = efficiencies.GetSignalYields( "mmbb" , "total" , 2.0 , mass , 3. )
        correctedTotalYield = (1.7*0.001*totalyields)/(efficiencies.GetBR( "mmbb" , 2.0 , mass , 3. )*1.114)
        correctionfactor = 1.0/correctedTotalYield
        
        Ratio_TTM , Ratio_TTT = efficiencies.GetSignalYields( "mmbb" , "TT" , tanbeta , mass , modeltype ) ,  efficiencies.GetSignalYields( "mmtt" , "TT" , tanbeta , mass , modeltype ) 
        Ratio_TMM , Ratio_TMT = efficiencies.GetSignalYields( "mmbb" , "TM" , tanbeta , mass , modeltype ) ,  efficiencies.GetSignalYields( "mmtt" , "TM" , tanbeta , mass , modeltype )
        Ratio_TLM , Ratio_TLT = efficiencies.GetSignalYields( "mmbb" , "TL" , tanbeta , mass , modeltype ) ,  efficiencies.GetSignalYields( "mmtt" , "TL" , tanbeta , mass , modeltype )

        Ratio_TT = correctionfactor*(Ratio_TTM + Ratio_TTT)
        Ratio_TM = correctionfactor*(Ratio_TMM + Ratio_TMT)
        Ratio_TL = correctionfactor*(Ratio_TLM + Ratio_TLT)
        
        
        print "\t" , mass , yieldinws , Ratio_TL + Ratio_TM + Ratio_TT
        print "\t\t" , "TT" , Ratio_TT , Ratio_TTT/(Ratio_TTM+Ratio_TTT)
        print "\t\t" , "TM" , Ratio_TM , Ratio_TMT/(Ratio_TMM+Ratio_TMT)
        print "\t\t" , "TL" , Ratio_TL , Ratio_TLT/(Ratio_TLM+Ratio_TLT)
        
        with open("bTagSR2016Systs.txt", "rt") as fin:
            with open( dirName + "/Mass%d.txt"%(mass), "wt") as fout:
                for line in fin:
                    lout = line.replace( "TLSIG" , "%.6f"%Ratio_TL  ).replace( "TMSIG" , "%.6f"%Ratio_TM  ).replace( "TTSIG" , "%.6f"%Ratio_TT  )
                    fout.write( lout )


        
