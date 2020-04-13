from ROOT import TDirectory, TFile, TCanvas , TH1D , TH1 , THStack, TList, gROOT, TLegend, TPad, TLine, gStyle, TTree , TObject , gDirectory, gPad, TLimit, Double, TLimitDataSource, TString, TLatex
from ROOT import RooFit,RooDataHist, RooHistPdf,RooAddPdf,RooFitResult, RooRealVar, RooArgSet, RooArgList, gSystem
from xml.etree.ElementTree import SubElement

from math import sqrt,log
import os
import sys
import Sample
from array import array
import string
from collections import OrderedDict

class Property:
	def __init__(self , name , bkg_hists , data_hist , signal_hists , sample_hists, GRE = True):
		self.Name = name
		self.Bkg = bkg_hists
		self.Data = data_hist
		self.Signal = signal_hists
		self.Samples = sample_hists
		self.greater = GRE
		self.isSoB = False
		self.isSoSqrtB = False
		self.isSoSqrtBdB2 = False
		self.isLnSoSqrtSB = False
		self.isLnSoSqrtSBdB = False
		self.SigSignificance = []

	@staticmethod
	def FromDir( dir , GRE = True ):
		name = dir.GetName()
		ret = Property( name , OrderedDict() , None , [] , [] , GRE )
        
		cats_dir = dir.GetDirectory("cats")
		for cat_ in cats_dir.GetListOfKeys() :
			cat = cat_.GetName()
			if cat.endswith("_Data"):
				gROOT.cd()
				ret.Data = cats_dir.Get( cat ).Clone()
			elif cat != "SumMC" :
				gROOT.cd()
				ret.Bkg[cat.split("_")[-1]] =  cats_dir.Get( cat ).Clone()

		sigs_dir = dir.GetDirectory("signals")
		if sigs_dir :
			for sig_ in sigs_dir.GetListOfKeys() :
				sig = sig_.GetName()
				gROOT.cd()
				ret.Signal.append( sigs_dir.Get(sig).Clone() )

		samples_dir = dir.GetDirectory("samples")
		for sam_ in samples_dir.GetListOfKeys() :
			sam = sam_.GetName()
			gROOT.cd()
			ret.Samples.append( samples_dir.Get(sam).Clone() )
            
		return ret

	@staticmethod
	def AddOFUF(h):
		UF = h.GetBinContent(0)
		UF_E = h.GetBinError(0)

		b1 = h.GetBinContent(1)
		b1_e = h.GetBinError(1)

		h.SetBinContent( 1 , UF+b1 )
		h.SetBinError( 1 , sqrt( UF_E*UF_E + b1_e*b1_e ) )

		h.SetBinContent( 0 , 0.0 )
		h.SetBinError( 0 , 0.0 )
		
		lastBin = h.GetNbinsX()
		OF = h.GetBinContent(lastBin+1)
		OF_E = h.GetBinError(lastBin+1)

		bL = h.GetBinContent(lastBin)
		bL_e = h.GetBinError(lastBin)
		
		h.SetBinContent( lastBin , OF+bL )
		h.SetBinError( lastBin , sqrt( OF_E*OF_E + bL_e*bL_e ) )
		
		h.SetBinContent( lastBin+1 , 0.0 )
		h.SetBinError( lastBin+1 , 0.0 )
		
	def AddOF_UF_Bins(self):
		Property.AddOFUF( self.Data )
		for s in self.Signal:
			Property.AddOFUF(s)
		for s in self.Bkg:
			Property.AddOFUF(self.Bkg[s])
		for s in self.Samples:
			Property.AddOFUF(s)
	
			
	def GetBkgFromCR(self, CRProp , Bkgs , replacement , yieldsMethod=1) :
		""" 
		extract the shape of bkg from CRProp using data minus all Bkgs
		for the normalization in SR (which is the current property) several methods are foreseen :
		yieldsMethod = 1 : sum of the integral of Bkgs in CR (so taken from the simulation and cross section of backgrounds, trusted in signal region)
		yieldsMethod = 2 : data minus other MC's except Bkgs
		yieldsMethod = 3 : template fit

		replacement is a list with this format : [ NewName , NewColor ]
		"""

		notInBkg = [item for item in self.Bkg if item not in Bkgs]
		template = CRProp.SubtractDataMC( notInBkg , self.Name )
		if template.Integral() == 0:
			return -1
		nMCBkgsSR = 0
		nDataMinusBkgsSR = self.Data.Integral()
		for bkg in Bkgs:
			nMCBkgsSR += self.Bkg.pop(bkg).Integral()
		for bkg in self.Bkg:
			nDataMinusBkgsSR -= self.Bkg[bkg].Integral()


		nNormalization = 0
		if yieldsMethod == 1:
			nNormalization = nMCBkgsSR
		elif yieldsMethod == 2:
			nNormalization = nDataMinusBkgsSR
		elif yieldsMethod == 3:
			nFit = 1.0
			var = RooRealVar( self.Name, self.Name , self.Data.GetXaxis().GetXmin() , self.Data.GetXaxis().GetXmax() )
			templatehist = RooDataHist( "%s_bkg_templateHist" %(self.Name) , self.Name , RooArgList(var) , template)
			templatepdf = RooHistPdf("%s_bkg_templatePDF" %(self.Name), self.Name , RooArgSet(var) ,templatehist);

			SumNonBkg = self.Data.Clone( "sum_%s_%s_th1" % (self.Name , "_".join(notInBkg) ) )
			SumNonBkg.Reset()
			for bkg in notInBkg:
				SumNonBkg.Add( self.Bkg[bkg] )
			SumNonBkgHist = RooDataHist( "sum_%s_%s_Hist" % (self.Name , "_".join(notInBkg) ),
					                     self.Name , RooArgList(var) , SumNonBkg )
			SumNonBkgpdf = RooHistPdf( "sum_%s_%s_PDF" % (self.Name , "_".join(notInBkg) ),
					                   self.Name , RooArgSet(var) , SumNonBkgHist )

			DataHist = RooDataHist( "data_%s_Hist" % (self.Name) ,
					                self.Name , RooArgList(var) , self.Data )

			
			nBkgs = None
			if nDataMinusBkgsSR > 0 :
				nBkgs = RooRealVar("nBkgs","NBkgs", nDataMinusBkgsSR , 0.5*nDataMinusBkgsSR , 2*nDataMinusBkgsSR)
			elif nDataMinusBkgsSR < 0:
				nBkgs = RooRealVar("nBkgs","NBkgs", nDataMinusBkgsSR , 2*nDataMinusBkgsSR , -2*nDataMinusBkgsSR)
			else:
				nBkgs = RooRealVar("nBkgs","NBkgs", nDataMinusBkgsSR , -10 , 10 )
			nFixed = RooRealVar("nFixed","NFIXED", SumNonBkg.Integral() , SumNonBkg.Integral() , SumNonBkg.Integral() )
			model = RooAddPdf("model","model",RooArgList(SumNonBkgpdf,templatepdf),RooArgList(nFixed , nBkgs ) )
			res = model.fitTo( DataHist , RooFit.Extended( True ) , RooFit.Save(True) , RooFit.SumW2Error(True) )
			nNormalization = nBkgs.getVal()

		template.Scale( nNormalization/template.Integral() )
		template.SetLineWidth(2)
		template.SetLineColor(1)
		template.SetFillColor( replacement[1] )
		template.SetFillStyle( 1001 )
		self.Bkg[ replacement[0] ] = template

		return nNormalization
	
	def Rebin(self , newbins):
		bins = sorted(newbins)
		runArray = array('d',bins)
		self.Data = self.Data.Rebin( len(newbins)-1 , self.Data.GetName() + "_rebined" , runArray )
		if self.Signal:
			for i in range(0 , len(self.Signal) ):
				self.Signal[i] = self.Signal[i].Rebin( len(newbins)-1 , self.Signal[i].GetName() + "_rebined" , runArray )
		for bkg in self.Bkg:
			self.Bkg[bkg] = self.Bkg[bkg].Rebin( len(newbins)-1 , self.Bkg[bkg].GetName() + "_rebined" , runArray )
		
	@staticmethod
	def addLabels(histo , labels):
		if not histo:
			return
		for i in range(1, histo.GetNbinsX()+1 ):
			if not i > len(labels) :
				histo.GetXaxis().SetBinLabel( i , labels[i-1] )

	def SetLabels(self , labels):
		Property.addLabels( self.Data , labels )
		for s in self.Signal:
			Property.addLabels( s , labels )
		for bkg in self.Bkg:
			Property.addLabels( self.Bkg[bkg] , labels )
		for smpl in self.Samples:
			Property.addLabels( smpl , labels )
		
	def Clone(self , newname , allsamples = False):
		ret = Property( newname , {} , None , None , [] )
		ret.Data = self.Data.Clone( string.replace( self.Data.GetName() , self.Name , newname ) )
		if self.Signal :
			ret.Signal = []
			for i in range(0 , len(self.Signal) ):
				ret.Signal.append( self.Signal[i].Clone( string.replace( self.Signal[i].GetName() , self.Name , newname ) ) )
		for bkg in self.Bkg:
			ret.Bkg[bkg] = self.Bkg[bkg].Clone( string.replace( self.Bkg[bkg].GetName() , self.Name , newname ) )
		if allsamples:
			ret.Samples = [ h.Clone( string.replace( h.GetName() , self.Name , newname ) ) for h in self.Samples ]

		return ret
		
	def SubtractDataMC( self , tosubtract , appendix = "" ):
		tokeep = [item for item in self.Bkg if item not in tosubtract]
		ret = self.Data.Clone( "%s_%s_template_%s" % ( self.Name , "_".join(tokeep) , appendix ) )
		for bkg in tosubtract:
			ret.Add( self.Bkg[bkg] , -1 )
		return ret
		
	def GetStack(self, normtodata = False):
		if not hasattr(self , "Stack"):
			stackname = "%s_stack" % (self.Name)
			scale = 1.0
			if normtodata:
				totalmc = 0.
				for st in self.Bkg:
					totalmc += self.Bkg[st].Integral()
				if totalmc > 0.000001 :
					scale = self.Data.Integral()/totalmc
				else :
					print "\t%s was not normalized to data as the mc yield is %.2f" % (self.Name , totalmc)
			#print "in getStack, normtodata = %s and scale is %f" % (str(normtodata) , scale)
			self.Stack = THStack( stackname , self.Name ) 
			for st in self.Bkg:
				if normtodata:
					self.Bkg[st].Scale( scale )
				self.Stack.Add( self.Bkg[st] )

		return self.Stack

	def GetSignalCanvas(self):
		canvasname = "%s_signal_canvas" % (self.Name)
		if not hasattr(self , "SignalCanvas" ):
			self.SignalCanvas = TCanvas(canvasname)

			if self.Signal:
				for s in self.Signal:
					s.DrawNormalized("E SAME HIST")
				self.GetSLegend().Draw()
		return self.SignalCanvas

                
	def GetCanvas(self, padid , padOrCanvas=0 , W=1050 , H=750 , appendix=''):
		canvasname = "%s_canvas%s" % (self.Name , appendix)
		pad1name = "%s_pad1%s" % (self.Name , appendix)
		pad2name = "%s_pad2%s" % (self.Name , appendix)
                
		#print( 'start' ,  canvasname , appendix , W, H , hasattr(self , "Canvas{0}".format(appendix) )
		if not hasattr(self , canvasname):
			if padOrCanvas == 0:
				Canvas = TCanvas( canvasname , canvasname , W , H)
                                setattr( self , canvasname , Canvas )
			else:
				Canvas = gPad
		        Canvas.cd()
			Pad1 =  TPad(pad1name ,pad1name,0,0.25,1,1)
			Pad1.SetBottomMargin(0.1)
			Pad1.Draw()

			Canvas.cd()

			Pad2 = TPad( pad2name,pad2name,0,0,1,0.24)
			Pad2.SetTopMargin(0.1)
			Pad2.SetBottomMargin(0.1)
			Pad2.Draw()

                        setattr( self , pad1name , Pad1 )
                        setattr( self , pad2name , Pad2 )
                        #print( 'test' , canvasname , pad1name , pad2name)

                #print( canvasname , pad1name , pad2name)
		if padid == 0:
			getattr(self, canvasname).cd()
                        return getattr(self, canvasname)
		elif padid == 1:
			getattr(self, pad1name).cd()
                        return getattr(self, pad1name)
		if padid == 2:
			getattr(self, pad2name).cd()
                        return getattr(self, pad2name)
                else:
                        return None

	def GetLegend(self):
		legendname = "%s_legend" % (self.Name)
		if not hasattr(self , "Legend"):
			self.Legend = TLegend(0.7,0.6,0.9,0.9,"","brNDC") 
			self.Legend.SetName( legendname )
			self.Legend.AddEntry( self.Data , "Data" , "lp" )
			for st in reversed( self.Bkg.keys() ):
				self.Legend.AddEntry( self.Bkg[st] , self.Bkg[st].GetTitle() , "f" )
				
		return self.Legend

	def GetSLegend(self):
		legendname = "%s_Slegend" % (self.Name)
		if not hasattr(self , "SLegend"):
			self.SLegend = TLegend(0.6,0.6,0.7,0.9,"","brNDC") 
			self.SLegend.SetName( legendname )
			for st in self.Signal:
				self.SLegend.AddEntry( st , st.GetTitle() , "l" )
			
		return self.SLegend
	

	def GetRatioPlot(self):
		rationame = "%s_Ratio_%d" % (self.Name , self.MarkerStyle)
		if not hasattr(self, "Ratio_{0}".format(self.MarkerStyle)):
			self.Ratio = self.Data.Clone( rationame )
			self.Ratio.SetStats(0)
			self.Ratio.Divide( self.GetStack().GetStack().Last() )
			for i in range(1 , self.Data.GetNbinsX()+1 ):
				self.Ratio.GetXaxis().SetBinLabel(i , "")
			self.Ratio.SetMarkerStyle(self.MarkerStyle)
                        #self.Ratio.SetMarkerSize( self.MarkerSize )
			self.Ratio.GetYaxis().SetRangeUser(0,2)
			self.Ratio.GetXaxis().SetLabelSize( 0.)
			self.Ratio.GetYaxis().SetTitle("Data / MC")
			self.Ratio.GetXaxis().SetTitleSize(0.2) 
			self.Ratio.GetXaxis().SetTitleOffset(0.25)
			self.Ratio.GetYaxis().SetLabelSize(0.1)
			self.Ratio.GetXaxis().SetTickLength(0.09)
			self.Ratio.GetYaxis().SetTitleSize(0.18)
			self.Ratio.GetYaxis().SetNdivisions(509)
			self.Ratio.GetYaxis().SetTitleOffset(0.25)
			self.Ratio.SetFillStyle(3001)
                        setattr( self , "Ratio_{0}".format(self.MarkerStyle) , self.Ratio )
			
		return self.Ratio

	def GetRatioUnc(self):
		rationame = "%s_RatioUncert" % (self.Name)
		if not hasattr(self, "RatioUncert"):
			mc = self.GetStack().GetStack().Last()
			self.RatioUncert = mc.Clone( rationame )
			self.RatioUncert.SetStats(0)
			self.RatioUncert.Divide(mc)
			for i in range(1 , self.Data.GetNbinsX()+1 ):
				self.RatioUncert.GetXaxis().SetBinLabel(i , "")
			self.RatioUncert.GetYaxis().SetRangeUser(0,2)
			self.RatioUncert.GetYaxis().SetTitle("Data / MC")
			self.RatioUncert.GetXaxis().SetTitleSize(0.2) 
			self.RatioUncert.GetXaxis().SetTitleOffset(0.25)
			self.RatioUncert.GetYaxis().SetLabelSize(0.1)
			self.RatioUncert.GetXaxis().SetTickLength(0.09)
                        self.RatioUncert.GetXaxis().SetTitle("")
			self.RatioUncert.GetYaxis().SetTitleSize(0.18)
			self.RatioUncert.GetYaxis().SetNdivisions(509)
			self.RatioUncert.GetYaxis().SetTitleOffset(0.25)
			self.RatioUncert.SetFillStyle(3001)
			self.RatioUncert.SetFillColor(1)
			
		return self.RatioUncert


	def GetLineOne(self):
		linename = "%s_lineone" % (self.Name)
		if not hasattr(self, "LineOne"):
			self.LineOne = TLine(self.GetRatioPlot().GetXaxis().GetXmin(), 1.00, self.GetRatioPlot().GetXaxis().GetXmax(), 1.00)
			self.LineOne.SetLineWidth(2)
			self.LineOne.SetLineStyle(7)

		return self.LineOne

        def GetTitleBox(self):
                title = self.Samples[0].GetTitle()
                if not hasattr(self , "TitleBox"):
                        self.TitleBox = TLatex()
                        self.TitleBox.SetNDC()
                        self.TitleBox.SetTextSize(0.06)
                        self.TitleBox.DrawLatex(0.6,0.943,title)
                return self.TitleBox

	def Draw(self, normalizetodata = False , padOrCanvas = 0 , W=1050 , H=750 , canvas_appendix='' ):
                if W<500 :
                        self.MarkerStyle = 7
                else:
                        self.MarkerStyle = 20
		gStyle.SetOptTitle(0)
		self.GetCanvas(1, padOrCanvas , W=W , H=H , appendix=canvas_appendix)
                self.Data.SetMarkerStyle(self.MarkerStyle)
		#self.Data.Draw("E")
		self.GetStack(normalizetodata).Draw('HIST') #"HIST SAME")
		self.Data.Draw("E SAME P")
		if self.Signal:
			for s in self.Signal:
				s.Draw("E SAME HIST")
			self.GetSLegend().Draw()
		self.GetLegend().Draw()
		self.GetTitleBox().Draw()
		self.GetCanvas(2 , padOrCanvas,  appendix=canvas_appendix)
		self.GetRatioUnc().Draw("E2")
		self.GetRatioPlot().Draw("ep same")
		self.GetLineOne().Draw()

	def Write(self , propdir , normtodata , mkdir=False , png_filename = None , xml_node = None  ):
		if mkdir:
                        if propdir.Get( self.Name ):
                                for i in range(10):
                                        name = "{0}_{1}".format( self.Name , i )
                                        if propdir.Get(name) :
                                                continue
                                        propdir = propdir.mkdir( "{0}_{1}".format( self.Name , i ) )
                                        break
                        else:
			        propdir = propdir.mkdir( self.Name )
		propdir.cd()
                print( propdir.GetPath() )
		catdir = propdir.mkdir( "cats" )
		catdir.cd()
		if hasattr( self , "Data" ) and self.Data :
			self.Data.Write()
		for bkg in self.Bkg :
			self.Bkg[bkg].Write()
		if len(self.Bkg) > 0 :
			self.GetStack(normtodata).GetStack().Last().Write("SumMC")

		if self.Signal :
			sigdir = propdir.mkdir( "signals" )
			sigdir.cd()
			for i in range(0 , len(self.Signal) ):
				self.Signal[i].Write()
		
		sampledir = propdir.mkdir( "samples" )
		sampledir.cd()
		for ss in self.Samples:
			ss.Write()

		propdir.cd()
		if(self.Data is not None):
                        self.Data.GetYaxis().SetRangeUser( 0.0 , 2*max(self.Data.GetMaximum(), self.GetStack().GetStack().Last().GetMaximum()) )
			self.Draw(normtodata , canvas_appendix='main')
                c = self.GetCanvas(0 , appendix='main')
                c.Write()
                if(self.Data is not None):
			self.Draw(normtodata , W=400 , H=300 , canvas_appendix='thumbnail')
                cth = self.GetCanvas(0 , appendix='thumbnail')
                cth.Write()

                self.GetCanvas(padid=1 , appendix='main').SetLogy()
                self.GetCanvas(padid=1 , appendix='thumbnail').SetLogy()
                if self.Data:
                        self.Data.SetMarkerStyle(20)
                        self.Data.GetYaxis().SetRangeUser( 0.001 , 500*self.Data.GetMaximum() )

                c.Write( c.GetName() + "_log" )
                if self.Data:
                        self.Data.SetMarkerStyle(7)
                cth.Write( cth.GetName() + "_log")
                
                if png_filename and self.Data:
                        c.SaveAs( png_filename )
                        c.SaveAs( png_filename.replace( '.png' , '.pdf' ) )
                        
                        cth.SaveAs( png_filename.replace( '.png' , '_thumb.png' ) )
                        
                        gSystem.ProcessEvents()
                        #c.SaveAs( png_filename.replace( '.png' , '_log.png') )
                        c.SaveAs( png_filename.replace( '.png' , '_log.pdf') )
                        c.SaveAs( png_filename.replace( '.png' , '_log.png') )

                        cth.SaveAs( png_filename.replace( '.png' , '_thumb_log.png' ) )
                        
                        if xml_node is not None:
                                var_el = SubElement(xml_node, "variable")
                                SubElement( var_el , "name" ).text = self.Name
                                SubElement( var_el , "image" ).text = png_filename.split( '/' )[-1]
                                SubElement( var_el , "thumbnail" ).text = png_filename.split( '/' )[-1].replace( '.png' , '_thumb.png' )
                                SubElement( var_el , "HasLog").text = str(True)
                                SubElement( var_el , "logImage").text = png_filename.split( '/' )[-1].replace( '.png' , '_log.png' )
                                SubElement( var_el , "logThumbnail").text = png_filename.split( '/' )[-1].replace( '.png' , '_thumb_log.png' )
                                other_formats = SubElement( var_el , "OtherFormats" )
                                of_el = SubElement( other_formats , "format" )
                                SubElement( of_el , "ext" ).text = 'pdf'
                                SubElement( of_el , "file" ).text = png_filename.split( '/' )[-1].replace( '.png' , '.pdf' )
                                SubElement( of_el , "logImage" ).text = png_filename.split( '/' )[-1].replace( '.png' , '_log.pdf' )
                        cth.Close()
                c.Close()
                
		if(hasattr(self, "SignalROC")):
			roc = propdir.mkdir( "ROCs" )
			roc.cd()
			self.DataROC.Write()
			self.BkgROC.Write()
			for iSig in range(0, len(self.SignalROC)):
				self.SignalROC[iSig].Write()
		propdir.cd()
		
		if(hasattr(self, "SigSignificance")):	
			sigdir = propdir.mkdir( "Significances" )
			sigdir.cd()
			if self.isSoB:
				sob = sigdir.mkdir("SoB")
				sigdir.cd()
			if self.isSoSqrtB:
				sosqrtb = sigdir.mkdir("SoSqrtB")
				sigdir.cd()
			if self.isSoSqrtBdB2:
				sosqrtbdb2 = sigdir.mkdir("SoSqrtBdB2")
				sigdir.cd()
			if self.isLnSoSqrtSB:
				lnsosqrtb = sigdir.mkdir("LnSoSqrtSB")
				sigdir.cd()
			if self.isLnSoSqrtSBdB:
				lnsosqrtbdb = sigdir.mkdir("LnSoSqrtSBdB")
				sigdir.cd()				

			for iSig in range(0, len(self.SigSignificance)):
				if TString(self.SigSignificance[iSig].GetName()).Contains("_SoB"):
					sob.cd()
				elif TString(self.SigSignificance[iSig].GetName()).Contains("_LnSoSqrtSBdB"):
					lnsosqrtbdb.cd()
				elif TString(self.SigSignificance[iSig].GetName()).Contains("_LnSoSqrtSB"):
					lnsosqrtb.cd()
				elif TString(self.SigSignificance[iSig].GetName()).Contains("_SoSqrtBdB2"):
					sosqrtbdb2.cd()
				elif TString(self.SigSignificance[iSig].GetName()).Contains("_SoSqrtB"):
					sosqrtb.cd()
				self.SigSignificance[iSig].Write()
				sigdir.cd()
		propdir.cd()
		
		if(hasattr(self, "ExpLimits")):		
			expdir = propdir.mkdir( "ExpLimits" )
			expdir.cd()
			for iSig in range(0, len(self.ExpLimits)):
				self.ExpLimits[iSig].Write()
		propdir.cd()
	        #return self.GetCanvas(0)

	def ROCMaker(self, inputHist):
		tmp = inputHist.Clone("ROC_%s" %inputHist.GetName())
		tmp.Sumw2()
		for iBin in range(0, inputHist.GetXaxis().GetNbins()):
			n = 0
			nError = Double(-1.)
			if(self.greater):
				n = inputHist.IntegralAndError(iBin,-1,nError)
			else:
				n = inputHist.IntegralAndError(0, iBin, nError)
			tmp.SetBinContent(iBin, n)
			tmp.SetBinError(iBin, nError)
		return tmp

	def SetPropertyROCs(self):
		self.SignalROC = []
		for iSig in range(0, len(self.Signal)):
			self.SignalROC.append(self.ROCMaker(self.Signal[iSig]))
			self.BkgROC = self.ROCMaker(self.GetStack().GetStack().Last())
			self.DataROC = self.ROCMaker(self.Data)


	def Significance(self, signal, bkg, method=1):
		signame = "SoB"
		if(method == 2):
			signame = "SoSqrtB"
		elif(method == 3):
			signame = "SoSqrtBdB2"
		elif(method == 4):
			signame = "LnSoSqrtSB"
		elif(method == 5):
			signame = "LnSoSqrtSBdB"			
		elif(method > 5):
			print "Significance method not defined! Null histogram is returned!!!"
			return
		significance = signal.Clone("%s_%s" %(signal.GetName(),signame))
		significance.Sumw2(False)
		for iBin in range(0, signal.GetXaxis().GetNbins()):
			u = 0
			if(bkg.GetBinContent(iBin) == 0):
				u = -1.
				continue
			if(method == 1):
				u = signal.GetBinContent(iBin) / bkg.GetBinContent(iBin)
			elif(method == 2):
				u = signal.GetBinContent(iBin) / sqrt(bkg.GetBinContent(iBin))
			elif(method == 3):
				u = signal.GetBinContent(iBin) / sqrt(bkg.GetBinContent(iBin) + (bkg.GetBinError(iBin)*bkg.GetBinError(iBin)))
			elif(method == 4):
				u = sqrt(2)*sqrt((signal.GetBinContent(iBin)+bkg.GetBinContent(iBin))*log(1+(signal.GetBinContent(iBin)/bkg.GetBinContent(iBin))) - signal.GetBinContent(iBin))
			elif (method == 5):
				s =  signal.GetBinContent(iBin) 
				b = bkg.GetBinContent(iBin)
				sigb =  bkg.GetBinError(iBin)
				ln1 = ((s+b)*(b+(sigb*sigb)))/((b*b)+((s+b)*sigb*sigb))
				ln2 = 1+ (sigb*sigb*s)/(b*(b+(sigb*sigb)))
				Sum = ((s+b)*ln1) - ((b*b/(sigb*sigb))*ln2)
				if(Sum >= 0):
					u = sqrt(2*Sum)
				u = -1
				
			significance.SetBinContent(iBin, u)
		return significance

	def SetSignificances(self,method = 1):
		if not (hasattr(self,"BkgROC") and hasattr(self,"DataROC") and hasattr(self,"SignalROC")):
			self.SetPropertyROCs()
		if method == 1: self.isSoB = True
		elif method == 2: self.isSoSqrtB = True
		elif method == 3: self.isSoSqrtBdB2 = True
		elif method == 4: self.isLnSoSqrtSB = True
		elif method == 5: self.isLnSoSqrtSBdB = True		
		for iSig in range(0, len(self.Signal)):
			self.SigSignificance.append(self.Significance(self.SignalROC[iSig], self.BkgROC, method))
			
	def ExpectedLimits(self, signal, bkg_, data_):
   		sig = TH1D(("sig_%s" %signal.GetName()),"sig",1,0,1)
   		bkg = TH1D(("bkg_%s" %signal.GetName()),"bkg",1,0,1)
   		data = TH1D(("data_%s" %signal.GetName()),"data",1,0,1)
   		limits = signal.Clone("%s_ExpLimit" %signal.GetName())
   		limits.Sumw2(False)
		for iBin in range(0, signal.GetXaxis().GetNbins()):
			sig.SetBinContent(1, signal.GetBinContent(iBin))
			sig.SetBinError(1, signal.GetBinError(iBin))
			bkg.SetBinContent(1, bkg_.GetBinContent(iBin))
			bkg.SetBinError(1, bkg_.GetBinError(iBin))
			data.SetBinContent(1, data_.GetBinContent(iBin))
			data.SetBinError(1, data_.GetBinError(iBin))
			mydatasource = TLimitDataSource(sig,bkg,data)
			myconfidence = TLimit.ComputeLimit(mydatasource,50000);
			limits.SetBinContent(iBin, myconfidence.GetExpectedCLs_b(0))
		del sig
		del bkg
		del data
		return limits
			
	def SetExpectedLimits(self):
		if not (hasattr(self,"BkgROC") and hasattr(self,"DataROC") and hasattr(self,"SignalROC")):
			self.SetPropertyROCs()
		self.ExpLimits = []
		for iSig in range(0, len(self.Signal)):
			self.ExpLimits.append(self.ExpectedLimits(self.SignalROC[iSig], self.BkgROC, self.BkgROC))

