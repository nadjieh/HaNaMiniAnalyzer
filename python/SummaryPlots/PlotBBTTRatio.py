from BR import *
import ROOT
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas


style1=GetStyleHtt()
style1.cd()


fOut = ROOT.TFile.Open("plots/brRatios.root" , "recreate")
fOut.cd()

for model in [1,2,3,4] :
    binbeta=200
    minbeta=0.5
    maxbeta=10.0
    minmass=20
    maxmass=60
    binmass=200
    
    if (model==4):
        minbeta=0.1
        maxbeta=6
    if (model==2):
        minbeta=0.3
    #   maxbeta=0.8

    
    histBRRatio=ROOT.TH2F("histBRRatio_%d" % model,"BR(a#to bb)/BR(a#to #tau#tau) model type = %d" % model,binmass,minmass,maxmass,binbeta,minbeta,maxbeta)
    for i in range(1,binmass+1):
        xxsm= histBRRatio.GetXaxis().GetBinCenter(i) #0.0000001+minmass+1.0*i*(maxmass-minmass)/(binmass)
        for b in range(1,binbeta+1):
            tanbeta=histBRRatio.GetYaxis().GetBinCenter( b )
            #width=get_total_width(model,float(xxsm),tanbeta)
    	    BRtautau=gamma_tau(tanbeta,float(xxsm),model) #/width
  	    BRbb=gamma_quarks(tanbeta,float(xxsm),model,6) #/width
            binindex = histBRRatio.GetBin( i , b ) #xxsm , tanbeta )
            histBRRatio.SetBinContent( binindex,BRbb/BRtautau)
    histBRRatio.Write()

fOut.Close()
