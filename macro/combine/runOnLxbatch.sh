#! /bin/bash
cd /afs/cern.ch/work/a/ajafari/HAMB/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/macros
if [ ! -z "$LSB_JOBINDEX" ];
then
    echo $LSB_JOBINDEX
    export MASS=`echo "$LSB_JOBINDEX * 0.5 + 20" | bc`
    echo $MASS
fi
eval `scramv1 runtime -sh`
combine -M Asymptotic -n Br  -m $MASS hamb_shape_Br_ws.txt
combine -M Asymptotic -n SigmaBr -m $MASS hamb_shape_SigmaBr_ws.txt

#bsub -q 1nh -J HambCombine[0,85] -o HambCombine%I.out runOnLxbatch.sh