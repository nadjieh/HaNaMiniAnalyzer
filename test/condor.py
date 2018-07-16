#!/usr/bin/env python
nFilesPerJob=2
import sys
import getpass
user = getpass.getuser()
if not len(sys.argv) == 3 :
    print "exactly two options are needed : "
    print "%s [working dir] [output dir on eos]" % (sys.argv[0])
    exit()

prefix = "out"
OutPath = "eos/cms/store/user/%s/%s/" % (user, sys.argv[2] )

from SamplesPU.Samples import MINIAOD as samples
for sample in samples:
    sample.MakeJobs( nFilesPerJob , "%s/%s" % (OutPath , prefix) )

import os
from shutil import copy

workingdir = sys.argv[1]
while os.path.isdir( "./%s" % (workingdir) ):
    workingdir += "_"
os.mkdir( workingdir )

from subprocess import call
call(["voms-proxy-init" , "--out" , "./%s/.x509up_u%d" % ( workingdir , os.getuid()) , "--voms" , "cms" , "--valid" , "1000:0"])


file_sh = open("%s/Submit.sh" % (workingdir) , "w" )


for sample in samples:
    if not sample.Name.count("SingleNeutrinoTuneCP"):
        continue

    os.mkdir( "%s/%s" % (workingdir , sample.Name) )
    copy( "SetupAndRun.sh" , "./%s/%s" % (workingdir , sample.Name) )

    file = open("%s/%s/Submit.cmd" % (workingdir , sample.Name) , "w" )
    print >> file, "executable              = %s/%s/%s/SetupAndRun.sh" % (os.getcwd() , workingdir , sample.Name)
    print >> file, "output                  = $(ClusterId)_$(ProcId).out"
    print >> file, "error                   = $(ClusterId)_$(ProcId).err"
    print >> file, "log                     = $(ClusterId)_$(ProcId).log"
    print >> file, '+JobFlavour             = "tomorrow"'
    print >> file, "environment             = CONDORJOBID=$(ProcId)"
    print >> file, "notification            = Error"
    print >> file, ""
    print >> file, "arguments               = %(vomsaddress)s %(scram)s %(cmsver)s %(gitco)s %(sample)s %(out)s %(outdir)s %(nFilesPerJob)d" % { 
        "vomsaddress":"%s/%s/.x509up_u%d" % (os.getcwd() , workingdir , os.getuid()) ,
        "scram":os.getenv("SCRAM_ARCH") ,
        "cmsver":os.getenv("CMSSW_VERSION"),
        "gitco":"HamedPU" ,
        "sample":sample.Name ,
        "out":prefix,
        "outdir":OutPath,
        "nFilesPerJob":nFilesPerJob
        }
    print >> file, "queue %d" % (len(sample.Jobs))

    print >> file, ""

    file.close()

    print >> file_sh, "cd %s" % (sample.Name)
    print >> file_sh, "condor_submit -batch-name %s Submit.cmd" % (sample.Name)
    print >> file_sh, "cd .."


print "to submit the jobs, you have to run the following commands :"
print "cd %s" % (workingdir)
print "source Submit.sh"
file_sh.close()



