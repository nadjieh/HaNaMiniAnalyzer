HaNaMiniAnalyzer/test
=====================

## Configuring the environment
To run the ntuple producer, one has to produce the list of samples and some basic configuration. These part has to be repeated 
when a new set of samples is available.

### Producing the list of samples and files
For each set of new samples, one has to make a new directory including a python file, similar to what can be found in [Samples80/Samples.py](test/Samples80/Samples.py).
First lines should be repeated. For each sample, we have to define a Sample object and add it to the list object. Don't forget to 
commit and push all the changes.

```
DoubleMuB80 = Sample("DoubleMuB" , 0 , False ,  "/DoubleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD" )
MiniAOD80Samples.append( DoubleMuB80 )
```

Here is the description of the parameters given to the Sample class constructor :

```
1 : Sample Name ("DoubleMuB")
2 : Cross section : 0 for data
3 : If this sample has negative weeights :
4 : Address of the sample in DAS
```

When the `Samples.py` is available, the file list of each sample should be produced. The idea is to have a list of all the files for each
sample in a file named `SampleName.list`. Some example can be found [here](test/Samples80/DYJetsLowMass.list). There are several ways to produce these files


#### Manually producing the file
One way is to use manually the ADS website and copy the file names to a file. It can be done using the following command :
```
das_client --query="files dataset='dataset path in das'" --limit=0 > DataSetName.list
```

#### Automatic
Some codes has been implemented in Haamm.HaNaMiniAnalyzer.Sample to retreive the list of the files. If you run 
```
python Sample.py
```

and if you are lucky enough, it fetches the list of files from das and produce the files automatically. If it doesn't work, go back to the 
first approach and repeat the command for every sample


### Setup directory

A setup directory, should contain the needed the scale factors and json files. You can find a sample directory [test/Setup80](test/Setup80).
The content of these directory may change if new scale factors and corrections are needed to be applied. In that case the basic codes
and classes also should be updated.

For the moment, the following files are needed :

#### b-tagging scale factors :
a file named `CSVv2.csv` which contain the latest CSVv2 scale factors should be there

#### JSON
a file name `JSON.txt` which is the latest json file of the ceretified lumi-sections should be copied here

#### MuonIDSF.root and MuonIsoSF.root
Two standard files provided by the muon group which include iso/id scale factors.

#### DiMuonHLTs.root
Di muon trigger weights

#### pileUpData.root and pileUpMC.root
the shape of the pileup in MC and data to perform pu reweighting

#### MCJetPtResolution.txt and MCJetSF.txt
Two txt files provided by JET POG for JET scale factors

## Running the tool
When the `sample` and `setup` directories are ready, one needs to produce a config file to run over the new samples with the new configuration.
A sample config file can be found [here](test/Hamb_cfg.py). Let's review these file, line by line :

### [Lines 1 to 55](https://github.com/nadjieh/HaNaMiniAnalyzer/blob/80X_201705/test/Hamb_cfg.py#L1-L55)
Standard modules from CMSSW that you want to run are loaded here in to the process. You can load as much as module you would like to run

### [Lines 57](https://github.com/nadjieh/HaNaMiniAnalyzer/blob/80X_201705/test/Hamb_cfg.py#L57)
The basic configuration of the analysis is loaded here. Muon and b-jet criteria to cut on are set here.

### [Lines 60 to 89](https://github.com/nadjieh/HaNaMiniAnalyzer/blob/80X_201705/test/Hamb_cfg.py#L60-L89)
The input parameters are defined here. The idea is that one can configure the job to run on a specific sample. It divides the sample files
into bunches of `nFilesPerJob` files per job and with option `job` one can tell which bunch of files should be used.
the important parameters are :

#### sample : sample name
#### nFilesPerJob : number of files per job
#### job : job number

### [Lines 92 to 122](https://github.com/nadjieh/HaNaMiniAnalyzer/blob/80X_201705/test/Hamb_cfg.py#L92-L122)
These lines are the part that select the files on which it should run. One needs to give the correct path of the samples file here and also the 
setup directory here.

### The rest of the file
It creates the path and endpath'es to run on the events. It has different parts for data and MC. So one can easily configure how it runs 
separately for data and MC.

## Ready to run
Now, one can test how it runs on. 
```
cmsRun <config_file_name.py> sample=<sample_name> nFilePerJob=1 job=0
```
Please test if it runs properly for data and MC samples.


## Ready to submit on the lxbatch
There is a script to produce all the environment from scratch and run the job with the given parameters. You can find it [here](https://github.com/nadjieh/HaNaMiniAnalyzer/blob/80X_201705/test/SetupAndRun.sh)

In the first 20 lines of that file, it creates an empty CMSSW directory, then clones the package from github and compile it. One has to add any extra package which is needed to run here. As an example, here the `git-merge-topic` has been called several times.

Then it calls the `cmsRun Hamb_cfg.py` command and configure it using the input arguments.

After that, it tries several times to copy the output files to the `eos` directory of the user. The copy part should be adapted it you want to copy the output file somewhere else.

## How to submit the jobs into lxbatch
There is a tool called [`lxbatch.py`](lxbatch.py) to produce jobs. One has to edit it and mention the `samples.py` file that wants to loop over.

It only needs two parameters : 

```
python lxbatch.py <eos_dir_to_copy_output_files> <current_dir_to_store_configurations>
```

Running this script, a directory is created in the test directory. There, you can find a file called `submit.sh`. Running it, all the jobs are submitted to the lxbatch.


## Monitor the job outputs and re-run for the failed jobs
There is a hard-coded parameter in the [lxbatch.py](https://github.com/nadjieh/HaNaMiniAnalyzer/blob/80X_201705/test/lxbatch.py#L3) file. It is called CheckFailedJobs. If it is set to `True`, lxbatch.py looks for the output of the previous jobs in `eos` and if one file is missing, add it to the list of jobs to run over them again.

## Merge the ouput files
A script is availabel to merge the output files. It can be found at [test/hadd.py](test/hadd.py).


# This documentation is not complete, please contact developers if more information is needed















