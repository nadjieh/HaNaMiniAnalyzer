executable              = /afs/cern.ch/user/h/hbakhshi/work/Hamb/HigCadiDatacards/trunk/cadi/HIG-18-011/Unblinded/runOnLxbatch.sh
output                  = $(ClusterId)_$(ProcId).out
error                   = $(ClusterId)_$(ProcId).err
log                     = $(ClusterId)_$(ProcId).log
+JobFlavour             = "tomorrow"
environment             = LSB_JOBINDEX=$(ProcId)
notification            = Error

arguments               = paperv4_condor
queue 85
