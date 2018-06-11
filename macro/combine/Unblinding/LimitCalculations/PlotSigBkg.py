#!/usr/bin/env python
import re
import math
import ROOT
import sys
import os
import shutil
from os import listdir
from os.path import isfile, join, splitext, basename
from subprocess import call, Popen, PIPE

inputDir = "nBins200"
workingdir = "BkgPlusSignal_" + inputDir
#while os.path.isdir( "./%s" % (workingdir) ):
#    workingdir += "_"
if not os.path.isdir( "./%s" % (workingdir) ):
    os.mkdir( workingdir )

AllIndices = {}
plots = {}
save_diag_outputs = False
toys_for_diag = True
nBinsToPlot = 50

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
for mass in [40] : # , 30 , 50 , 55 , 60] :
    fOutName = "./higgsCombineTest.MultiDimFit.mH%d.root" % (mass)
    if not isfile( "%s/%s" % (workingdir , fOutName) ):
        command = ["combine" ,  "-M" ,  "MultiDimFit" ,  "--saveWorkspace"  , "--X-rtd" , "ADDNLL_RECURSIVE=0" , "--cminDefaultMinimizerStrategy" , "0" , "-m" , "%d" % (mass) ,  inputDir+"/CombinedCard.root"]
        print " ".join( command )
        call( command )
        shutil.move( fOutName , "%s/%s" % (workingdir , fOutName) )
        shutil.move( "combine_logger.out" , "%s/combine_logger_%d.out" % (workingdir , mass) )


    

    if not isfile( "%s/BestFitCombinedCard_M%d.root" % (workingdir , mass ) ):
        fMultiDimFit = ROOT.TFile.Open( "%s/%s" % (workingdir , fOutName) )
        wMultiDimFit = fMultiDimFit.Get("w")
        wMultiDimFit.loadSnapshot("MultiDimFit")
        tt_index = wMultiDimFit.cat("pdfIndex_TT").getIndex()
        tl_index = wMultiDimFit.cat("pdfIndex_TLexc").getIndex()
        tm_index = wMultiDimFit.cat("pdfIndex_TMexc").getIndex()
        AllIndices[ mass ] = ( tt_index , tm_index , tl_index )

        fInWs = ROOT.TFile.Open( inputDir + "/UnblindedWS.root" )
        ws = fInWs.Get("HMuMubbWS")

        amumass = ws.var("aMuMass")
        amumass.setBins( nBinsToPlot )

        bestFitFunctions = {}

        for name , chid , index in [("TT", 3 , tt_index) , ("TMexc" , 2 , tm_index) , ("TLexc" , 1 , tl_index) ] :

            plot = amumass.frame()
            ws.data("Dataset_%s" % name ).plotOn( plot )

            print name , index
            #bkg = ws.pdf("BkgShape_%s" % name)
            bkg = wMultiDimFit.pdf( "shapeBkg_bkg_ch%d" %  chid )
            pdf_bestfit = bkg.getPdf( index )
            pdf_bestfit.Print()
            bestFitFunctions[ name ] = pdf_bestfit.GetName()
            #bkg_norm = ws.var("BkgShape_%s_norm" % name)
            bkg_norm = wMultiDimFit.var("shapeBkg_bkg_ch%d__norm" % chid )
            bestfit_norm = bkg_norm.Clone( pdf_bestfit.GetName() + "_norm" )
            getattr( ws , "import")( bestfit_norm )
            pdf_bestfit.plotOn( plot )

            c = ROOT.TCanvas( name )
            plot.Draw()
            plots[ name ] = (c , plot )

        fOutWs = ROOT.TFile.Open( "%s/UnblindedWS_M%d.root" % (workingdir , mass ) , "recreate" )
        fOutWs.cd()
        ws.Write()
        for name in plots :
            plots[name][0].Write()
        fOutWs.Close()

        fMultiDimFit.Close()
        fInWs.Close()

        with open("CombinedCard_BESTFit.txt", "rt") as fin:
            with open( "%s/BestFitCombinedCard_M%d.txt" % (workingdir , mass ) , "wt") as fout:
                for line in fin:
                    for tag in ["TT" , "TLexc" , "TMexc"] :
                        line = line.replace( "BESTFit%s" % tag   , bestFitFunctions[ tag ] )
                    fout.write( line )

        os.symlink( "%s/UnblindedWS_M%d.root" % (workingdir , mass ) , "UnblindedWS.root" )
        command = [ "text2workspace.py" , "%s/BestFitCombinedCard_M%d.txt" % (workingdir , mass ) , "-m" , "%d"%mass , "-o" , "%s/BestFitCombinedCard_M%d.root" % (workingdir , mass ) ]
        print " ".join( command )
        call( command )
        os.remove( "UnblindedWS.root" )

    if len(sys.argv) > 1 and sys.argv[1] == "diag" :
        os.chdir( workingdir )
        command = [ "combine" , "--X-rtd" , "ADDNLL_RECURSIVE=0" , "--cminDefaultMinimizerStrategy" , "0" , '-M' , 'FitDiagnostics' , '--saveNormalizations' , '--saveShapes' , '--saveWithUncertaintie' , '-m' , '%d'%mass , "%s/BestFitCombinedCard_M%d.root" % ('.' , mass )  ]
        if toys_for_diag:
            fMultiDimFit = ROOT.TFile.Open( "%s" % (fOutName) )
            limitTree = fMultiDimFit.Get("limit")
            for limit in limitTree:
                rValue = limit.r
            print "signal with r=%.4f is injected to make toys" % rValue
            command.extend( ["-t" , "-1" , "--expectSignal" , "%.4f" % rValue , "--saveToys"] )
        print " ".join( command )
        p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        shutil.move( "fitDiagnostics.root" , "fitDiagnostics_mass%d.root" % mass )
        shutil.move( "combine_logger.out" , "combine_logger_diag_mass%d.out" % mass )

        if save_diag_outputs :
            foutput = open( "combine_logger_diag_mass%d.stdout" % mass  , "wt")
            foutput_csv = open( "combine_logger_diag_mass%d.csv" % mass  , "wt")

            format_1 = r"^ server values: x=aMuMass=(\d+\.\d+), coefList=\((.*)\)"
            format_2 = r"(.*) = ([-+]?\d+\.\d+) \+\/\- ([-+]?\d+\.\d+)"
            for line in output.split( "\n" ):
                if not "WARNING:Plotting" in line :
                    foutput.write( line + "\n" )
                    if "server values" in line :
                        reg = re.match( format_1 , line , re.M|re.I)
                        if reg :
                            xvalue = reg.group(1)
                            #print reg.group(1) , reg.group(2) , reg.group(2).split(",")
                            csv_line = xvalue
                            for param in reg.group(2).split( "," ) :
                                #print param
                                par = re.match( format_2 , param , re.M|re.I)
                                if par :
                                    par_name = par.group(1)
                                    par_value = par.group(2)
                                    par_err = par.group(3)
                                    csv_line += ",%s,%s,%s" % (par_name , par_value , par_err )
                                else :
                                    csv_line += "," + line
                        else :
                            csv_line = line
                        foutput_csv.write( csv_line + "\n" )

            foutput.close()
            foutput_csv.close()

        ferr = open(  "combine_logger_diag_mass%d.stderr" % mass , "wt" )
        ferr.write( err )
        ferr.close()

        os.chdir( "../")


    if sys.argv[1] == "plot" :
        fFitDiag = ROOT.TFile.Open( "%s/fitDiagnostics_mass%d.root" % (workingdir , mass ) )
        fitresults_ = fFitDiag.Get( "fit_s" )
        fitresults_consts = fitresults_.constPars()
        fitresults_floats = fitresults_.floatParsFinal()
        fitresults_norms = fFitDiag.Get( "norm_fit_s" )


        fShapes = ROOT.TFile.Open( "%s/BestFitCombinedCard_M%d.root" % (workingdir , mass ) )
        ws_shapes = fShapes.Get( "w")
        data_obs = ws_shapes.data("data_obs")

        #if toys_for_diag :
        #    fToys = ROOT.TFile.Open( "%s/higgsCombineTest.FitDiagnostics.mH%d.123456.root" % (workingdir , mass ) )
        #    data_obs = fToys.Get("toys/toy_asimov")
        Systematics = {"symm":("lumi","signalTHunc") , "asymm":("JES","JER","MET","PDF","btag_CFERR1","btag_CFERR2","btag_HF","btag_HFSTAT1","btag_HFSTAT2","btag_JES","btag_lf","muonHLT","muonID","muonIso","pileup")}

        aMuMass = ws_shapes.arg("aMuMass")
        aMuMass.setBins( nBinsToPlot )
        
        fOutPlots = ROOT.TFile.Open("%s/plots_mass%d.root" % (workingdir , mass ) , "recreate" )
        aux_objects = []
        allpdfs = ROOT.RooArgList()
        allnorms = ROOT.RooArgList()
        
        hBkgPlusSignal = None
        hData = None
        for name , chid, nbins  in [("TT", 3 , 20 ) , ("TMexc" , 2 , 40 ) , ("TLexc" , 1 , 50 ) ] :
            shapeBkg = ws_shapes.pdf( "shapeBkg_bkg_ch%d" % chid ) 
            shapeSig = ws_shapes.pdf( "shapeSig_signal_ch%d" % chid )

            normBkg = ws_shapes.var( "shapeBkg_bkg_ch%d__norm" % chid ) 
            normSig = ws_shapes.function( "shapeSig_signal_ch%d__norm" % chid )
            
            data = data_obs.reduce( ROOT.RooFit.Cut( "CMS_channel==%d" % (chid-1) ) ) # , ROOT.RooFit.SelectVars( ROOT.RooArgSet( aMuMass ) ) )
        
            bkgParams = shapeBkg.getParameters( data )
            itr_params = bkgParams.fwdIterator()
            #bkgParams.Print()
            #fitresults.Print()
            for i_param in range(0 , bkgParams.getSize() ) :
                param = itr_params.next()
                if param.GetName() == "aMuMass" :
                    continue
                
                post_fit = fitresults_floats.find( param.GetName() )
                if not post_fit :
                    post_fit = fitresults_consts.find( param.GetName() )
                post_fit.Print()
                param.setVal( post_fit.getValV() )
                param.setError( post_fit.getError() )

            sigParams = shapeSig.getParameters( data )
            itr_params = sigParams.fwdIterator()
            for i_param in range(0 , sigParams.getSize() ) :
                param = itr_params.next()
                if param.GetName() == "aMuMass" :
                    continue

                post_fit = fitresults_floats.find( param.GetName() )
                if not post_fit :
                    post_fit = fitresults_consts.find( param.GetName() )
                #param.Print()
                post_fit.Print()
                param.setVal( post_fit.getValV() )
                param.setError( post_fit.getError() )

            normbkg_postfit = fitresults_norms["ch%d/bkg" % chid]
            normsig_postfit = fitresults_norms["ch%d/signal" % chid]
            
            #normsig_postfit = ROOT.ProcessNormalization( "normsig_ch%d" % chid , "normsig_ch%d" % chid , normsig_postfit_ )
            
            normBkg.setVal( normbkg_postfit.getValV() )
            normBkg.setError( normbkg_postfit.getError() )

            #normSig_ = ROOT.RooRealVar( "signal_norm_%s" % name , "signal_norm_%s" % name , normsig_postfit.getValV() ,  normsig_postfit.getError() )

            pdfs = ROOT.RooArgList( shapeBkg , shapeSig )
            norms = ROOT.RooArgList( normbkg_postfit , normsig_postfit )
            allpdfs.add( shapeBkg )
            allpdfs.add( shapeSig )
            allnorms.add( normbkg_postfit )
            allnorms.add( normsig_postfit )

            signal_plus_bkg = ROOT.RooAddPdf( "signal_plus_bkg_%s" % name , "Signal + Background in channel %s" % name , pdfs , norms )

            fOutPlots.cd()

            aMuMass.setBins( nbins )
            frame = aMuMass.frame()
            data.plotOn( frame )
            signal_plus_bkg.plotOn( frame ) # , ROOT.RooFit.VisualizeError(fitresults_) )
            canvas = ROOT.TCanvas( name )
            frame.Draw()
            canvas.Write()

            frame_err = aMuMass.frame()
            data.plotOn( frame_err )
            signal_plus_bkg.plotOn( frame_err  , ROOT.RooFit.VisualizeError(fitresults_) )
            canvas_err = ROOT.TCanvas( name + "_err" )
            frame_err.Draw()
            canvas_err.Write()

            ws_out = ROOT.RooWorkspace( "ws_" + name )
            getattr( ws_out , "import" )( signal_plus_bkg )
            ws_out.Write()
            
            aux_objects.append( (name , ws_out , canvas , signal_plus_bkg , frame , data , pdfs , norms ,shapeBkg , shapeSig ) )



            ###start reading post_fit histograms from fitdiagnostics output

            h_bkgPsignal = fFitDiag.Get( "shapes_fit_s/ch%d/total" % chid )
            for bin in range(0 , h_bkgPsignal.GetNbinsX()+2 ):
                err = h_bkgPsignal.GetBinError( bin )
                val = h_bkgPsignal.GetBinContent( bin )
                if math.isnan(err) :
                    h_bkgPsignal.SetBinError( bin , math.sqrt( val ) )
            datahist = data.binnedClone()

            binRatio = h_bkgPsignal.GetNbinsX()/50
            h_bkgPsignal_orig = h_bkgPsignal.Rebin( binRatio , "total_50_%s" % name )
            h_bkgPsignal_orig.Scale( 1.0/binRatio )
            aMuMass.setBins( h_bkgPsignal_orig.GetNbinsX() )
            h_data_50 = datahist.createHistogram( "data_hist_%s_50" % name , aMuMass ) 
            h_data_50.SetLineColor( ROOT.kRed )

            binRatio = h_bkgPsignal.GetNbinsX()/nbins
            h_bkgPsignal = h_bkgPsignal.Rebin( binRatio , "total_%s" % name)
            h_bkgPsignal.Scale( 1.0/binRatio )
            aMuMass.setBins( nbins )
            h_data = datahist.createHistogram( "data_hist_%s" % name , aMuMass ) 

            h_data.SetLineColor( ROOT.kRed )
            if hBkgPlusSignal :
                hBkgPlusSignal.Add( h_bkgPsignal_orig )
                hData.Add( h_data_50 )
            else :
                hBkgPlusSignal = h_bkgPsignal_orig.Clone("hBkgPlusSignal")
                print "hey" , hBkgPlusSignal.GetNbinsX() , " " , h_bkgPsignal_orig.GetNbinsX()
                hData = h_data_50.Clone( "hTotalData" )
            
            h_bkgPsignal.Write( "total_%s" % name )
            h_data.Write()
            h_data_50.Write()
            h_bkgPsignal_orig.Write("total_50_%s" % name)
            canvas_fitDiag = ROOT.TCanvas( "CanvasBkgPlusSignal_%s" % name )
            h_bkgPsignal.Draw()
            h_data.Draw("same")
            canvas_fitDiag.Write()

        
        aMuMass.setBins( 50 )
        signal_plus_bkg_total = ROOT.RooAddPdf( "signal_plus_bkg"  , "Signal + Background"  , allpdfs , allnorms )
        frame = aMuMass.frame()
        data_obs.plotOn( frame )
        signal_plus_bkg_total.plotOn( frame , ROOT.RooFit.VisualizeError(fitresults_) )
        canvas = ROOT.TCanvas( "total" )
        frame.Draw()
        canvas.Write()

        canvas = ROOT.TCanvas( "total_fromfitDiag" )
        hData.Draw()
        hBkgPlusSignal.Draw("same")
        hData.Write()
        hBkgPlusSignal.Write()
        canvas.Write()

        fOutPlots.Close()


print AllIndices

