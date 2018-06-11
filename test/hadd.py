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
for sample in samples:
    if "GGH" not in sample.Name :
	continue
    if "GGH35" in sample.Name :
        continue
    if "GGHmmtt40" in sample.Name :
        continue
        #job is already created : sample.MakeJobs( 20 , "%s/%s" % (OutPath24June , prefix) )
    #    print sample.Name 
    #else:
    sample.MakeJobs( 15 , "eos/cms/store/user/%s/%s/%s" % (GetUserName(), "JERSystBatch" , "out" ) ) 

    ss = ExtendedSample(sample)
    #export EOS_MGM_URL=root://eosuser.cern.ch
    #eosmount eos_cb
    ss.fhadd("./JERSystBatch/")
