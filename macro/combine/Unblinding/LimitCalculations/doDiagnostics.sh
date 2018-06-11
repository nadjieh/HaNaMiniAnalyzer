#! /bin/bash


read -e -p "Please enter the CMSSW directory with Combine tools (plotImpacts.py should be also available there) :" CMSSWDir
eval CMSSWDir=$CMSSWDir
cd "${CMSSWDir}"
eval `scram runtime -sh`
cd -

mkdir $1
cd $1
ln -s $CMSSWDir/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py
text2workspace.py ../$1.txt -m 40 -o ./$1.root

# combine -M MultiDimFit --saveWorkspace -t -1 --expectSignal 1 -m 40 ./$1.root
# https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWG/SWGuideNonStandardCombineUses#Nuisance_parameter_impacts

combine -M  FitDiagnostics -d $1.root -m 40 -t -1 --expectSignal 0 --X-rtd ADDNLL_RECURSIVE=0  --cminDefaultMinimizerStrategy 0 --setCrossingTolerance 1E-6
mv fitDiagnostics.root fitDiagnostics_bonly.root
python diffNuisances.py -a fitDiagnostics_bonly.root -g plots_bonly.root

combine -M  FitDiagnostics -d $1.root -m 40 -t -1 --expectSignal 1 --X-rtd ADDNLL_RECURSIVE=0  --cminDefaultMinimizerStrategy 0 --setCrossingTolerance 1E-6
mv fitDiagnostics.root fitDiagnostics_splusb.root
python diffNuisances.py -a fitDiagnostics_splusb.root -g plots_splusb.root

