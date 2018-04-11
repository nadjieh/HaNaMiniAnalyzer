#! /bin/bash
if [ ! -z "$LSB_JOBINDEX" ];
then
    echo $LSB_JOBINDEX
    export MASS=$LSB_JOBINDEX
else
    export MASS=35
fi
echo $MASS

cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_7_4_7/
eval `scramv1 runtime -sh`

cd /afs/cern.ch/user/h/hbakhshi/work/Hamb/CMSSW_8_0_26_patch1/src/Haamm/HaNaMiniAnalyzer/macro/combine/Feb2018/bTagSR2016Systs_MMTTIncluded/modelMODEL/tanbetaTANBETA/
combine -M Asymptotic -m $MASS Mass$MASS.txt --run=blind

#bsub -q 1nh -J "HambCombine[1-85]" -o HambCombine%I.out `pwd`/runOnLxbatch.sh
