#! /usr/bin/env python

import ROOT
import re

dsnames = {'All':(ROOT.kBlack,), 'eraA':(ROOT.kBlue,) , 'eraB':(ROOT.kRed,) }
class DataPU:
    def __init__(self, f , color , title , Range=range( 840 , 1180 ) ):
        self.File = f
        self.histos = {}
        for i in Range:            
            h = f.Get( 'h_{0}'.format( i ) )
            if not h :
                continue
            h = h.Clone()
            h.SetTitle(title)
            h.SetLineColor( color )
            h.SetLineWidth( 2 )
            h.SetLineStyle( 1 )
            self.histos[ 69200.0*i/1000 ] = h

dataPu = {}
for name,color in dsnames.items():
    dataPu[name] = DataPU( ROOT.TFile.Open(  'datapu_hadd/data_latest_{0}.root'.format( name )  ), color[0] , name )
            
class Variable:
    def __init__(self, dir , color , xsec_range = [ 69200.0*i/1000  for i in range( 840 , 1170 ) ] ):
        rree = re.compile( '(?P<filename>[^:]*):/(?P<samples>[^/]*)/(?P<variable>[^/]*)/(?P<mcname>[^/]*)/(?P<pu_algo>[^/]*)/(?P<datasetname>[^/]*)' )
        dirname_parts = rree.match ( dir.GetPath() )
        if dirname_parts:
            parts = dirname_parts.groupdict()
            self.var = parts['variable']
            self.pu_algo = parts['pu_algo']
            self.datasetname = parts['datasetname']
            self.mcname = parts['mcname']
            self.samples = parts['samples']
            self.filename = parts['filename']
        else:
            raise ValueError( dir.GetPath() + ' is not correctly formatted' )

        self.color = color
        self.data = dir.Get( '{0}_{1}'.format(self.datasetname , self.var ) )
        self.data.SetTitle( '{0};{1};'.format( self.datasetname , self.var ) )
        self.data.SetLineColor( color )
        self.data.SetLineWidth(3)
        
        self.mc2dplot = dir.Get( self.var )
        self.mc2dplot.SetTitle( ";{0};nInteractions".format( self.var ) )
        
        self.mcPlots = {}
        self.chi2Canvas = dir.Get('Chi2')
        self.chi2Canvas.Print()
        self.chi2 = self.chi2Canvas.GetListOfPrimitives().At(1)
        self.chi2.SetLineColor( color )
        self.chi2.SetMarkerColor( color )
        self.chi2.SetTitle( self.datasetname )
        #self.chi2.Print()
        self.chi2Values = {}
        for xsec in xsec_range:
            self.mcPlots[ xsec ] = dir.Get( '{0}_{1}_{2}_{3:.1f}'.format( self.var , self.pu_algo , self.datasetname , xsec ) )
            self.chi2Values[xsec] = self.chi2.Eval( xsec )
            self.mcPlots[xsec].SetTitle( '{0},xsec = {1:.1f};{2};'.format(self.datasetname, xsec , self.var ) )
            self.mcPlots[xsec].SetLineColor( color )
            self.mcPlots[xsec].SetLineWidth(2)
            
    def GetMinHisto(self):
        self.MinXSec = min( self.chi2Values , key = lambda k: self.chi2Values[k] )
        MinHisto = self.mcPlots[self.MinXSec]
        return MinHisto
    
    def GetFilledHisto(self , name , index = -1):
        h = getattr( self, name)
        if index > -1:
            h = h[index]
        h = h.Clone()
        h.SetLineStyle(10)
        h.SetFillColor( self.color )
        return h

    def MakeSlideTex(self , ret):
        ret += [r'\subsection{'+self.var+'}']
        ret += [r'\begin{frame}']
        ret += [r'\frametitle{'+self.var+'}']
        ret += [r'\begin{columns}[t]']
        ret += [r'\column{.33\textwidth}']
        ret += [r'\includegraphics[width=.98\textwidth]{figs/'+self.var+'_bestfits.pdf}\\']
        ret += [r'\includegraphics[width=.98\textwidth]{figs/'+self.var+'_correlation.pdf}']
        ret += [r'\column{.33\textwidth}']
        ret += [r'\centering']
        ret += [r'\includegraphics[width=.98\textwidth]{figs/'+self.var+'_data_normalized.pdf}\\']
        ret += [r'\includegraphics[width=.98\textwidth]{figs/'+self.var+'_data_stack.pdf}']
        ret += [r'\column{.33\textwidth}']
        ret += [r'\centering']
        ret += [r'\includegraphics[width=.98\textwidth]{figs/'+self.var+'_datapus.pdf}\\']
        ret += [r'\includegraphics[width=.98\textwidth]{figs/'+self.var+'_datapus_stack.pdf}\\']
        ret += [r'\includegraphics[width=.98\textwidth]{figs/'+self.var+'_chi2s.pdf}\\']        
        ret += [r'\end{columns}']
        ret += [r'\end{frame}']


def MakeTexHeader():
    ret = [r'\documentclass{beamer}']
    ret += [r'\begin{document}']
    ret += [r'\title{PU Studies}']
    ret += [r'\author{Hamed}']
    ret += [r'\date{\today}']

    ret += [r'\frame{\titlepage}']
    ret += [r'\frame{\frametitle{Table of contents}\tableofcontents}']
    ret += [r'\section{Details for variables}']
    return ret

def maketitlebox(title):
    ret = ROOT.TLatex()
    ret.SetNDC()
    ret.SetTextSize(0.06)
    ret.DrawLatex(0.2,0.943,title)
    ret.Draw()
    return ret

ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

f = ROOT.TFile.Open( 'out_2018_SingleNeutrinovsZeroBias.root' )
eras = {}

vars = ['fixedGridRhoFastjetAllCalo', 'fixedGridRhoFastjetCentralChargedPileUp' ,  'fixedGridRhoFastjetCentralCalo' , 'nVertices'  , 'nNeutralHadrons' ,  'nPhotons' , 'fixedGridRhoFastjetCentral' , 'fixedGridRhoFastjetAll' , 'nChargedHadrons' , 'fixedGridRhoAll' ]
buggy_vars= ['fixedGridRhoFastjetCentralNeutral', 'nEles' , 'nMus' ]
BeamerCode = MakeTexHeader()
print BeamerCode
fout = ROOT.TFile.Open('figs/fout.root' , 'recreate' )
for varname in vars+buggy_vars:
    fout.mkdir( varname ).cd()
    print(varname)
    for dsname,pars in dsnames.items() :
        print(pars[0])
        dir = f.GetDirectory( '/SingleNuZeroBias/{0}/Type1/latest/{1}'.format( varname , dsname )   )
        eras[dsname] = Variable( dir ,  pars[0] )

    c1 = ROOT.TCanvas('{0}_data_normalized'.format(varname) , '{0}_data_normalized'.format(varname) )
    c1.cd()
    h1 = eras['All'].data.DrawNormalized()
    if varname in buggy_vars:
        h1.GetYaxis().SetRangeUser( 0 , 2*h1.GetYaxis().GetXmax() )
    eras['eraA'].data.DrawNormalized('same')
    eras['eraB'].data.DrawNormalized('same')
    c1.BuildLegend(0.8 , 0.8 , 0.98 , 0.98)
    maketitlebox('Normalized Data')
    c1.SaveAs( 'figs/' + c1.GetTitle() + '.pdf' )
    c1.Write()
    
    c2 = ROOT.TCanvas('{0}_data_stack'.format(varname) , '{0}_data_stack'.format(varname))
    c2.cd()
    eras['All'].data.Draw()
    if varname in buggy_vars:
        h1 = eras['All'].data
        h1.GetYaxis().SetRangeUser( 0 , 3*h1.GetMaximum() )
        h1.Draw()
    stack = ROOT.THStack()
    stack.Add( eras['eraA'].GetFilledHisto('data') )
    stack.Add( eras['eraB'].GetFilledHisto('data') )
    stack.Draw('same')
    c2.BuildLegend(0.8 , 0.8 , 0.98 , 0.98)
    eras['All'].data.Draw('same')
    maketitlebox('Data')
    c2.SaveAs( 'figs/' +  c2.GetTitle() + '.pdf' )
    c2.Write()

    c3 = ROOT.TCanvas( '{0}_bestfits'.format( varname ) , '{0}_bestfits'.format( varname ) )
    
    h1 = eras['All'].GetMinHisto().DrawNormalized()
    if varname in buggy_vars:
        h1.GetYaxis().SetRangeUser( 0 , 2*h1.GetYaxis().GetXmax() )
    eras['eraA'].GetMinHisto().DrawNormalized('same')
    eras['eraB'].GetMinHisto().DrawNormalized('same')

    c3.BuildLegend(0.6 , 0.8 , 0.98 , 0.98)
    maketitlebox('Best fits')
    c3.SaveAs( 'figs/' +  c3.GetTitle() + '.pdf' )
    c3.Write()
    
    varType2 = Variable( f.GetDirectory( '/SingleNuZeroBias/{0}/Type2/latest/{1}'.format( varname , dsname )   ) , 0 )
    c4 = ROOT.TCanvas( "{0}_correlation".format( varname ) , "{0}_correlation".format( varname ) )
    varType2.mc2dplot.Draw("colz")
    maketitlebox('Correlation')
    c4.SaveAs( 'figs/' +  c4.GetTitle() + '.pdf' )
    c4.Write()
    
    c5 = ROOT.TCanvas( "{0}_datapus".format( varname ) , "{0}_datapus".format( varname ) )
    opt = 'L'
    for era in ['All' , 'eraA' , 'eraB']:
        dataPu[era].histos[ eras[ era ].MinXSec ].DrawNormalized(opt)
        opt = 'L same'
    c5.BuildLegend(0.6 , 0.8 , 0.98 , 0.98)
    maketitlebox('DataPU')
    c5.SaveAs('figs/' + c5.GetTitle() + '.pdf' )
    c5.Write()
    
    c6 = ROOT.TCanvas( "{0}_datapus_stack".format( varname ) , "{0}_datapus_stack".format( varname ) )
    hAll = dataPu['All'].histos[ eras[ 'All' ].MinXSec ]
    hAll.Scale( eras['All'].data.Integral()/hAll.Integral() )
    hAll.Draw()

    stack2 = ROOT.THStack()
    hEraA = dataPu['eraA'].histos[ eras[ 'eraA' ].MinXSec ]
    hEraA.Scale( eras['eraA'].data.Integral()/hEraA.Integral() )
    hEraA.SetFillColor( dsnames['eraA'][0] )
    stack2.Add( hEraA )

    hEraB = dataPu['eraB'].histos[ eras[ 'eraB' ].MinXSec ]
    hEraB.Scale( eras['eraB'].data.Integral()/hEraB.Integral() )
    hEraB.SetFillColor( dsnames['eraB'][0] )
    stack2.Add( hEraB )

    stack2.Draw('same')
    c6.BuildLegend(0.6 , 0.8 , 0.98 , 0.98)
    hAll.Draw('same')
    maketitlebox('DataPU-stack')
    c6.SaveAs('figs/' + c6.GetTitle() + '.pdf' )
    c6.Write()
    
    eras['All'].MakeSlideTex( BeamerCode )

    c7 = ROOT.TCanvas( "{0}_chi2s".format( varname ) , "{0}_chi2s".format( varname ) )
    eras['All'].chi2.Draw("AL")
    eras['eraA'].chi2.Draw("L SAME")
    eras['eraB'].chi2.Draw("L SAME")
    Min = min( [eras[a].chi2.GetMinimum() for a in eras] )
    Max = max( [eras[a].chi2.GetMinimum() for a in eras] )
    eras['All'].chi2.GetHistogram().GetYaxis().SetRangeUser( Min , Max )
    c7.BuildLegend(0.6 , 0.8 , 0.98 , 0.98)
    maketitlebox('#chi^{2}')
    c7.SaveAs( 'figs/' +  c7.GetTitle() + '.pdf' )
    c7.Write()
    
    c1.Close()
    c2.Close()
    c3.Close()
    c4.Close()
    del c1
    del c2
    del c3
    del c4

BeamerCode += [r'\input{BbB.tex}']
BeamerCode += [r'\end{document}']
with open('Slides.tex' , 'w' ) as f:    
    for l in BeamerCode:
        f.write( l + '\n' )

fout.Close()
