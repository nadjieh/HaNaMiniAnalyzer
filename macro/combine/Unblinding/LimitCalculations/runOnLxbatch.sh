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
cd /afs/cern.ch/user/h/hbakhshi/work/Hamb/HigCadiDatacards/trunk/cadi/HIG-18-011/Unblinded/$1
combine -M AsymptoticLimits -m $MASS CombinedCard.root --X-rtd ADDNLL_RECURSIVE=0 --cminDefaultMinimizerStrategy 0

#dir=
#bsub -q 1nh -J "Hamb$dir[1-85]" -o $dir/HambCombine%I.out `pwd`/runOnLxbatch.sh $dir

