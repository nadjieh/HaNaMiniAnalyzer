#ifndef BTagWeight_H
#define BTagWeight_H

//https://github.com/nfaltermann/ST_RunII_EA/blob/master/src/DMAnalysisTreeMaker.cc
//https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods    (method 1a)

#include <vector>
#include <iostream>
#include <string>

#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondTools/BTau/interface/BTagCalibrationReader.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
using namespace std;



/*
 *
 * enum OperatingPoint {
 *     OP_LOOSE=0,
 *     OP_MEDIUM=1,
 *     OP_TIGHT=2,
 *     OP_RESHAPING=3,
 *     };
 * enum JetFlavor {
 *     FLAV_B=0,
 *     FLAV_C=1,
 *     FLAV_UDSG=2,
 *     };
 *
 */



class BTagWeight
  {
  private:
    string algo;
    int WPT, WPL, minTag, maxTag;
    int syst, minTagL, maxTagL;
    float bTagMapCSVv2[3];
  public:
    BTagWeight(string algorithm, int WPt, string setupDir, int mintag, int maxtag, double BLCut = 0.460, double BMCut = 0.800, 
	       double BTCut = 0.935, int WPl = -1, int systematics = 0, int mintagl = -1, int maxtagl = -1): 
      algo(algorithm), WPT(WPt), WPL(WPl), minTag(mintag), maxTag(maxtag), syst(systematics), minTagL(mintagl), maxTagL(maxtagl), readerExc(0),readerCentExc(0)
    {
	bTagMapCSVv2[0] = BLCut;
	bTagMapCSVv2[1] = BMCut;
	bTagMapCSVv2[2] = BTCut;
	if(WPL != -1){
		if(minTagL == -1){
			std::cout<<"At least provide the minimum number of loose-non-tight tags you want!!"<<std::endl;
			return;
		}
    		if (WPL > WPT){
		       	int tmp;
		       	tmp = WPL;
			WPL = WPT;
			WPT = tmp;
		}
	}
	Systs[0] = "central";
	Systs[-1] = "down";
	Systs[1] = "up";
	cout<< setupDir+"/"+algo+string(".csv")<<endl;
	calib = new BTagCalibration(algo /*"CSVv2"*/, setupDir+"/"+algo+string(".csv"));
	reader = new BTagCalibrationReader( (BTagEntry::OperatingPoint)WPT, "central" , {"up", "down"} );

	reader->load( *calib , BTagEntry::FLAV_B , "mujets" );
	reader->load( *calib , BTagEntry::FLAV_UDSG , "incl" );
	
	if(WPL != -1){
	  readerExc = new BTagCalibrationReader( (BTagEntry::OperatingPoint)WPL , "central" , {"up", "down"} );
	  readerExc->load( *calib , BTagEntry::FLAV_B , "mujets" );
	  readerExc->load( *calib , BTagEntry::FLAV_UDSG , "incl" );

	}

    };

  BTagWeight(string fileweights , string algorithm,  string setupDir): 
      algo(algorithm), WPT(-100), WPL(-1), minTag(-1), maxTag(-1), syst(-1), minTagL(-1), maxTagL(-1), readerExc(0),readerCentExc(0)
    {
	//for reshaping 
	Systs[0] = "central";
	Systs[-1] = "down_hfstats1";
	Systs[1] = "up_hfstats1";
	Systs[2] = "up_hfstats2";
	Systs[-2] = "down_hfstats2";
	Systs[3] = "up_lfstats1";
	Systs[-3] = "down_lfstats1";
	Systs[4] = "up_lfstats2";
	Systs[-4] = "down_lfstats2";
	Systs[5] = "up_jes";
	Systs[-5] = "down_jes";
	Systs[6] = "up_lf";
	Systs[-6] = "down_lf";
	Systs[7] = "up_cferr1";
	Systs[-7] = "down_cferr1";
	Systs[8] = "up_cferr2";
	Systs[-8] = "down_cferr2";
	Systs[9] = "up_hf";
	Systs[-9] = "down_hf";

	std::vector<string> allSystNames;
	for(auto syst_ : Systs )
	  if( syst_.first != 0 )
	    allSystNames.push_back( syst_.second );

	cout<< setupDir+"/"+algo+string(".csv")<<endl;
	calib = new BTagCalibration(algo /*"CSVv2"*/, setupDir+"/"+fileweights+string(".csv"));
	//formula: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSPhysicsObjectSchoolVertBTag#Exercise_I_applying_the_BTV_scal
	reader = new BTagCalibrationReader( BTagEntry::OP_RESHAPING, "central" , allSystNames );
	reader->load(*calib, BTagEntry::FLAV_B, "iterativefit");
	reader->load(*calib, BTagEntry::FLAV_C, "iterativefit");
	reader->load(*calib, BTagEntry::FLAV_UDSG, "iterativefit");

	/* Sanity checks
	 * std::cout<< "---- BTag WPs ----\n\t" <<bTagMapCSVv2[0] <<",\t"<<bTagMapCSVv2[1] <<",\t"<<bTagMapCSVv2[2]
	 *	 <<"\n---- WPs to select ----\n\t"<<bTagMapCSVv2[WPT]
	 *	 <<"\n---- WPs to veto ----\n\t";
	 *	 if(WPL != -1) std::cout << bTagMapCSVv2[WPL]<<std::endl;
	 *	 else std::cout << "No veto is requested" <<std::endl;
	 * End Sanity Checks
	 */
    };
    inline bool filter(int t){
	if(maxTag != -1)
		return (t >= minTag && t <= maxTag);
	else
		return (t >= minTag);
    }
    inline bool filter(int tight, int looseNonTight){
        bool OK = false;
	if(maxTag != -1)
		OK = (tight >= minTag && tight <= maxTag);
	else
		OK = (tight >= minTag);
        if(maxTagL != -1)
		OK = (OK && (looseNonTight >= minTagL && looseNonTight <= maxTagL));
	else
		OK = (OK && (looseNonTight >= minTagL));
	return OK;
    }
    float weight(pat::JetCollection jets);
    float weight(pat::JetCollection jets, int);
    float weightShape(pat::JetCollection , int);
    float weightExclusive(pat::JetCollection jetsTags);
    float TagScaleFactor(pat::Jet jet, bool LooseWP = false);
    float MCTagEfficiency(pat::Jet jet, int WP);
    std::map<int, string> Systs;
    BTagCalibration * calib;
    BTagCalibrationReader * reader;
    BTagCalibrationReader * readerCent;
    BTagCalibrationReader * readerExc;
    BTagCalibrationReader * readerCentExc;
    BTagCalibrationReader * readerLight;
    BTagCalibrationReader * readerCentLight;
    BTagCalibrationReader * readerExcLight;
    BTagCalibrationReader * readerCentExcLight;
  };
#endif

