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
int main(int argc, char** argv) {
    double sigNormUnc = 0;
    bool blind = true;
    bool WideRange = false;
    for (int f = 1; f < argc; f++) {
        std::string arg_fth(*(argv + f));
	cout<<arg_fth<<endl;
        if (arg_fth == "sigNormUnc") {
            f++;
            std::string out(*(argv + f));
            sigNormUnc = std::atof(out.c_str());
        } else if (arg_fth == "unblind") {
            //f++;
	    blind = false;
	} else if (arg_fth == "wide") {
	    cout<<"WIDE"<<endl;
            //f++;
            WideRange = true;
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
    //for (double i = 25.; i < 65; i += 0.5) {
    //for (double i = 30.; i < 30.01; i += 0.5) {
    //	double i = 28;
    if(WideRange)
        cout<<"In provider :-)"<<endl;
    WSProvider * myprovider = new WSProvider(meanerrors, fixes, sigNormUnc,WideRange);
    myprovider->WriteWS(blind);
    delete myprovider;
    return 0;
}
