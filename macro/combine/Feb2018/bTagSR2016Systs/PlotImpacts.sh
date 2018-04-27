#! /bin/bash


read -e -p "Please enter the CMSSW directory with Combine tools (plotImpacts.py should be also available there) :" CMSSWDir
eval CMSSWDir=$CMSSWDir
cd "${CMSSWDir}"
eval `scram runtime -sh`
cd -

mkdir $1
cd $1
text2workspace.py ../$1.txt -m 40 -o ./$1.root

# combine -M MultiDimFit --saveWorkspace -t -1 --expectSignal 1 -m 40 ./$1.root
# https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWG/SWGuideNonStandardCombineUses#Nuisance_parameter_impacts

combineTool.py -t -1 --expectSignal=1 -M Impacts -d $1.root -m 40 --doInitialFit --robustFit 1 --rMin=0 --rMax=20 --X-rtd ADDNLL_RECURSIVE=0 > InitialFitOut.txt
combineTool.py -M Impacts -d $1.root -m 40 --robustFit 1 --doFits --parallel $2 --X-rtd ADDNLL_RECURSIVE=0
combineTool.py -M Impacts -d $1.root -m 40 -o impacts.json --X-rtd ADDNLL_RECURSIVE=0
plotImpacts.py -i impacts.json -o impacts

