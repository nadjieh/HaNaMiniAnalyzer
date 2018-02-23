# HaNaMiniAnalyzer
This package is designed to read MiniAOD files and produce plots and ntuples.
For using it, one needs to compile it as a package in CMSSW. This version can be compiled using CMSSW_8_0X. It should be cloned into
a directory named Haamb.

```
cmsrel CMSSW_8_0_26_patch1
cd CMSSW_8_0_26_patch1/src
mkdir Haamb
cd Haamb
git clone -b 80X_201705 https://github.com/nadjieh/HaNaMiniAnalyzer 
cd HaNaMiniAnalyzer
scram b -j 4
```

Basic files of the package is located in the [src](src), [python](python) and [include](include) directories.
Currently one plugin is availabel in [TreeHamb.cc](plugins/TreeHamb.cc).
One can read and learn how these tools are designed to facilitate reading MiniAOD.

Information about how to run this package can be found in [test](test) directory
