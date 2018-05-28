void FillCOsMap( std::map< unsigned int , double > COs ){
  COs[1] = 12.7065;
  COs[2] = 4.3026;
  COs[3] = 3.1824;
  COs[4] = 2.7764;
  COs[5] = 2.5706;
  COs[6] = 2.4469;
  COs[7] = 2.3646;
  COs[8] = 2.306;
  COs[9] = 2.2621;
  COs[10] = 2.2282;
  COs[11] = 2.201;
  COs[12] = 2.1788;
  COs[13] = 2.1604;
  COs[14] = 2.1448;
  COs[15] = 2.1314;
  COs[16] = 2.1199;
  COs[17] = 2.1098;
  COs[18] = 2.1009;
  COs[19] = 2.093;
  COs[20] = 2.086;
  COs[21] = 2.0796;
  COs[22] = 2.0739;
  COs[23] = 2.0686;
  COs[24] = 2.0639;
  COs[25] = 2.0596;
  COs[26] = 2.0555;
  COs[27] = 2.0518;
  COs[28] = 2.0484;
  COs[29] = 2.0452;
  COs[30] = 2.0423;
  COs[31] = 2.0395;
  COs[32] = 2.0369;
  COs[33] = 2.0345;
  COs[34] = 2.0322;
  COs[35] = 2.0301;
  COs[36] = 2.0281;
  COs[37] = 2.0262;
  COs[38] = 2.0244;
  COs[39] = 2.0227;
  COs[40] = 2.0211;
  COs[41] = 2.0196;
  COs[42] = 2.0181;
  COs[43] = 2.0167;
  COs[44] = 2.0154;
  COs[45] = 2.0141;
  COs[46] = 2.0129;
  COs[47] = 2.0117;
  COs[48] = 2.0106;
  COs[49] = 2.0096;
  COs[50] = 2.0086;
  COs[51] = 2.0076;
  COs[52] = 2.0066;
  COs[53] = 2.0057;
  COs[54] = 2.0049;
  COs[55] = 2.0041;
  COs[56] = 2.0032;
  COs[57] = 2.0025;
  COs[58] = 2.0017;
  COs[59] = 2.001;
  COs[60] = 2.0003;
  COs[61] = 1.9996;
  COs[62] = 1.999;
  COs[63] = 1.9983;
  COs[64] = 1.9977;
  COs[65] = 1.9971;
  COs[66] = 1.9966;
  COs[67] = 1.996;
  COs[68] = 1.9955;
  COs[69] = 1.995;
  COs[70] = 1.9944;
  COs[71] = 1.9939;
  COs[72] = 1.9935;
  COs[73] = 1.993;
  COs[74] = 1.9925;
  COs[75] = 1.9921;
  COs[76] = 1.9917;
  COs[77] = 1.9913;
  COs[78] = 1.9909;
  COs[79] = 1.9904;
  COs[80] = 1.9901;
  COs[81] = 1.9897;
  COs[82] = 1.9893;
  COs[83] = 1.9889;
  COs[84] = 1.9886;
  COs[85] = 1.9883;
  COs[86] = 1.9879;
  COs[87] = 1.9876;
  COs[88] = 1.9873;
  COs[89] = 1.987;
  COs[90] = 1.9867;
  COs[91] = 1.9864;
  COs[92] = 1.9861;
  COs[93] = 1.9858;
  COs[94] = 1.9855;
  COs[95] = 1.9852;
  COs[96] = 1.985;
  COs[97] = 1.9847;
  COs[98] = 1.9845;
  COs[99] = 1.9842;
  COs[100] = 1.984;
};
  
std::vector<std::string> split(const std::string &s, char delim) {
  std::vector<std::string> elems;
  
  std::stringstream ss;
  ss.str(s);
  std::string item;
  while (std::getline(ss, item, delim)) {
    elems.push_back(item);
  }

  return elems;
}





#include "RooInvPoly.h"

ClassImp(RooPolynomial);

/// coverity[UNINIT_CTOR]

RooInvPoly::RooInvPoly()
{
}


////////////////////////////////////////////////////////////////////////////////
/// Constructor

RooInvPoly::RooInvPoly(const char* name, const char* title, 
			     RooAbsReal& x, const RooArgList& coefList, Int_t lowestOrder) :
  RooAbsPdf(name, title),
  _x("x", "Dependent", this, x),
  _coefList("coefList","List of coefficients",this),
  _lowestOrder(lowestOrder) 
{
  // Check lowest order
  if (_lowestOrder<0) {
    coutE(InputArguments) << "RooInvPoly::ctor(" << GetName() 
			  << ") WARNING: lowestOrder must be >=0, setting value to 0" << endl ;
    _lowestOrder=0 ;
  }

  RooFIter coefIter = coefList.fwdIterator() ;
  RooAbsArg* coef ;
  while((coef = (RooAbsArg*)coefIter.next())) {
    if (!dynamic_cast<RooAbsReal*>(coef)) {
      coutE(InputArguments) << "RooInvPoly::ctor(" << GetName() << ") ERROR: coefficient " << coef->GetName() 
			    << " is not of type RooAbsReal" << endl ;
      R__ASSERT(0) ;
    }
    _coefList.add(*coef) ;
  }
}



////////////////////////////////////////////////////////////////////////////////

RooInvPoly::RooInvPoly(const char* name, const char* title,
                           RooAbsReal& x) :
  RooAbsPdf(name, title),
  _x("x", "Dependent", this, x),
  _coefList("coefList","List of coefficients",this),
  _lowestOrder(1)
{ }                                                                                                                                 

////////////////////////////////////////////////////////////////////////////////
/// Copy constructor

RooInvPoly::RooInvPoly(const RooInvPoly& other, const char* name) :
  RooAbsPdf(other, name), 
  _x("x", this, other._x), 
  _coefList("coefList",this,other._coefList),
  _lowestOrder(other._lowestOrder) 
{ }




////////////////////////////////////////////////////////////////////////////////
/// Destructor

RooInvPoly::~RooInvPoly()
{ }




////////////////////////////////////////////////////////////////////////////////

Double_t RooInvPoly::evaluate() const 
{
  // Calculate and return value of InvPoly

  const unsigned sz = _coefList.getSize();
  const int lowestOrder = _lowestOrder;
  if (!sz) return lowestOrder ? 1. : 0.;
  _wksp.clear();
  _wksp.reserve(sz);
  {
    const RooArgSet* nset = _coefList.nset();
    RooFIter it = _coefList.fwdIterator();
    RooAbsReal* c;
    while ((c = (RooAbsReal*) it.next())) _wksp.push_back(c->getVal(nset));
  }
  const Double_t x = _x;
  Double_t retVal = _wksp[sz - 1];
  for (unsigned i = sz - 1; i--; ) retVal = _wksp[i] + x * retVal;
  return 1.0/(retVal * std::pow(x, lowestOrder) + (lowestOrder ? 1.0 : 0.0));
}

