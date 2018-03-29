#include "WSProvider.h"
#include "SignalWSProvider.h"
using namespace std;
/****** WITH T0 SLECTION
    meanerrors["a1"] = make_pair(0.009, make_pair(0.0001,0.0001));
    meanerrors["b1"] = make_pair(0.0166, make_pair(0.0002, 0.0002));
    meanerrors["m1"] = make_pair(-0.063, make_pair(0.0038,0.0038));
    fixes["alpha"] = 1.06;
    fixes["width"] = 0.035;
    fixes["n"] = 3.22;
    fixes["frac"] = 0.607;
*/

/*** WITH PUBLISHED RESULTS (https://github.com/nadjieh/HaNaMiniAnalyzer/blob/80X/macro/combine/IntermediateProvider.C)
 * meanerrors["a1"] = make_pair(0.0091, make_pair(0.00085,0.00085));
 * meanerrors["b1"] = make_pair(0.0172, make_pair(0.0017, 0.0017));
 * meanerrors["m1"] = make_pair(-0.069, make_pair(0.0066,0.0066));
 * FixedParams fixes;
 * fixes["alpha"] = 1.15;
 * fixes["width"] = 0.008;
 * fixes["n"] = 3.02;
 * fixes["frac"] = 0.57;
 */

int main(int argc, char** argv) {
    double sigNormUnc = 0;
	double sigEff = 1.0;
	double bkgEff = 1.0;
    bool WideRange = false;
    TString btag = "";
    TString inFile = "DoubleMu2012_final_6_6.root";
	TString cat = "";
    for (int f = 1; f < argc; f++) {
        std::string arg_fth(*(argv + f));
	cout<<arg_fth<<endl;
        if (arg_fth == "sigNormUnc") {
	  f++;
	  std::string out(*(argv + f));
	  sigNormUnc = std::atof(out.c_str());
        } else if (arg_fth == "wide") {
	  cout<<"WIDE"<<endl;
            //f++;
            WideRange = true;
        } else if (arg_fth == "btag") {
	  f++;
	  std::string out(*(argv + f));
          btag = out.c_str();
	} else if (arg_fth == "input") {
	  f++;
	  std::string out(*(argv + f));
          inFile = out.c_str();
	} else if (arg_fth == "cat") {
	  f++;
	  std::string out(*(argv + f));
          cat = out.c_str();
	} else if (arg_fth == "sigEff") {
	  f++;
	  std::string out(*(argv + f));
	  sigEff = std::atof(out.c_str());
    } else if (arg_fth == "bkgEff") {
	  f++;
	  std::string out(*(argv + f));
	  bkgEff = std::atof(out.c_str());
    }

    }
    MeanErr meanerrors;
    meanerrors["a1"] = make_pair(0.000, make_pair(0.0004,0.0004));
    meanerrors["b1"] = make_pair(0.011, make_pair(0.00006, 0.00006));
    meanerrors["m1"] = make_pair(0.000, make_pair(0.00015,0.00015));
    FixedParams fixes;
    fixes["alpha"] = 1.345;
    fixes["width"] = 0.42;
    fixes["n"] = 2.7;
    fixes["frac"] = 0.121;
    /*meanerrors["a1"] = make_pair(0.0091, make_pair(0.00085,0.00085));
    meanerrors["b1"] = make_pair(0.0172, make_pair(0.0017, 0.0017));
    meanerrors["m1"] = make_pair(-0.069, make_pair(0.0066,0.0066));
    FixedParams fixes;
    fixes["alpha"] = 1.15;
    fixes["width"] = 0.008;
    fixes["n"] = 3.02;
    fixes["frac"] = 0.57;*/


    
    if(WideRange)
        cout<<"In provider :-)"<<endl;
    WSProvider * myprovider = new WSProvider(meanerrors, fixes, sigNormUnc,WideRange,btag);
	myprovider->SetCatName(cat);
	myprovider->SetSigEff(sigEff);
	myprovider->SetBkgEff(bkgEff);
    myprovider->WriteWS(inFile);
    delete myprovider;
    return 0;
}
