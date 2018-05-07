#! /bin/bash
cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_8_1_0/
eval `scramv1 runtime -sh`

if [ ! -z "$LSB_JOBINDEX" ];
then
    echo $LSB_JOBINDEX
    export MASS=`echo "$LSB_JOBINDEX * 0.5 + 19.5" | bc`
else
    export MASS=35
fi
echo $MASS
cd /afs/cern.ch/user/h/hbakhshi/work/Hamb/CMSSW_8_0_26_patch1/src/Haamm/HaNaMiniAnalyzer/macro/combine/Feb2018/bTagSR2016Systs/
combine -M AsymptoticLimits -m $MASS CombinedCard.txt  --X-rtd ADDNLL_RECURSIVE=0 --cminDefaultMinimizerStrategy 0 --run=blind

#bsub -q 1nh -J "HambCombine[1-85]" -o HambCombine%I.out `pwd`/runOnLxbatch.sh
