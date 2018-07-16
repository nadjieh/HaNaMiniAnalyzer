#!/usr/bin/env python
from ROOT import gROOT
gROOT.SetBatch(True)

from SamplesPU.Samples import *
samples = None
runOnOutsOfAnotherJob = False
if runOnOutsOfAnotherJob :
    samples = skimmedSamples1
else :
    samples = MINIAOD

for sample in samples:
    #if sample.Name in [s.Name for s in sampleswith24juneonly]:
        #job is already created : sample.MakeJobs( 20 , "%s/%s" % (OutPath24June , prefix) )
    #    print sample.Name 
    #else:
    sample.MakeJobs( 4 , "/eos/cms/store/user/%s/%s/%s" % (GetUserName(), "MayPU" , "out" ) ) 
    # sample.ParentSample.MakeJobs( 3 , "root://eoscms//eos/cms/store/user/%s/%s/%s" % (GetUserName(), "Moriond17" , "tree" ) ) 

    #print [j.Output for j in sample.Jobs]

from Haamm.HaNaMiniAnalyzer.ExtendedSample import *
for sample in samples:
    ss = None
    skip = True
    for sname in [ "SingleMuC" , "SingleMuD" ]: #"ZmuMuM" , "NuGunM" ]:,
        if sname in sample.Name :
            print "skipping ", sample.Name
            skip = False
    if skip :
        continue

    if False : #sample.Name in ["ttH" , "Signal"]:
        print "using parent for " + sample.Name
        ss = ExtendedSample( sample.ParentSample )
    else :
        ss = ExtendedSample(sample)
    #export EOS_MGM_URL=root://eosuser.cern.ch
    #eosmount eos_cb
    ss.fhadd("/eos/user/h/hbakhshi/Personal/Projects/PU/May/" , True ) #"/eos/user/h/hbakhshi/Personal/Projects/PU/02MarchPPD2/" , True)
