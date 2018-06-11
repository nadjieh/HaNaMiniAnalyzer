#! /bin/bash
if [ ! -z "$LSB_JOBINDEX" ];
then
    echo $LSB_JOBINDEX
    export MASS=`echo "$LSB_JOBINDEX * MASSSTEP + 20 - MASSSTEP" | bc`
else
    export MASS=35
fi
echo $MASS
export MASS=`printf "%.2f" $MASS`
echo $MASS

cd /afs/cern.ch/user/h/hbakhshi/work/tHq/CMSSW_8_1_0/
eval `scramv1 runtime -sh`

cd /afs/cern.ch/user/h/hbakhshi/work/Hamb/CMSSW_8_0_26_patch1/src/Haamm/HaNaMiniAnalyzer/macro/combine/Unblinding/MMTTIncluded/modelMODEL/tanbetaTANBETA/
combine -M AsymptoticLimits -m $MASS --X-rtd ADDNLL_RECURSIVE=0 --cminDefaultMinimizerStrategy 0 Mass$MASS.txt

#bsub -q 1nh -J "HambCombine[1-85]" -o HambCombine%I.out `pwd`/runOnLxbatch.sh
