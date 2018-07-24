executable              = /afs/cern.ch/user/h/hbakhshi/work/Hamb/CMSSW_8_0_26_patch1/src/Haamm/HaNaMiniAnalyzer/macro/combine/Unblinding/MMTTIncluded/modelMODEL/tanbetaTANBETA/runOnLxbatch.sh
output                  = $(ClusterId)_$(ProcId).out
error                   = $(ClusterId)_$(ProcId).err
log                     = $(ClusterId)_$(ProcId).log
+JobFlavour             = "tomorrow"
environment             = LSB_JOBINDEX=$(ProccIndex)
notification            = Error

queue ProccIndex in MASSINDICES
