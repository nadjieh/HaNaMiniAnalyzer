from ROOT import TDirectory, TFile, TCanvas , TH1D , TH1 , TH2D , THStack, TList, gROOT, TLegend, TPad, TLine, gStyle, TTree , TObject , gDirectory, TEntryList, TEventList, TProof, TColor
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring
import os
import sys
import Sample
from array import array
from collections import OrderedDict
from ExtendedSample import *
from SampleType import *
from Property import *

TheProof = None
    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class HistInfo:
    def __init__(self , name , varname = None , nbins = None , _from = None , to = None , title = "" , Auto = False , dirName = None):
        self.DirName = dirName
        self.Title = title
        self.TwoD = False
        if isinstance(name, HistInfo) and type(varname) == str and nbins == None and _from == None and to == None :
            s = name.Name
            if len(name.Name.split("_")) > 1 :
                s = name.Name.split("_")[-1]
            self.Name = varname + "_" + s
            self.VarName = name.VarName
            
            self.nBins = name.nBins
            self.From = name.From
            self.To = name.To
            self.Auto = name.Auto

            self.DirName = name.DirName
        elif type(name) == str and type(varname) == str and type(nbins) == int and ( type(_from) == float or type(_from) == int ) and ( type(to) == float or type(to) == int ) :
       
            self.Name = name
            self.VarName = varname

            self.nBins = nbins
            self.From = float(_from)
            self.To = float(to)
            self.Auto = False
        elif type(name) == str and type(varname) == str and type(nbins) == int and Auto :
            self.Name = name
                
            self.VarName = varname

            self.nBins = nbins
            self.From = float(0)
            self.To = float(0)
            self.Auto = True
            
        elif isinstance(name, HistInfo) and isinstance(varname, HistInfo) and type(nbins) == str  and _from == None and to == None : #2d
            s = name.Name
            if len(name.Name.split("_")) > 1 :
                s = name.Name.split("_")[-1]
                
            s2 = varname.Name
            if len(s2.split("_")) > 1 :
                s2 = s2.split("_")[-1]

            self.Name = nbins + "_" + s + "vs" + s2
            self.VarName = name.VarName + ":" + varname.VarName

            self.H1 = name
            self.H2 = varname
            self.TwoD = True
            self.Auto = False

        else:
            print "Initiate histinfo correctly, the given parameters are not allowd"

    def MakeEmptyHist(self , sName , index = 0):
        hname = self.MakeName( sName , index )
        if hasattr(self, "emptyhist" ):
            return self.emptyhist
        elif self.TwoD:
            self.emptyhist = TH2D( hname , self.Title , self.H2.nBins , float( "{0:.2g}".format(self.H2.From)) , float( "{0:.2g}".format(self.H2.To)) , self.H1.nBins , float( "{0:.2g}".format(self.H1.From)) , float( "{0:.2g}".format(self.H1.To)) )
        else:
            self.emptyhist = TH1D( hname , self.Title , self.nBins , float( "{0:.2g}".format(self.From) ) , float( "{0:.2g}".format(self.To)) )

        return self.emptyhist
        
    def Bins(self):
        if self.TwoD:
            return "%s,%s" % (self.H2.Bins() , self.H1.Bins())
        else:
            return "%d,%.2g,%.2g" % (self.nBins , self.From , self.To)
            
    def MakeName(self , sName , index = 0 ):
        return "%s_%s_%d" % (sName , self.Name , index )

class CutInfo:
    def __init__(self, name , cut , weight = "1"  , title = "" , blind=False ):
        self.Name = name
        self.Cut = cut
        self.Weight = weight

        self.ListOfEvents = {}
        self.ListOfHists = []
        self.AllTH1s = {}

        self.GREs = []
        self.Blind = blind
        self.Title = name if title == "" else title
        
    def AddHist(self, name , varname = None , nbins = None , _from = None , to = None , GRE = True , Title = "" , Auto = False , dirName = None  ):
        self.GREs.append(GRE)
        Title = self.Title + ";" + Title 
        if isinstance(name , HistInfo) and varname == None and nbins == None and _from == None and to == None :
            OrigTitle = name.Title.split(";")
            if len(OrigTitle) > 1 :
                Title = ";".join( [ self.Title ] + OrigTitle[1:] )
            else :
                Title = self.Title
            self.ListOfHists.append( HistInfo(name , self.Name , title = Title , dirName = dirName ) )
        elif type(name) == str and type(varname) == str and type(nbins) == int and ( type(_from) == float or type(_from) == int ) and ( type(to) == float or type(to) == int ) :
            self.ListOfHists.append( HistInfo( self.Name + "_" + name , varname , nbins , _from , to , title = Title , dirName = dirName) )
        elif type(name) == str and type(varname) == str and type(nbins) == int and Auto :
            name = name.replace("_" , "")
            self.ListOfHists.append( HistInfo( self.Name + "_" + name , varname , nbins , title = Title , Auto = True , dirName = dirName ) )
        elif isinstance(name , HistInfo) and isinstance(varname , HistInfo) and nbins == None and _from == None and to == None : #2d histogram
            self.ListOfHists.append( HistInfo(name , varname , self.Name , title = Title , dirName = dirName) )
        else:
            print "Initiate histinfo correctly, the given parameters to AddHists are not allowd(%s=%s,%s=%s,%s=%s,%s=%s,%s=%s)" % (type(name),name,type(varname),varname,type(nbins),nbins,type(_from),_from,type(to),to)

        return self.ListOfHists[-1]
        
    def SetWeight(self, w):
        self.Weight = w
        
    def Weights(self, index = 0 , samplename = "" , isdata = False):
        if hasattr( self , "Weight"):
            if type(self.Weight) == str:
                return self.Weight
            elif type( self.Weight) == dict:
                if samplename in self.Weight:
                    return self.Weight[ samplename ]
                elif isdata and "data" in self.Weight:
                    return self.Weight["data"]
                else:
                    return self.Weight["all"]
        else:
            return ("Weight.W%d" % (index) )

    def MakeTextFile(self):
        fout = open( self.Name , "w" )
        fout.write( self.Cut + "\n" )
        fout.write( self.Weight + "\n" )
        for hist in self.ListOfHists:
            hname =  hist.MakeName('{SN}' , 0)
            fout.write("%s,%s>>cloned_%s(%s)\n" % ( hist.Name , hist.VarName , hname , hist.Bins() ) )

    def LoadHistosWithProof( self, samplename , isdata , tree ):
        if tree.GetEntries() != 0:
            tree.SetProof()
            dir_ = "/home/hbakhshi/Downloads/CERNBox/Personal/Projects/VBFGamma/HaNaMiniAnalyzer/vbf"
            print( "{0}/{1}:{2}:{3}".format( dir_ , self.Name , samplename , int(isdata) ) )
            tree.Process( "Sel" , "{0}/{1}:{2}:{3}".format( dir_ , self.Name , samplename , int(isdata) ) )
        
            lst = TheProof.GetOutputList ()
            for i in range(lst.GetEntries()):
                print( "name {0}: {1}".format( i , lst.At(i).GetName() ) )
        else:
             lst = TList()   
        ret = {}
        for hist in self.ListOfHists:
            ret[hist.Name] = {}
            n = 0
            hname =  hist.MakeName(samplename , n)
            if not TheProof.GetOutput( "cloned_"+hname , lst ):
                print( hname + ' not found' )
                if tree.GetEntries() == 0:
                    setattr( self , hname , hist.MakeEmptyHist( samplename , n ) )
            else:
                gROOT.cd()
                setattr( self , hname , TheProof.GetOutput( "cloned_"+hname , lst ).Clone( hname ) )

            hhh = getattr( self , hname )
            hhh.SetTitle( hist.Title )
            #hhh.SetTitle( self.Title )
            rebined = False
            correct = True
            color = bcolors.OKBLUE
            if not hist.TwoD :
                if not hhh.GetNbinsX() == hist.nBins :
                    if hhh.GetNbinsX()%hist.nBins == 0:
                        hhh.Rebin( hhh.GetNbinsX()/hist.nBins )
                        rebined = True
                        color = bcolors.WARNING
                    else:
                        correct = False
                        color = bcolors.FAIL
                        
            print "%s\t\t\tHisto %s[%d] created ([%d,%.1f,%1f] and integral=%.2f, average=%.2f)%s" % (color, hist.Name , n , hhh.GetXaxis().GetNbins() , hhh.GetXaxis().GetBinLowEdge(1) , hhh.GetXaxis().GetBinLowEdge( hhh.GetXaxis().GetNbins() ) + hhh.GetXaxis().GetBinWidth( hhh.GetXaxis().GetNbins() ) , hhh.Integral() , hhh.GetMean() , bcolors.ENDC )
                        
                    
            hhh.SetLineColor( 1 )
            hhh.SetLineWidth( 2 )
            #hhh.SetBit(TH1.kNoTitle)
            if not isdata :
                hhh.SetFillStyle( 1001 )
            else:
                hhh.SetStats(0)

            ret[hist.Name][n] = hhh

        lst.Delete()
        return ret

    def LoadHistos( self , samplename , isdata , tree , indices=[0] , additionalCut = None  ):
        global TheProof
        if TheProof: # and not isdata:
            print("Loading {0} histograms using proof".format( samplename ) )
            return self.LoadHistosWithProof( samplename , isdata , tree )
        print( "Proof is {0}".format( TheProof ) )
        UseEventList = gROOT.GetVersionInt() > 60000
        
        #print UseEventList, gROOT.GetVersionInt()
        if UseEventList :
            tree.SetEventList( None )
        else:
            tree.SetEntryList( None )
        
        cut_ = self.Cut
        if(additionalCut):
            cut_ += " && " + additionalCut

        if self.Blind and isdata:
	    if cut_ == "":
		cut_ += "(abs(higgsMass - 125.0) > 10)"
	    else:
		cut_ += " && (abs(higgsMass - 125.0) > 10)"
                        
        nLoaded = tree.Draw( ">>list_%s_%s"%(samplename, self.Name) , cut_  , "" if UseEventList else  "entrylist" )
        #gDirectory.ls()
        lst = gDirectory.Get( "list_%s_%s"%(samplename, self.Name) )
        print "%s\t\tEvents from tree are loaded (%s , %s), %d" % (bcolors.UNDERLINE, self.Name , cut_ , nLoaded )
        print "\t\tHistograms from tree are being created" + bcolors.ENDC
        if nLoaded < 0:
            print "Error in loading events with cut (%s) from dataset (%s), nLoaded = %d" % (cut_,samplename , nLoaded)
        if nLoaded < 1 :
            if UseEventList :
                self.ListOfEvents[samplename] = TEventList( "list_%s" % (samplename) , cut_ )
            else:
                self.ListOfEvents[ samplename ] = TEntryList( "list_%s" % (samplename) ,cut_ , tree )
        else:
            self.ListOfEvents[samplename] = lst

        #print self.ListOfEvents[samplename]
        #self.ListOfEvents[samplename].Print()
        #self.ListOfEvents[samplename].SetTreeName( tree.GetName() )
        if UseEventList :
	    tree.SetEventList( self.ListOfEvents[samplename] )
        else:
            tree.SetEntryList( self.ListOfEvents[samplename] )
            
        ret = {}
        for hist in self.ListOfHists:
            ret[hist.Name] = {}
            for n in indices:
                hname =  hist.MakeName(samplename , n)
                gROOT.cd()
                
                tocheck = [] #"jPt","jEta" , "jPhi","bjPt" ]
                for sss in tocheck:
                    if sss in hist.Name:
                        print "%s : %d , %.2f , %.2f" % (hist.Name , hist.nBins , hist.From , hist.To)

                if nLoaded > 0:
                    if hist.Auto :
                        hist.From = tree.GetMinimum( hist.VarName )
                        hist.To = tree.GetMaximum( hist.VarName )
                        if hist.nBins < 1 :
                            hist.nBins = 10
                        hist.Auto = False
                        import __main__ as main
                        with open(main.__file__ , "a") as f:
                            f.write("#{0:s}:[{1:d},{2:.2g},{3:.2g}]".format( hist.VarName , hist.nBins , hist.From , hist.To ) )

                    tree.Draw( "%s>>cloned_%s(%s)" % ( hist.VarName , hname , hist.Bins() ) ,
                               "" if isdata else self.Weights( n , samplename , isdata) )
                    #print self.Weights(n,samplename,isdata)
                    if not gDirectory.Get( "cloned_"+hname ):
                        print( hname + ' not found' )
                    setattr( self , hname , gDirectory.Get( "cloned_"+hname ).Clone( hname ) )
                else :
                    hcloned_empty = hist.MakeEmptyHist( samplename , n )
                    setattr( self , hname , hcloned_empty )
                hhh = getattr( self , hname )
                hhh.SetTitle( hist.Title )
                #hhh.SetTitle( self.Title )
                rebined = False
                correct = True
                color = bcolors.OKBLUE
                if not hist.TwoD :
                    if not hhh.GetNbinsX() == hist.nBins :
                        if hhh.GetNbinsX()%hist.nBins == 0:
                            hhh.Rebin( hhh.GetNbinsX()/hist.nBins )
                            rebined = True
                            color = bcolors.WARNING
                        else:
                            correct = False
                            color = bcolors.FAIL
                        
                print "%s\t\t\tHisto %s[%d] created ([%d,%.1f,%1f] and integral=%.2f, average=%.2f)%s" % (color, hist.Name , n , hhh.GetXaxis().GetNbins() , hhh.GetXaxis().GetBinLowEdge(1) , hhh.GetXaxis().GetBinLowEdge( hhh.GetXaxis().GetNbins() ) + hhh.GetXaxis().GetBinWidth( hhh.GetXaxis().GetNbins() ) , hhh.Integral() , hhh.GetMean() , bcolors.ENDC )
                        
                    
                hhh.SetLineColor( 1 )
                hhh.SetLineWidth( 2 )
                #hhh.SetBit(TH1.kNoTitle)
                if not isdata :
                    hhh.SetFillStyle( 1001 )
                else:
                    hhh.SetStats(0)

                ret[hist.Name][n] = hhh

        return ret
        
class Plotter:
    def __init__(self):
        TH1.SetDefaultSumw2(True)
        self.Samples = []
        self.Props = {}
        self.TreePlots = []

    def FindGRE(self, histname):
        #print "In Find method: %s" %histname
        found = False
        gre = True
        for i in range(0, len(self.TreePlots)):
            for j in range(0, len(self.TreePlots[i].ListOfHists)):
                #print "%s" %self.TreePlots[i].ListOfHists[j].Name
                if self.TreePlots[i].ListOfHists[j].Name == histname:
                    gre = self.TreePlots[i].GREs[j]
                    found = True
                    break;
            if(found):
                break
        return gre	        

    def AddTreePlots( self , selection ):
        self.TreePlots.append( selection )
        
    def AddSampleType(self , st):
        self.Samples.append(st)
              
    def AddLabels(self , hist , labels ):
        if labels :
            self.Props[hist].SetLabels(labels)

    def Rebin(self , hist , newbins):
        self.Props[hist].Rebin( newbins )
                        
    def GetData(self, propname):
        for st in self.Samples:
            if st.IsData():
                return st.AllHists[propname]
        return None

    def LoadHistos(self  , lumi , dirName_ = "Hamb" , cftName = "CutFlowTable" , proof = True):
        #for st in self.Samples :
        #print "%sCreating histos for : %s%s" % (bcolors.OKGREEN , st.Name , bcolors.ENDC)
        ##if not st.Name.count("Signal"):
        ##    dirName = "Hamb"
        ##else:
        dirName = dirName_
        #with poolcontext(processes=1) as pool:
        #    self.Samples = pool.map( partial(LoadHistosCaller, lumi_=lumi , dirName_=dirName , cftName_=cftName , tp=self.TreePlots), self.Samples)
            #pool.map( LoadHistosCaller , [ (st,lumi , dirName , cftName , self.TreePlots) for st in self.Samples ] )
        #print( lumi , dirName , cftName , self.TreePlots )

        if proof :
            global TheProof
            TheProof = TProof.Open("workers=8")
            current_dir = os.getcwd()
            #gROOT.ProcessLine(".L {0}/Sel.C++".format(current_dir))
            TheProof.Load("{0}/Sel.C+".format(current_dir))

        for st in self.Samples :
            st.LoadHistos( lumi , dirName , cftName , self.TreePlots )
            for prop in st.AllHists:
                if not prop in self.Props:
                	self.Props[prop] = Property( prop , OrderedDict() , None, [] , [], self.FindGRE(prop)) 
                    #self.Props[prop] = Property( prop , OrderedDict() , None, None , [] )
                append = []
                for s in st.Samples:
                    if prop in s.AllHists:
                        append.append( s.AllHists[prop][0] )
                    else:
                        print "prop %s doesn't exist in %s!" % (prop , s.Name )
                self.Props[prop].Samples += append #[ s.AllHists[prop][0] for s in st.Samples ]
                if st.IsData():
                    self.Props[prop].Data = st.AllHists[prop]
                elif st.IsSignal:
                    self.Props[prop].Signal.extend( st.AllOtherHists[prop].values() )
                else :
                    self.Props[prop].Bkg[st.Name] = st.AllHists[prop]

                #print( prop , st)
        if proof :
            TheProof.Close()
            del TheProof

    def DrawAll(self , normtodata ):
        gStyle.SetOptTitle(0)
        for prop in self.Props :
            self.Props[prop].Draw(normtodata)

    def GetProperty(self , propname):
        return self.Props[propname]

    def CalcSignificances(self, method=1):
	print ("Significance calculation with method %d" % method)
	if method > 4:
	    print "Illigal method!"
	    return
	for prop in self.Props:
	    self.Props[prop].SetSignificances(method)    
    		
    def CalcExpLimits(self):
	print "Limit calculation"    
	for prop in self.Props:
            self.Props[prop].SetExpectedLimits()
    
    def Write(self, fout , normtodata , png_folder = None , root_xml_node = None ):
        print "%sStarted writing the plots to the output file (%s)...%s" % (bcolors.BOLD, fout.GetPath() , bcolors.ENDC)
        root = root_xml_node
        root_categories = {}
        if png_folder :
            if not os.path.exists( png_folder ):
                os.mkdir( png_folder )
            if root is None:
                root = Element("categories")

        for propname in self.Props :
            propdir = None
            seldirname = fout.GetName()
            for selection in self.TreePlots:
                for t in selection.ListOfHists:
                    if t.Name == propname :
                        seldirname = selection.Name                        
                        seldir = fout.GetDirectory(seldirname)
                        if not seldir:
                            seldir = fout.mkdir( seldirname )
                        subdir = seldir
                        if t.DirName and not seldir.GetDirectory(t.DirName) :
                            subdir = seldir.mkdir( t.DirName )
                        elif t.DirName :
                            subdir = seldir.GetDirectory(t.DirName)
                        propdirname = propname
                        if len(propname.split("_")) > 1 :
                            propdirname = propname.split("_")[-1]
                        propdir = subdir.GetDirectory( propdirname )
                        if not propdir :
                            propdir = subdir.mkdir( propdirname )

            if root is not None and seldirname not in root_categories:
                cat_el = SubElement(root, "category")
                cat_name = SubElement( cat_el , 'name').text = seldirname
                variables = SubElement( cat_el , 'variables')
                root_categories[ seldirname ] = variables
                            
            if not propdir :
                propdir = fout.mkdir( propname )

            if png_folder:
                self.Props[propname].Write(propdir, normtodata, png_filename = '{0}/{1}_{2}.png'.format( png_folder , seldirname , propname ) , xml_node = root_categories[seldirname] )
            else:
                self.Props[propname].Write(propdir, normtodata)
                
            fout.cd()

        if root is not None:
            tree = ElementTree(root)
            tree.write(png_folder+"/data.xml")
    
            import xml.dom.minidom
            dom = xml.dom.minidom.parse(png_folder+'/data.xml')
            pi = dom.createProcessingInstruction('xml-stylesheet',
                                                 'type="text/xsl" href="/hbakhshi/SMP-19-005/categories.xsl"')
            dom.insertBefore(pi, dom.firstChild)
            with open(png_folder+'/data.xml' , 'w') as f:
                pretty_xml_as_string = dom.toprettyxml()
                f.write( pretty_xml_as_string )
            return root


def GetCanvases(d):
    #"Generator function to recurse into a ROOT file/dir and yield (path, obj) pairs"
    #https://root-forum.cern.ch/t/loop-over-all-objects-in-a-root-file/10807/4
    for key in d.GetListOfKeys():
        kname = key.GetName()
        if key.IsFolder():
            # TODO: -> "yield from" in Py3
            for i in GetCanvases(key.ReadObj()):
                yield i
        else:
            if key.GetClassName() == 'TCanvas':
                yield ( key.GetMotherDir() , key.GetMotherDir().GetPath() ) #ReadObj()

def ExtractConvases(inFile , outdir , formats):
    TColor.DefinedColors()
    TColor.GetColor("#7fc97f")
    TColor.GetColor("#DCDCDC")
    TColor.GetColor("#386cb0")
    TColor.GetColor("#fdc086")
    TColor.GetColor("#f0027f")
    TColor.DefinedColors()

    f = TFile.Open(inFile)
    canvases = GetCanvases( f )
    allcategories = {}
    for dir_,address in set( [c for c in canvases ] ):
        p =  Property.FromDir( dir_)
        if p.Data is None:
            continue

        print( address )
        filename = address.split(':/')[1].replace('/' , '_' )
        parts = filename.split('_')
        category = parts[0]
        subcategory = parts[1] if len(parts) >2 else "Plots"
        if category in allcategories:
            if subcategory in allcategories[category]:
                allcategories[category][subcategory].append( filename )
            else:
                allcategories[category][subcategory] = [filename]
        else:
            allcategories[category] = {subcategory:[filename]}
        
        p.Data.GetYaxis().SetRangeUser( 0.0 , 2*max(p.Data.GetMaximum(), p.GetStack().GetStack().Last().GetMaximum()) )
	p.Draw(False , canvas_appendix='main')
	p.Draw(False , W=400 , H=300 , canvas_appendix='thumbnail')
        c = p.GetCanvas(0 , appendix='main')
        cth = p.GetCanvas(0 , appendix='thumbnail')
        for frmt in formats:
            p.Data.SetMarkerStyle(20)
            c.SaveAs( "{0}/{1}.{2}".format( outdir , filename , frmt ) )
            p.Data.SetMarkerStyle(7)
            cth.SaveAs( "{0}/{1}_thumb.{2}".format( outdir , filename , frmt ) )
        p.Data.GetYaxis().SetRangeUser( 0.001 , 500*p.Data.GetMaximum() )
        p.GetCanvas(padid=1 , appendix='main').SetLogy()
        p.GetCanvas(padid=1 , appendix='thumbnail').SetLogy()
        gSystem.ProcessEvents()
        gSystem.ProcessEvents()
        p.Data.SetMarkerStyle(20)
        for frmt in formats:
            c.SaveAs( "{0}/{1}_log.{2}".format( outdir , filename , frmt ) )
        p.Data.SetMarkerStyle(7)
        gSystem.ProcessEvents()
        for frmt in formats:
            cth.SaveAs( "{0}/{1}_thumb_log.{2}".format( outdir , filename , frmt ) )
                
        cth.Close()
        c.Close()
        del p
    print( allcategories )
    f.Close()

    root = Element("categories")
    for cat in allcategories:
        cat_el = SubElement(root, "category")
        cat_name = SubElement( cat_el , 'name').text = cat
        subcategories = SubElement( cat_el , 'subcats')
        #root_categories[ seldirname ] = variables
        for subcat in allcategories[cat]:
            subcat_ = SubElement( subcategories , 'SubCategory' )
            SubElement( subcat_ , 'name').text = subcat
            variables = SubElement( subcat_ , 'variables')
        
            for png_filename in allcategories[cat][subcat]:
                var_el = SubElement(variables, "variable")
                SubElement( var_el , "name" ).text = '_'.join( png_filename.split('_')[1:] )
                png_filename = '/' + png_filename + '.png'
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

    tree = ElementTree(root)
    tree.write(outdir+"/data.xml")

    import xml.dom.minidom
    dom = xml.dom.minidom.parse(outdir+'/data.xml')
    pi = dom.createProcessingInstruction('xml-stylesheet',
                                         'type="text/xsl" href="/hbakhshi/SMP-19-005/categories.xsl"')
    dom.insertBefore(pi, dom.firstChild)
    with open(outdir+'/data.xml' , 'w') as f:
        pretty_xml_as_string = dom.toprettyxml()
        f.write( pretty_xml_as_string )
    return root
