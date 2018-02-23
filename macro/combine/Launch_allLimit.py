#!/usr/bin/env python
#Usage: python Launch_allCP ConfigFile
#example: python Launch_allCP zbbConfig
#combine -M Asymptotic hamb_shape_25_ws.txt -m 25 --run=blind

import urllib
import string
import os
import sys
import LaunchOnCondor
import glob

BrSignal = sys.argv[1]

dir_plot = {
  "ajafari": os.getcwd()+"/",
}


combine = "/nfs/user/ajafari/work/CMSSW_7_1_5/bin/slc6_amd64_gcc481/combine"

        
README = "Individual fit for 25-65 GeV with 250 MeV step (V5) \n"



dir = dir_plot[os.environ["USER"]]
string_mode='HalfGeV_'+BrSignal+'_VPol2'

os.system('mkdir '+dir+string_mode)
f = open(dir+string_mode+'/README.txt', 'w')
f.write(README)
f.close()
os.system('mkdir '+dir+string_mode+'/'+string_mode)
LaunchOnCondor.Jobs_FinalCmds.append('mv higgsCombineTest.Asymptotic.mH*.root '+dir+string_mode+'/'+string_mode+'/ \n')
FarmDirectory = dir+"FARM_"+string_mode
JobName = "limit_list_"
LaunchOnCondor.SendCluster_Create(FarmDirectory, JobName)
print "after creation"

datacard = "hamb_shape_"+BrSignal+"_ws.txt"
for num in range(0,25):
    mass = 25 + 0.5*num
#for num in range(0,40):
#    mass = 25. + num
#for num in range(0,20):
#    mass = 25. + 2*num
#for num in range(0,160):
#    mass = 25. + 0.25*num
    LaunchOnCondor.SendCluster_Push(["BASH", combine+" -M Asymptotic "+os.getcwd()+"/"+datacard+" -m "+str(mass)])

LaunchOnCondor.SendCluster_Submit()
