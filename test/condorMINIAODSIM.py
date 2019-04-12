#!/usr/bin/env python
nFilesPerJob=5
import sys
import getpass
user = getpass.getuser()
if not len(sys.argv) == 3 :
    print "exactly two options are needed : "
    print "%s [working dir] [output dir on eos]" % (sys.argv[0])
    exit()

prefix = "Premix_step1"
OutPath = "eos/cms/store/user/%s/%s/" % (user, sys.argv[2] )

from Samples80.Samples import MiniAOD80Samples as samples
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


os.mkdir( "%s" % (workingdir ) )
copy( "SetupAndRunMiniAODSim.sh" , "./%s" % (workingdir) )
    
file = open("%s/Submit.cmd" % (workingdir ) , "w" )
print >> file, "executable              = %s/%s/SetupAndRunMiniAODSim.sh" % (os.getcwd() , workingdir )
print >> file, "output                  = $(ClusterId)_$(ProcId).out"
print >> file, "error                   = $(ClusterId)_$(ProcId).err"
print >> file, "log                     = $(ClusterId)_$(ProcId).log"
print >> file, '+JobFlavour             = "tomorrow"'
print >> file, "environment             = CONDORJOBID=$(ProcId)"
print >> file, "notification            = Error"
print >> file, "request_cpus            = 4"
print >> file, 'requirements            = (OpSysAndVer =?= "SLCern6")'
print >> file, ""
print >> file, "arguments               = %(vomsaddress)s %(scram)s %(cmsver)s %(gitco)s %(sample)s %(out)s %(outdir)s %(nFilesPerJob)d" % { 
    "vomsaddress":"%s/%s/.x509up_u%d" % (os.getcwd() , workingdir , os.getuid()) ,
    "scram":"slc6_amd64_gcc530" ,
    "cmsver":"CMSSW_8_0_21" ,
    "gitco":"80X_201705" ,
    "sample":"ALL" ,
    "out":prefix,
    "outdir":OutPath,
    "nFilesPerJob":nFilesPerJob
    }
print >> file, "queue %d" % (120)
print >> file, ""
  
file.close()

print >> file_sh, "condor_submit -batch-name ALL Submit.cmd"


print "to submit the jobs, you have to run the following commands :"
print "cd %s" % (workingdir)
print "source Submit.sh"
file_sh.close()



