import ROOT
from BR import *
import array
import numpy as np
import math
import os

colors = []
def newColor(red,green,blue , alpha = 0.8):
    newColor.colorindex+=1
    color=ROOT.TColor(newColor.colorindex,red,green,blue , "" , alpha)
    colors.append(color)
    return color, newColor.colorindex
    
newColor.colorindex=301

class EfficiencyReader:
    def __init__(self, fname= os.path.dirname(os.path.abspath(__file__)) + "/InputSignalEfficiencies.root"):
        self.InputFile = ROOT.TFile.Open( fname )

        self.mmbb = {}
        self.mmtt = {}
        self.ttbb = {}
        self.CatNames = {"TL":"SRTLexc" , "TM":"SRTMexc" , "TT":"SRTT"}
        for cat in self.CatNames :
            dirName = self.CatNames[cat]
            self.mmbb[cat] = self.GetCategoryEffGraph( "" , dirName , {20:2.00000000000000000e+05 , 25:9.60100000000000000e+04 , 30:1.99235000000000000e+05 , 40:2.00000000000000000e+05 , 45:2.00000000000000000e+05 , 50:2.00000000000000000e+05 , 55:2.00000000000000000e+05 , 60:2.00000000000000000e+05 } )
            self.mmtt[cat] = self.GetCategoryEffGraph( "mmtt" , dirName , {20:2.50000000000000000e+05 , 40:2.50000000000000000e+05 , 60:2.49252000000000000e+05 } )
            self.ttbb[cat] = self.GetCategoryEffGraph( "bbtt" , dirName , {20:4.18969000000000000e+05/0.1426 , 40:3.91355000000000000e+05/0.1322 , 60:3.39000000000000000e+05/0.1133 } )

        self.InputFile.Close()
        self.TempList = []

    def GetEfficiency(self , sample , catName , mass ):
        # if sample == "mmbb" and catName != "total":
        #     totalEff = self.GetTotalEff( sample , mass )
        #     if catName == "TT" :
        #         return 0.27*totalEff
        #     elif catName == "TM" :
        #         return 0.32*totalEff
        #     elif catName == "TL" :
        #         return 0.41*totalEff

        if catName == "total":
            return self.GetTotalEff( sample , mass )
        else :
            return getattr( self , sample )[catName].Eval( mass , 0 , "S" )
        
    def GetMMBBEfficiency(self , catName , mass ):
        return self.mmbb[catName].Eval( mass , 0 , "S" )
    def GetMMTTEfficiency(self , catName , mass ):
        return self.mmtt[catName].Eval( mass , 0 , "S" )
    def GetTTBBEfficiency(self , catName , mass ):
        return self.ttbb[catName].Eval( mass , 0 , "S" )
    def GetTotalEff(self, sample , mass):
        eff = 0.0
        for cat in self.CatNames :
            if sample == "mmbb" :
                eff += self.GetMMBBEfficiency( cat , mass )
            else :
                eff += self.GetEfficiency(sample , cat , mass )
        return eff
        

    def GetEffRatio( self , sample1 , sample2 , cat , color ):
        x = array.array('d' , [] )
        y = array.array('d' , [] )
        for mass in np.linspace(20 , 62.5 , 85 ):
            eff1 = self.GetEfficiency( sample1 , cat , mass )
            eff2 = self.GetEfficiency( sample2 , cat , mass )
            x.append(mass)
            ratio = 0. if eff2==0.0 else eff1/eff2
            y.append(ratio)

        ret = ROOT.TGraph( len(x) , x , y )
        ret.SetTitle( "%s/%s , %s" % (sample1 , sample2 , cat) )
        ret.SetMarkerStyle(20)
        ret.SetMarkerColor(color)
        self.TempList.append(ret)
        return ret
    def PlotEffRatio(self, sample1 , sample2):
        color = 2
        self.GetEffRatio(sample1 , sample2 , "total" , color).Draw("AP")
        for cat in self.CatNames:
            color += 1
            self.GetEffRatio(sample1 , sample2 , cat , color).Draw("P")

    def GetBR(self, sample ,  tanb , m , modeltype):
        width=get_total_width(modeltype,m,tanb)
    	BRmm=gamma_mu(tanb,m,modeltype)
  	BRbb=gamma_quarks(tanb,m,modeltype,6)
        BRtt=gamma_tau(tanb,m,modeltype)
        BR = 0.0
        if sample == "mmbb" :
            BR = 2*BRmm*BRbb/(width*width)
        elif sample == "mmtt" :
            BR = 2*BRmm*BRtt/(width*width)
        elif sample == "ttbb" :
            BR = 2*BRtt*BRbb/(width*width)

        return BR

    def GetSignalYields(self, sample , cat , tanb , m , modeltype , lumi=35900 , xsection=48.5800 , brHaa = 0.1):
        BR = self.GetBR( sample , tanb , m , modeltype )
        return lumi*xsection*brHaa*BR*self.GetEfficiency( sample , cat , m )

    def GetSignalYieldsPlot( self, sample , cat , modeltype , lumi=35900 , xsection=48.5800 , brHaa = 0.1):
        name = "h2d_%s_%s_%d_signalyield" % (sample , cat , modeltype)
        title = "Signal yilds for %s in category %s for model type %d" % (sample , cat , modeltype )
        if hasattr(self, name ):
            return getattr(self, name)
        
        binmass = 170
        binbeta = 50
        h2d = ROOT.TH2D( name , title , binmass , 20 , 62.5 , binbeta , 0.1 , 5.1 )

        for i in range(1,binmass+1):
            mass = h2d.GetXaxis().GetBinCenter(i) #0.0000001+minmass+1.0*i*(maxmass-minmass)/(binmass)
            for b in range(1,binbeta+1):
                tanbeta=h2d.GetYaxis().GetBinCenter( b )
                binindex = h2d.GetBin( i , b ) #xxsm , tanbeta )
                yields = self.GetSignalYields( sample , cat , tanbeta , mass , modeltype , lumi, xsection , brHaa )

   	        h2d.SetBinContent(binindex,yields)
        
        self.TempList.append( h2d )
        return h2d
    
    def PlotYieldRatio(self, sample1 , sample2 , modeltype):
        ROOT.gStyle.SetOptStat(0)
        canvas = ROOT.TCanvas( "signalyields_%s_%s_%d" % (sample1 , sample2 , modeltype) )
        canvas.SetLogz()
        canvas.Divide(2,2)
        canvas.cd(1).SetLogz()
        htotal = self.GetSignalYieldsPlot( sample1 , "total" , modeltype , 1. , 1. , 1. )
        htotal.Divide( self.GetSignalYieldsPlot( sample2 , "total" , modeltype , 1. , 1. , 1. ) )
        htotal.SetTitle( ("%s/%s" % (sample1, sample2)).replace("m" , "#mu").replace("t" , "#tau") + " TYPE %d" % modeltype )
        htotal.Draw("COLZ")
        self.TempList.append( htotal )
        
        npad = 1
        for cat in self.CatNames:
            npad += 1
            canvas.cd( npad ).SetLogz()
            h_cat = self.GetSignalYieldsPlot( sample1 , cat , modeltype , 1. , 1. , 1. )
            h_cat.Divide( self.GetSignalYieldsPlot( sample2 , cat , modeltype , 1. , 1. , 1. ) )
            h_cat.SetTitle( self.CatNames[cat] )
            h_cat.Draw("COLZ")
            self.TempList.append( h_cat )

        self.TempList.append( canvas )
        canvas.SaveAs("plots/signalyields_%s_%s_%d.pdf" % (sample1 , sample2 , modeltype) )
        return canvas
    
    
    def GetCategoryEffGraph(self , sampleName , catName , masses ):
        x = array.array('d' , [])
        ex = array.array('d' , [])
        y = array.array('d' , [])
        ey = array.array('d' , [])
        for mass in masses :
            total = masses[mass]                                           
            hist = self.InputFile.Get("%s/General/amuMass/signals/%s_amuMass_Signal%s%d" % (catName , catName , sampleName , mass ) )
            nSelected = hist.GetEntries()
            eff = float(nSelected)/total
            if nSelected == 0:
                err = 0
            else:
                err = eff*math.sqrt( 1.0/float(nSelected) + 1.0/float(total) )
            x.append(mass)
            ex.append(0)
            y.append(eff)
            ey.append(err)
            
        ROOT.gROOT.cd()    
        graph = ROOT.TGraphErrors(len(x) , x , y , ex , ey)
        name = "Eff_%s_amuMass_Signal%s" % (catName , sampleName)
        graph.SetName(name)
        setattr( self , name , graph )
        return graph

class LimitReader:
    def __init__(self, fname , color = ROOT.kOrange-4):
        self.Color = color

        tColor=ROOT.gROOT.GetColor(color)
        trans1, ShadeColor =newColor(tColor.GetRed(), tColor.GetGreen(),tColor.GetBlue() , 0.9 )
        self.ShadeColor = ShadeColor 
        self.File = ROOT.TFile.Open( fname )
        ROOT.gROOT.cd()
        self.MedianGraph = self.File.Get("median").Clone()
        self.g2sigmaBand = self.File.Get("graph2sigma").Clone()
        self.g1sigmaBand = self.File.Get("graph1sigma").Clone()
        self.File.Close()
        ROOT.gROOT.cd()
        self.gp2sigma = self.ProduceUpDownPlots( self.g2sigmaBand , +1 )
        self.gm2sigma = self.ProduceUpDownPlots( self.g2sigmaBand , -1 )
        self.gp1sigma = self.ProduceUpDownPlots( self.g1sigmaBand , +1 )
        self.gm1sigma = self.ProduceUpDownPlots( self.g1sigmaBand , -1 )
        self.AllGraphs = {-2:self.gm2sigma , -1:self.gm1sigma , 0:self.MedianGraph , +1:self.gp1sigma , +2:self.gp2sigma }
        self.MassLimits = {}

        self.EfficiencyReader = EfficiencyReader()
        
    def ProduceUpDownPlots(self, graph , w ):
        x_ = []
        y_ = []

        X = ROOT.Double(0)
        Y = ROOT.Double(0)
        for point in range(0 , graph.GetN() ):
            graph.GetPoint( int(point) , X , Y )
            x_.append( X.real )
            if w > 0 :
                YError = graph.GetErrorYhigh( point )
            elif w < 0 :
                YError = (-1 * graph.GetErrorYlow( point ))
            y_.append( Y.real + YError )
        x = array.array('d' , x_)
        y = array.array('d' , y_)
        ret = ROOT.TGraph( graph.GetN() , x , y )
        ret.SetName( "graph%s%d" % ( "p" if w > 0 else "m" , abs( w ) ) )
        return ret
        
    def GetLimit(self , mass , index = 0 ):
        if mass in self.MassLimits :
            limit = self.MassLimits[mass]
        else :
            limit = self.AllGraphs[index].Eval( mass , 0 , "S" )/1.114
            self.MassLimits[mass] = limit

        return limit
        
    def GetModelLimit( self , modelType , mass , tanB , index = 0 ):
        limit = self.GetLimit(mass , index)
        width=get_total_width(modelType,mass,tanB)
    	BRmm=gamma_mu(tanB,mass,modelType)/width
  	BRbb=gamma_quarks(tanB,mass,modelType,6)/width
        ysm=(limit/(2*BRmm*BRbb))
        return ysm , limit , width , BRmm , BRbb

    def GetModelLimitTTNormalized(self , modelType , mass , tanB , index = 0 ):
        mmbb = self.EfficiencyReader.GetSignalYields( "mmbb" , "total" , tanB , mass , modelType , 1. , 1. , 1.)
        mmtt = self.EfficiencyReader.GetSignalYields( "mmtt" , "total" , tanB , mass , modelType , 1. , 1. , 1. )
        upperbound = self.GetModelLimit( modelType , mass , tanB , index )[0]
        ratio = 1.0 + mmtt/mmbb
        return upperbound/ratio , ratio , upperbound
    
    def ProduceGraphTanbBeta( self, modelType , tanB , minM = 20 , maxM = 62.5 , bins = 200 , ymax = None ):
        name = "vsMass%.2f_%.2f_%d_tbeta%.2f_model%d" % (minM , maxM , bins , tanB , modelType )
        if hasattr( self , name ):
            return getattr( self , name )

        x = array.array('d' , [])
        y = array.array('d' , [])
        y_low = array.array('d' , [])
        y_high = array.array('d' , [])
        x_err = array.array('d' , [])
        if ymax :
            for mass in np.linspace(minM , maxM , bins ):
                x.append( mass )
                x_err.append(0)
                y.append( ymax )
                y_low.append(0)
                y_high.append(0)
        for mass in np.linspace(minM , maxM , bins )[::-1]:
            x.append( mass )
            x_err.append(0)
            Y = self.GetModelLimit( modelType , mass , tanB , 0)
            Y_high = self.GetModelLimit( modelType , mass , tanB , 1)
            Y_low = self.GetModelLimit( modelType , mass , tanB , -1)

            y.append( Y[0] )
            y_low.append( abs(Y_low[0] - Y[0] ) )
            y_high.append( abs(Y_high[0] - Y[0] ) )

        if ymax :
            ret = ROOT.TGraph( len(x) , x , y )
            ret.SetFillStyle(3001)
            ret.SetFillColor( self.ShadeColor)

        else:
            #ret = ROOT.TGraphAsymmErrors( len(x) , x , y , x_err , x_err , y_low , y_high )
            ret = ROOT.TGraph( len(x) , x , y )
        ret.SetLineWidth(1)
        ret.SetLineColor( self.Color )

        setattr( self , name , ret )

        return ret
