#! /usr/bin/env python3.6
# coding: utf-8

# ## General remark
# This programme runs slow on CERN SWAN, especially when extracting the data from the lumi files (tarfiles). It is much more efficient to copy the Massi files of interesting fills to a local directory, extract them and then take this code and run it locally on a computer. (More than a factor 10 difference during extraction).
# 
# This programme takes data from the lumi files and creates a pandas dataframe. Raw data from the Massi files and the processed data frame data are cached to disk
# This dataframe is written to disk as a cache file. If for a given fill the cachefile is found the slow extraction is not repeated. If, for some reason, you want to redo the extraction you have to delete the cache files from disk beforehand.



import pandas as pd
import sys
import os
import glob
import re
import plotly.express as px
import json
import urllib
import tarfile
import pickle
import argparse

def extract_messi_file( year , fillno):
    # Massi files are available on eos:
    #/eos/project/l/lpc/public/MassiFiles/<year>/measurements/<experiment>/<lumi|lumiregion|beamgas> 
    # we need the lumi files
    # Documentation on the contents and the file naming conventions can be found at
    # https://lpc.web.cern.ch/MassiFileDefinition_v2.htm
    
    #Commented out since we do not want to decode the csv files in order to get the 
    # Bunch arrays of the filling scheme. It is easier to generate the bunch arrays
    # on the LPC website and copy the into the SWAN notebook.
    #
    # Retrieve the filling scheme from the LPC webspace via the provided API
    #urlbase = "http://lpc.web.cern.ch/lpc/cgi-bin/schemeInfo.py"
    #parameters = "?fill=" + str(fillno) + "&fmt=json"
    #schemeurl = urlbase + parameters

    MassiBaseDir = os.path.join("/eos/project/l/lpc/public/MassiFiles/", str(year), "measurements/CMS/lumi")
    MassiData = os.path.join( MassiBaseDir, str(fillno)+".tgz")

    # ### Massi files
    # The Massi files are contained in a tgz file on eos. This code opens the 
    # tarfile and extracts the contents to the local directory. Since extracting
    # the files is very slow we do this once and keep the files in the working 
    # directory until the user deletes them by hand. The files for a given fill 
    # can be found in the directory with the corresponding fill number as name. 
    # If such a directory already exists it is assumed to contain the massi 
    # files and the extraction is NOT repeated. Hence if you want to force a
    # a fresh extraction of the files, delete the directory with the fillnumber as
    # a name.

    # open the tgz file with the massi files and extract them to the file system.
    # File extraction is super slow on Swan. This is why we do it here in a 
    # dedicated cell: the data is then on disk an can be accessed faster by
    # the following cells. If you do not have time to wait for this you are 
    # better off to copy the Massi files by hand and extract them by hand...
    #
    # If a directory with the fillnumber as the name already exists it is assumed
    # that the extracted data is already present and the extraction is skipped.

    if ( os.path.isdir( str(fillno))) :
        print("Fill " + str(fillno) + " seems to be extracted already. Skipping extraction")
    else:
        print( "Extracting Massi files for fill " + str(fillno))
        massi = tarfile.open( MassiData )
        massi.getnames()
        regex = str(fillno)+'/'+str(fillno)+'_lumi_\d+_CMS.txt'
        first = True # some extra work to be done for the first file, see below
        for filename in massi.getnames():
            #print(filename)
            if re.match( regex, filename):
                io=massi.extract(filename)
    

def process_messi_file(fillno , year):
    # ### Massi file processing
    # Massi files contain the instantaneous bunch luminosity for each bunch. Each line in the file has a timestamp corresponding ot the lumi "snapshot". Granularity is lumi-section (I think).
    # 
    # The detailed description of the contents of the Massi files can be found here:
    # 
    # <a href="https://lpc.web.cern.ch/MassiFileDefinition_v2.htm"> https://lpc.web.cern.ch/MassiFileDefinition_v2.htm </a>
    # 
    # Data is extracted from the first file on the disk and the 10th last lumi section is identified. Now from all files data of this point in time is extracted and inserted into a pandas dataframe. This dataframe is saved to disk as a cache. 
    # 
    # This processing is only done if no dataframe cachefile for this fill is found.
    # If a dataframe for this fill already exists in the working directory 
    # this processing step is skipped since. If you want to redo the processing
    # delete the dataframe file by hand

    cachename = "{0}/df_{0}.pkl".format( fillno )
    df = None
    if os.path.isfile( cachename ): 
        print( "Found a cached dataframe for fill " +str(fillno) + ". Just loading the cache file.")
        df = pd.read_pickle( cachename )
    else:
        extract_messi_file( year , fillno )
        print("Processing Massi files for fill " + str(fillno))
        filenames  = glob.glob(str(fillno) + "/*")
        #print(filenames)
        reftime = 0
        ifc = 0 # debug counter
        darr = []
        first = True # some extra work to be done for the first file, see below
        for filename in filenames:
            #print(filename)
            fd = open(filename,"r")

            # decode the bxid from the filename
            mo = re.match(str(fillno)+"/"+str(fillno)+"_lumi_(\d+)", filename)
            bxid = (int( mo.group(1) ) - 1 ) / 10

            if first:
                # need to find out how long the file is. Take the 10th lumisection at the 
                # end of the file for taking the snapshop at the end of the file.
                lix = 0
                linearr = [] 
                for row in fd:
                    #print (row)
                    toks = str(row).split()
                    linearr.append(toks)
                    lix += 1

                lix -= 10 # 10th last timestamp
                time = int(float(linearr[lix][0])) # time stamp
                stab = int(float(linearr[lix][1])) # stable beam flag
                lumi = float(linearr[lix][2]) # lumi
                reftime = time
                darr.append( [bxid, time, lumi] )
                #print(lix,time,stab,lumi)
                if stab != 1:
                    print("the 10th last lumisection does not have the stable beams flag set. Bailing out...")
                    sys.exit()
                first = False
                print( "decoding line " + str(lix))
                continue
            ix = 0
            try:
                for row in fd:
                    ix += 1
                    if ix == lix:
                        # we found the reference line
                        # check the time stamp
                        toks = str(row).split()
                        #print(toks)
                        time = int(float(toks[0])) # time stamp
                        stab = int(float(toks[1])) # stable beam flag
                        lumi = float(toks[2]) # lumi
                        row = [bxid,time,lumi]
                        #print("row ", row)
                        darr.append( [bxid, time, lumi] )
                        if stab != 1:
                            print("the 10th last lumisection does not have the stable beams flag set. Bailing out...")
                            sys.exit()
                        break
            except:
                print ("ioerror ",filename)
            ifc += 1
            fd.close()
            if (ifc % 100) == 0:
                print(ifc,filename)

        df = pd.DataFrame( darr,columns=["bxid","time","lumi"] )
        df.to_pickle( cachename )
    return df

def get_filling_schemas(fillno, year):
    # ### Retrieving the filling scheme
    # For the steps below a simple version of the filling scheme data is required. Filling schemes in the last years of Run 2 have been produced with the Filling Scheme editor on the LPC website. They are accessible for everyone and can be downloaded. 
    # This programme uses a simple format of the filling scheme in the form of bunch arrays (1 array per beam with 3564 entries corresponding to the 3564 possible collisions in CMS ("slots"). A '1' in the array means a bunch is filled, a '0' means the bunch is not filled. 
    # 
    # To retrieve the bunch arrays in json format, one has to open the Filling Scheme editor at  
    # <a href="https://lpc.web.cern.ch/SchemeEditor.htm">https://lpc.web.cern.ch/SchemeEditor.htm</a>  
    # Enter "lpc" as used name and click on load (or hit "return"). The scheme for Fill 7056 is named 
    # 25ns_2556b_2544_2215_2332_144bpi_20inj_800ns_bs200ns_v3
    # and can be found under the '2018' category. After clicking on the scheme it will be loaded into the editor and can be inspected or modified. (Saving requires a password, of course.)
    # Further down on the page there is a button to download the bunch arrays of the scheme. The retrieved file should be renamed to bunchArrays_{fillno}.json and uploaded to the directory where the code for this notebook is saved. 
    # 
    # In case other fills should be analysed the association of the fill number to the filling scheme can be found in the table <a href="https://lpc.web.cern.ch/cgi-bin/fillTable.py">https://lpc.web.cern.ch/cgi-bin/fillTable.py</a>.
    # 
    # In case a larger amount of fills should be analysed we should probably put more automisation into this software (the scheme could be automatically retrieved and analysed from the fill number).
    # 
    # ### Analysis of fill 7056
    # After having inspected the bunch intensity display towards the end of the fill in the LHC logbook for fill 7056 it became apparent that the three bumps in the bunch lumi distribution is due to intensity variations in the bunches. The intensity display suggests that there are three different regions of bunches within an injection. The code below tries to identify these regions and give bunches from these regions a code number so that in a histogram the bunches can be distinguished by color. 
    # 
    # Three regions are identified  
    # code 2  :  bunches in the first 22 bxid slots of the injection  
    # code 3  :  bunches in slots 22 to 67  
    # code 5  :  bunches in slots after 67
    # 
    # Later these three classes will be color-coded in the bunch lumi histogram and it will be seen that they populate the different bumps in the histogram separately. This indicates that the bunch intensity is the origin of the bumps. It does not explain why the bunches of the three classes develop differently during the long fill. 
    # 
    # A more thorough analysis would download the bunch intensities from NXCals at the end of the fill and correlate the tree bumps with what is expected from multiplying the intensities of the colliding bunches. 
    ba = None
    with open( "bunchArrays_" + str(year) + ".json", "r" ) as bafile:
        ba = json.load( bafile )

    b1 = ba["beam1"]
    b2 = ba["beam2"]

    return b1,b2

def train_schema(beaminfo):
    ret = [0]*3564
    # establish where the bunches are in the train:
    # classify the first 8 after a injection gap and after a batch gap
    pos = 0
    ec = 0  # emtpy counter: counts the empty bunch crossing in a row 
            # to distinguish between injection spacing and batch spacing
    batchc = 0
    wasbgap = False   # True if there was a batch gap
    wasigap = False   # True if there was a injection gap
    code = 0          # counts the batches in the injection (bad name... shoud be ibatch)
    batchpos = 0      # indicates the position in the batch
    for ix,bx in enumerate(beaminfo):
        if bx != 0:
            if not wasbgap and not wasigap:   # this is the first bunch after a gap
                batchpos = 1
                if ec > 10:                   # A large gap (>250ns) indicates a injection gap
                    wasigap = True
                    code = 1 # first batch
                elif ec > 1:                  # A small gap indicates a gap between SPS batches
                    wasbgap = True
                    code += 1  # next batch
            batchpos += 1
            pos += 1
            ec = 0
        else:
            ec += 1
            pos = 0
            batchpos = 0
            wasbgap = False
            wasigap = False

        icode = 0
        if code == 1:
            if batchpos <= 22:
                icode = 2*code
            else:
                icode = 2*code + 1
        elif code == 2:
            if batchpos <= 20:
                icode = 2*code
            else:
                icode = 2*code + 1
        elif code == 3:
            if batchpos <= 12:
                icode = 2*code
            else:
                icode = 2*code + 1


        if icode == 4:
            icode = 3
        if icode > 5:
            icode = 5
        ret[ix] = icode
    
    return ret
    # code 2: batch 1 position <= 22 in batch
    # code 3: batch 2 position > 22 or batch 2 position <= 20
    #          i.e. injection bunch 22 ... 67
    # code 5: injection position 68 -> 144    

    # Injection positions:  1-22    22-67    68-144


    # ### Analysis of bunch classes
    # First it was assumed that the three different peaks of the bunch lumi histogram could be caused by various classes of bunches which collide or don't collide in LHCb and therefore burn of faster or less fast. In order to find a possible correlation the bunches are divided into various classes. These classes are encoded with a 3 bit code:
    # 
    # | bit | meaning |
    # |-----|-------- |
    # | 0 | collision in IP 1&5 |
    # | 1 | collision in IP 2 |
    # | 2 | collision in IP 8 |
    # 
    # Each collision in CMS involves 2 bunches. They might belong to different classes due to the asymmetric position of LHCb and ALICE wrt CMS. Therefore for every bunch crossing a number with 2 digits is determined. The first (most significant) digit gives the bitcode for the bunch of Beam 1 and the second digit the bitcode for the bunch of Beam 2. As an example the code combination 3 5 means: Beam 1 -> code 3 (binary 0011) -> bits 0 and 1 set to 1 -> collisions in IP 1 & 5 & 2
    # Beam 2 -> code 5 (binary 101) -> bits 1 and 2 set -> collisions in IP 1 & 5 & 8.

    # In[132]:


    ## establish where the bunches are in the train: go until 48 in groups of 8
    #pos = 0
    #posb1 = [0]*3564
    #posb2 = [0]*3564
    #
    #for ix,bx in enumerate(b1):
    #    if bx != 0:
    #        pos += 1
    #    else:
    #        pos = 0
    #    posb1[ix] = int(pos/4)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( '-f' , dest='fill' , default=7056 , help='fill number' , type=int )
    parser.add_argument( '-y' , dest='year' , default=2018 , help='year' , type=int , choices=[2016,2017,2018] )
    opt = parser.parse_args()
    
    #extract_messi_file( opt.year , opt.fill )
    df = process_messi_file(opt.fill , opt.year)
    
    # A simple histogramme showing the distribution of the per bunch luminosity of the Fill. 
    # A simple histogram of the bunch lumi at this time of the fill
    fig = px.histogram( df, x="lumi", title="Bunch lumi distribution for Fill " + str(opt.fill) )
    fig.update_layout( xaxis_title = "bunch luminosity [Hz/μb]")
    #fig.show()
    fig.write_html("{0}/bunch_lumi.html".format(opt.fill))
    

    b1,b2 = get_filling_schemas(opt.fill , opt.year)
    posb1 = train_schema( b1 )
    posb2 = train_schema( b2 )




    cmscol = 0
    lhcbcol = 0
    alicecol = 0
    b1cl=[0]*3564
    b2cl = [0]*3564

    for ix,bx in enumerate(b1):
        if bx == 0:
            continue
        if b2[ix] != 0:
            cmscol += 1
            b1cl[ix] |= 1
            b2cl[ix] |= 1
        ix2 = ( ix+891 ) % 3564
        if b2[ix2] != 0 :
            alicecol += 1
            b1cl[ix] |= 2
            b2cl[ix2] |= 2
        ix2 = (ix-894) % 3564
        if b2[ix2] != 0:
            lhcbcol += 1
            b1cl[ix] |= 4
            b2cl[ix2] |= 4

    print ("collisions IP1, 2, 8 ", cmscol, alicecol, lhcbcol )
    #print( b1cl)
    #print (b2cl)

    df["b1cl"] = 0
    df["b2cl"] = 0
    df["b12cl"] = 0
    df["posb1"] = 0

    df.set_index( "bxid", inplace=True )
    df.sort_index( inplace=True )
    for index,row in df.iterrows():
        iindex = int(index)
        df.at[index,'b1cl'] = b1cl[iindex]
        df.at[index,'b2cl'] = b2cl[iindex]
        df.at[index,'b12cl'] = 10*b1cl[iindex]+b2cl[iindex]
        df.at[index,'posb1'] = posb1[iindex]
    
    # This code counts the number of bunches in the various classes. It can be cross checked against the numbers coming from the filling scheme editor, to be sure that the code is not buggy.
    # now check the classes. This code is only here to check if we did not do a mistake above
    # The numbers which will be printed out can be compared to the numbers in the LPC
    # Filling Scheme editor. If they correspond it is unlikely that the code above is buggy.
    classesb1 = [0]*8
    classesb2 = [0]*8
    for index,row in df.iterrows():
        iclass = int( row['b1cl'] )
        classesb1[iclass] += 1
        iclass = int( row['b2cl'] )
        classesb2[iclass] += 1

    print ("classes b1", classesb1)    
    print ("classes b2", classesb2)
    # check end


    # ### Bunch class histogram
    # This histogram plots the bunch lumi of the various collisions in CMS. The colors code the possible bunch class combinations. It can be seen that all bunch classes are equally distributed over the three bumps and hence the assumption that the collisions in LHCb could play a role in the distribution of the bunch luminosity is not correct.

    # plot the histogram
    fig = px.histogram( df, x="lumi", color="b12cl", title="Bunch luminosity for various bunch classes" )
    fig.update_layout(xaxis_title="bunch luminosity [Hz/μb]")
    #fig.show()
    fig.write_html("{0}/bunch_lumi2.html".format(opt.fill))
    
    fig=px.histogram( df, x="lumi", color="posb1", title="Bunch lumi for bunches of different positions in the injection" )
    fig.update_layout( xaxis_title="bunch luminosity [Hz/μb]")
    #fig.show()
    fig.write_html("{0}/bunch_lumi3.html".format(opt.fill))




if __name__ == "__main__":
    main()
