#! /bin/bash
cd /afs/cern.ch/work/a/ajafari/HAMB/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/macros/Feb2018/bTagSR2016Systs
if [ ! -z "$LSB_JOBINDEX" ];
then
    echo $LSB_JOBINDEX
    export MASS=`echo "$LSB_JOBINDEX * 0.5 + 19.5" | bc`
else
    export MASS=35
fi
echo $MASS
eval `scramv1 runtime -sh`
combine -M Asymptotic -m $MASS bTagSR2016Systs.txt --run=blind

#bsub -q 1nh -J "HambCombine[1-85]" -o HambCombine%I.out `pwd`/runOnLxbatch.sh
