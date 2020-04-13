#!/usr/bin/env python
from ROOT import gROOT, TLatex, TCanvas, TFile, gROOT, TColor
import string
import json
import os
import sys
from Haamm.HaNaMiniAnalyzer.Sample import Sample, JobInformation
from Haamm.HaNaMiniAnalyzer.SampleType import SampleType
from Haamm.HaNaMiniAnalyzer.Plotter import Plotter, CutInfo, ExtractConvases
from collections import OrderedDict

Sample.WD = os.path.dirname(os.path.abspath(__file__))
print Sample.WD

verbose=1
year = int(sys.argv[1])
if year==2016:
    LUMIS={'LowAPt':28200.0, 'HighAPt':35900.0}
elif year==2017:
    LUMIS={'LowAPt':7661.0,'HighAPt':41367.0}
LOCATION = "/home/hbakhshi/Downloads/CERNBox/Personal/Projects/VBFGamma/nTuples/April12/{}/".format( year )
samplesList=OrderedDict()
with open( 'samples{0}.json'.format( year ) , 'r') as jsonFile:
    samplesList.update( json.load(jsonFile, encoding='utf-8',object_pairs_hook=OrderedDict) )

sampleTypes = OrderedDict([ (str(l[3]),{'color': gROOT.GetColor(l[4]).GetNumber() if type(l[4])==int else TColor.GetColor(str(l[4])) , 'colorcode':str(l[4]) , 'isdata':l[1] , 'samples':[]}) for l in [ samplesList[s] for s in samplesList] ])
#print(sampleTypes)
#exit()

allLoadedFiles = []
for ss in samplesList:
    sampleInfo = samplesList[ss]
    ss_info = str(samplesList[ss][2])
    sample_parts = ss_info.split('/')
    if len(sample_parts) == 1:
        if verbose>0:
            print("wrong sample info {0}".format( ss ) )
        continue
    
    xsec=sampleInfo[0]
    isData=sampleInfo[1]
    if isData:
        xsec = 0
    dsname = ss_info
    sample = Sample(ss , xsec , False ,  "" , treeName="Events" )

    for filename in os.listdir(LOCATION):
        if filename.endswith(".root"):
            if isData:
                if sample_parts[1] in filename and sample_parts[2].split('-')[0] in filename :
                    sample.Jobs.append( JobInformation( sample , len(sample.Jobs) , [] ,  "{0}/{1}".format( LOCATION ,filename ) ) )
                    #sample.Files.append( "{0}/{1}".format( LOCATION ,filename ) )
                    allLoadedFiles.append( filename )
            elif sample_parts[1] in filename:
                sample.Jobs.append( JobInformation( sample , len(sample.Jobs) , [] ,  "{0}/{1}".format( LOCATION ,filename ) ) )
                allLoadedFiles.append( filename )
    subProcs=sampleInfo[3]
    if len(sample.Jobs) == 0:
        if verbose>0:
            print("No file for sample {0} found".format( ss ) )
        continue
    if subProcs in sampleTypes:
        sampleTypes[subProcs]['samples'].append( sample )
        #print(subProcs, [s.Name for s in sampleTypes[subProcs]['samples'] ] )
if verbose>0:        
    fileswithnosample=set(allLoadedFiles) - set(os.listdir(LOCATION))        
    print( "Following {0} files with no sample".format( len(fileswithnosample) ) )
    print(fileswithnosample)
        
    for st in sampleTypes :
        print(st)
        for s in sampleTypes[st]['samples']:
            print("\t{0}".format( [j.Output for j in s.Jobs] ) )

gROOT.SetBatch(False)

Cuts = { "LowPtTrigger":'(VBFGamma_evcats[1]==1 || VBFGamma_evcats[1]==-1)',
         "HightPtTrigger":'(VBFGamma_evcats[0]==1 || VBFGamma_evcats[0]==-1)',
         "LowPtRegion":'Photon_pt["VBFGamma_gamma_index"]<200',
         "HighPtRegion":'Photon_pt["VBFGamma_gamma_index"]>=200',
         "HighMJJ":'VBFGamma_JJ_M>=1000',
         "LowMJJ":'(VBFGamma_JJ_M>500 && VBFGamma_JJ_M<1000)',
         "W":"( (VBFGamma_wgt==0)*1+VBFGamma_wgt )*puWeight*VBFGamma_Fall17V2_{0}_Tight_SF".format( year ),
    }
            
            
    
AllCategories=[]
cLowAPt = CutInfo( "LowAPt" , " && ".join( [Cuts[i] for i in ['LowPtRegion', 'LowPtTrigger'] ] ) , Cuts['W'] , title="#gamma p_{t}<200"  )
AllCategories.append( cLowAPt )
cLowAPtHighMjj = CutInfo( "LowAPtHighMjj" , " && ".join( [Cuts[i] for i in ['LowPtRegion', 'LowPtTrigger' , 'LowMJJ'] ] ) , Cuts['W'] , title="#gamma p_{t} < 200, 500<m_{jj}<1000"  )
AllCategories.append( cLowAPtHighMjj )
cLowAPtVeryHighMjj = CutInfo( "LowAPtVeryHighMjj" , " && ".join( [Cuts[i] for i in ['LowPtRegion', 'LowPtTrigger' , 'HighMJJ'] ] ) , Cuts['W'] , title="#gamma p_{t} < 200, m_{jj}>1000"  )
#AllCategories.append( cLowAPtVeryHighMjj )

cLowAPt.AddHist( "jj_m" , "VBFGamma_JJ_M", 72 , 200 , 2000, False , Title="m_{jj}" , dirName="jj" )
cLowAPtHighMjj.AddHist( "jj_m" , "VBFGamma_JJ_M", 20 , 500 , 1000, False , Title="m_{jj}" , dirName="jj" )
cLowAPtVeryHighMjj.AddHist( "jj_m" , "VBFGamma_JJ_M", 40 , 1000 , 3000, False , Title="m_{jj}" , dirName="jj" )

cLowAPtVeryHighMjj.AddHist( cLowAPtHighMjj.AddHist( cLowAPt.AddHist( "aPt", 'Photon_pt["VBFGamma_gamma_index"]', 20 , 50 , 250, False , Title="#gamma p_{t}" , dirName="photon" ) ) )

cHighAPt = CutInfo( "HighAPt" , " && ".join( [Cuts[i] for i in ['HighPtRegion', 'HightPtTrigger'] ] ) , Cuts['W'] , title="#gamma p_{t}>200"  )
#AllCategories.append( cHighAPt )
cHighAPtHighMjj = CutInfo( "HighAPtHighMjj" , " && ".join( [Cuts[i] for i in ['HighPtRegion', 'HightPtTrigger' , 'LowMJJ'] ] ) , Cuts['W'] , title="#gamma p_{t} > 200, 500<m_{jj}<1000"  )
#AllCategories.append( cHighAPtHighMjj )
cHighAPtVeryHighMjj = CutInfo( "HighAPtVeryHighMjj" ,  " && ".join( [Cuts[i] for i in ['HighPtRegion', 'HightPtTrigger' , 'HighMJJ'] ] ) , Cuts['W'] , title="#gamma p_{t}>200, m_{jj}>1000"  )
#AllCategories.append( cHighAPtVeryHighMjj )

cHighAPt.AddHist( "jj_m" , "VBFGamma_JJ_M", 72 , 200 , 2000, False , Title="m_{jj}" , dirName="jj" )
cHighAPtHighMjj.AddHist( "jj_m" , "VBFGamma_JJ_M", 20 , 500 , 1000, False , Title="m_{jj}" , dirName="jj" )
cHighAPtVeryHighMjj.AddHist( "jj_m" , "VBFGamma_JJ_M", 40 , 1000 , 3000, False , Title="m_{jj}" , dirName="jj" )


cHighAPtVeryHighMjj.AddHist( cHighAPtHighMjj.AddHist( cHighAPt.AddHist( "aPt", 'Photon_pt["VBFGamma_gamma_index"]', 25 , 200 , 700, False , Title="#gamma p_{t}" , dirName="photon" ) ) )

jetProperties = [ ('area' , 18 , .25 , .65 ),
                  ('btagCMVA' , 40 , -1 , 1 ),
                  ('btagCSVV2' , 10 , 0 , 1 ) ,
                  ('btagDeepB' , 10 , 0 , 1 ) ,
                  ('btagDeepC' , 10 , 0 , 1 ) ,
                  ('btagDeepFlavB', 10 , 0 , 1 ),
                  ('btagDeepFlavC' , 10 , 0 , 1 ),
                  ('chEmEF' , 20 , 0 , 1 ),
                  ('chHEF' , 20 , 0 , 1 ),
                  ('eta' , 24 , -4.7 , 4.7 ),
                  #('jerCHF' , 20 , 0 , 1 ),
                  #('jerCHPUF' , 15 , 0 , 3 ),
                  ('mass' , 25 , 0 , 100),
                  ('muEF' , 100 , 0 , 1 ) ,
                  ('muonSubtrFactor' , 100 , 0 , 1 ),
                  ('neEmEF' , 20 , 0 , 1 ),
                  ('neHEF' , 20 , 0 , 1 ),
                  ('phi' , 16 , -3.2 , 3.2),
                  ('pt' , 50 , 20 , 520),
                  ('qgl' , 20 , 0 , 1 ),
                  ('rawFactor' , 30, -1 , .5 ) ,
                  ('bRegCorr' , 20 , .5 , 1.5 ),
                  ('bRegRes' , 25 , 0 , .5 ),
                  ('electronIdx1' , 6 , -1 , 5 ),
                  ('electronIdx2' , 6 , -1 , 5 ),
                  ('jetId' , 8 , 0 , 8 ),
                  ('muonIdx1', 6 , -1 , 5 ),
                  ('muonIdx2' , 6 , -1 , 5 ),
                  ('nConstituents' , 35 , 0 , 70 ),
                  ('nElectrons' , 10 , 0 , 10 ),
                  ('nMuons' , 10 , 0 , 10 ),
                  ('puId' , 8 , 0 , 8 )
]
photonProperties = [('eCorr' , 20 , .9 , 1.1 ) ,
                    ('energyErr' , 10 , 0 , 100 ) ,
                    ('eta' , 30 , -3 , 3 ) ,
                    ('hoe' , 20 , 0 , 2 ) ,
                    ('mass' , 12 , -0.00006 , 0.00006),
                    ('mvaID' , 20 , -1 , 1),
                    ('mvaID17' if year==2016 else 'mvaIDV1' , 20 , -1 , 1),
                    ('pfRelIso03_all' , 20 , 0 , 20),
                    ('pfRelIso03_chg' , 20 , 0 , 10),
                    ('phi' , 16 , -3.2 , 3.2),
                    ('r9' , 20 , 0 , 2),
                    ('sieie' , 25 , 0 , 0.1),
                    ('cutBased' if year==2016 else 'cutBasedBitmap' , 8 , 0 , 8),
                    ('cutBased17Bitmap' if year==2016 else 'cutBasedV1Bitmap' , 8 , 0 , 8),
                    ('electronIdx' , 8 , 0 , 8),
                    ('jetIdx' , 8 , 0 , 8),
                    ('vidNestedWPBitmap' , 32 , 0 , 1600 ),
                    ('electronVeto' , 2 , 0 , 2 ),
                    ('isScEtaEB' , 2 , 0 , 2 ),
                    ('isScEtaEE' , 2 , 0 , 2 ),
                    ('mvaID_WP90' , 2, 0 , 2 ),
                    ('mvaID_WP80' , 2 , 0 , 2 ),
                    ('pixelSeed' , 2, 0 , 2 ),
                    ('seedGain' , 20 , 0 , 20 )
]
if year==2016:
    photonProperties.append( ('mvaID17_WP80' , 2 , 0 , 2 ) )
    photonProperties.append( ('mvaID17_WP90' , 2 , 0 , 2 ) )

                      
AllVariables = []
AllPlotters = []
plotter = Plotter()
for st in reversed(sampleTypes.keys()):
    info = sampleTypes[st]
    ST = SampleType(st , info['color'] , info['samples']  )
    plotter.AddSampleType( ST )
    AllPlotters.append( plotter )

outDir = '/home/hbakhshi/Downloads/CERNBox/www/SMP-19-005/April9/{0}/'.format( year )
if not os.path.exists( outDir ):
    os.mkdir( outDir )

for cut in AllCategories:
    

    # AllVariables.append( cut.AddHist( "aYStar", "VBFGamma_a_ystar" , 16 , -4 , 4 , False , Title="photon yStar" , dirName="photon" ) )
    # for pp in photonProperties:
    #     AllVariables.append( cut.AddHist( "a{0}".format(pp[0].replace('_' , "")), "Photon_{0}[VBFGamma_gamma_index]".format( pp[0] ) , pp[1] , pp[2] , pp[3] , False , Title="photon {0}".format(pp[0]) , dirName="photon" ) )

    # AllVariables.append( cut.AddHist( "jjpt" , "VBFGamma_JJ_Pt" , 12 , 0 , 600 , False , Title="p^{jj}_{t}" , dirName="jj" ) )
    # AllVariables.append( cut.AddHist( "jjScalarSum" , "VBFGamma_JJ_ScalarSum" , 18 , 90 , 990 , False , Title="jj_{HT}" , dirName="jj" ) )
    # AllVariables.append( cut.AddHist( "jjPhi" , "VBFGamma_JJ_Phi" , 16 , -3.2 , 3.2 , False , Title="jj_{#phi}" , dirName="jj" ) )
    # AllVariables.append( cut.AddHist( "jjEta" , "VBFGamma_JJ_Eta" , 18 , -4.5 , 4.5 , False , Title="jj_{#eta}" , dirName="jj" ) )
    # AllVariables.append( cut.AddHist( "jjDPhi" , "VBFGamma_JJ_DPhi" , 16 , -3.2 , 3.2 , False , Title="jj_{#Delta#phi}" , dirName="jj" ) )
    # AllVariables.append( cut.AddHist( "jjSEta", "VBFGamma_JJ_SEta" , 18 , -4.5 , 4.5 , False , Title="jj_{S#eta}" , dirName="jj" ) )
    # AllVariables.append( cut.AddHist( "jjDEta", "VBFGamma_JJ_DEta" , 14 , 0 , 7 , False , Title="jj_{D#eta}" , dirName="jj" ) )
    # AllVariables.append( cut.AddHist( "jjDRa", "VBFGamma_jj_dr2a" , 35 , 0 , 7 , False , Title="#DeltaR(jj,#gamma)" , dirName="jj" ) )
    # AllVariables.append( cut.AddHist( "nCentJets", "VBFGamma_nCentJets" , 7 , 0 , 7 , False , Title="#central jets" , dirName="centj" ) )
    # AllVariables.append( cut.AddHist( "CentJetYStart", "VBFGamma_CentJet_YStar" , 20 , -5 , 5 , False , Title="Central Jet YStar" , dirName="centj" ) )
    # for jp in jetProperties:
    #     AllVariables.append( cut.AddHist( "CentJet{0}".format(jp[0]),
    #                                       "(VBFGamma_CentJet_Index<0)*100*{0}+(VBFGamma_CentJet_Index>-1)*Jet_{1}[(VBFGamma_CentJet_Index>-1)*VBFGamma_CentJet_Index]".format( jp[3], jp[0] ),
    #                                       jp[1] , jp[2] , jp[3] , False , Title="central jet {0}".format(jp[0]) , dirName="centj" ) )
    #     AllVariables.append( cut.AddHist( "LeadingJet{0}".format(jp[0]), "Jet_{0}[VBFGamma_LeadinJet_index]".format( jp[0] ) , jp[1] , jp[2] , jp[3] , False , Title="leading jet {0}".format(jp[0]) , dirName="leadingj" ) )
    #     AllVariables.append( cut.AddHist( "SubLeadingJet{0}".format(jp[0]), "Jet_{0}[VBFGamma_SubLeadinJet_index]".format( jp[0] ) , jp[1] , jp[2] , jp[3] , False , Title="sub-leading jet {0}".format(jp[0]) , dirName="subleadingj" ) )

    # AllVariables.append( cut.AddHist( "leaddr2a", "VBFGamma_lead_dr2a" , 35 , 0 , 7 , False , Title="#DeltaR(j1,#gamma)" , dirName="leadingj" ) )
    # AllVariables.append( cut.AddHist( "subleaddr2a", "VBFGamma_sublead_dr2a" , 35 , 0 , 7 , False , Title="#DeltaR(j2,#gamma)" , dirName="subleadingj" ) )

    # AllVariables.append( cut.AddHist( "ajjpt", "VBFGamma_ajj_pt" , 50 , 0 , 50 , False , Title="ajj p_{t}" , dirName="ajj" ) )
    # AllVariables.append( cut.AddHist( "ajjeta", "VBFGamma_ajj_eta" , 18 , -4.5 , 4.5 , False , Title="ajj #eta" , dirName="ajj" ) )
    # AllVariables.append( cut.AddHist( "ajjphi", "VBFGamma_ajj_phi" , 16 , -3.2 , 3.2 , False , Title="ajj #phi" , dirName="ajj" ) )
    # AllVariables.append( cut.AddHist( "ajjmass", "VBFGamma_ajj_m" , 40 , 100 , 4100 , False , Title="ajj mass" , dirName="ajj" ) )
    # AllVariables.append( cut.AddHist( "scalarht", "VBFGamma_scalarht" , 45 , 100 , 1600 , False , Title="ajj scalarht" , dirName="ajj" ) )

    # AllVariables.append( cut.AddHist( "isotropy", "VBFGamma_es_isotropy" , 40 , 0 , 1 , False , Title="isotropy" , dirName="eventshape" ) )
    # AllVariables.append( cut.AddHist( "circularity", "VBFGamma_es_circularity" , 40 , 0 , 1 , False , Title="circularity" , dirName="eventshape" ) )
    # AllVariables.append( cut.AddHist( "sphericity", "VBFGamma_es_sphericity" , 50 , 0 , 500 , False , Title="sphericity" , dirName="eventshape" ) )
    # AllVariables.append( cut.AddHist( "aplanarity", "VBFGamma_es_aplanarity" , 10 , 0 , 50 , False , Title="aplanarity" , dirName="eventshape" ) )    
    # AllVariables.append( cut.AddHist( "C", "VBFGamma_es_C" , 100 , 0 , 1000000 , False , Title="C" , dirName="eventshape" ) )
    # AllVariables.append( cut.AddHist( "D", "VBFGamma_es_D" , 100 , 0 , 1000000 , False , Title="D" , dirName="eventshape" ) )

    cut.MakeTextFile()
    plotter.AddTreePlots( cut )
plotter.LoadHistos( LUMIS , dirName_="./" , cftName='hTotalNEvents' )
fout = TFile.Open("{1}/out_{0}.root".format(year , outDir) , "recreate")
xml_root = plotter.Write( fout , False )# , png_folder=outDir)
fout.Close()
del plotter
del fout

ExtractConvases( "{1}/out_{0}.root".format(year , outDir)  , outDir , [ 'png' , 'pdf' , 'png' ] )

