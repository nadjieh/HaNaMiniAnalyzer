from ROOT import TFile, TH2, TProfile, TFitResultPtr

files = ["LumiAnalysis_ZeroBias.root" , "LumiAnalysis_SingleMu.root" ]
varNames = ["nGoodVertices",
            "fixedGridRhoFastjetCentralChargedPileUp",
            "nChargedHadrons",
            "fixedGridRhoAll",
            "fixedGridRhoFastjetAll",
            "nVertices",
            "fixedGridRhoFastjetAllCalo",
            "fixedGridRhoFastjetCentral",
            "fixedGridRhoFastjetCentralCalo",
            "fixedGridRhoFastjetCentralNeutral",
            "nMus",
            "nEles",
            "nLostTracks",
            "nPhotons",
            "nNeutralHadrons"
]
Runs = ['B','C','D','E','F','G','H']

hName = "{Run:s}/h{Run:s}AVG{Var:s}"

for f in files :
    #print f
    fIn = TFile.Open( f )

    for run in Runs :
        for var in varNames :
            h = fIn.Get( hName.format( Run=run , Var=var) )
            #print hName.format( Run=run , Var=var)
            if h == None :
                #print "\tnot found"
                continue
            p = h.ProfileY()

            res = p.Fit( "pol1" , "SQ" )

            print f,run,var,res.Chi2(),res.Ndf()

    fIn.Close()
