#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)

#toAddSamples = ["TChannel" ]

from Samples80.Samples import *
samples = None
runOnOutsOfAnotherJob = False
if runOnOutsOfAnotherJob :
    samples = samples24june
    samples += sampleswith24juneonly
else :
    samples = MiniAOD80Samples

from Haamm.HaNaMiniAnalyzer.ExtendedSample import *

samples_extended = []
for sample in samples:
    if not any( [sample.Name.count(sname) for sname in ["VBF" , "GGH" ] ] ):
        continue
        #job is already created : sample.MakeJobs( 20 , "%s/%s" % (OutPath24June , prefix) )
    #    print sample.Name 
    #else:
    sample.MakeJobs( 2 , "eos/cms/store/user/%s/%s/%s" % (GetUserName(), "scales" , "out" ) ) 

    ss = ExtendedSample(sample)
    #export EOS_MGM_URL=root://eosuser.cern.ch
    #eosmount eos_cb
    ss.fhadd("./scales/")
    samples_extended.append( ss )

for ss in samples_extended:
    ss.PrintHaddResults()
