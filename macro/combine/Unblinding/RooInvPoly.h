#ifndef ROO_INVPOLY
#define ROO_INVPOLY

#include <vector>

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooListProxy.h"

#include <cmath>
#include <cassert>

#include "RooAbsReal.h"
#include "RooArgList.h"
#include "RooMsgService.h"

#include "TError.h"

using namespace std;

class RooInvPoly : public RooAbsPdf {
public:

  RooInvPoly() ;
  RooInvPoly(const char* name, const char* title, RooAbsReal& x) ;
  RooInvPoly(const char *name, const char *title,
		RooAbsReal& _x, const RooArgList& _coefList, Int_t lowestOrder=1) ;

  RooInvPoly(const RooInvPoly& other, const char* name = 0);
  virtual TObject* clone(const char* newname) const { return new RooInvPoly(*this, newname); }
  virtual ~RooInvPoly() ;

protected:

  RooRealProxy _x;
  RooListProxy _coefList ;
  Int_t _lowestOrder ;

  mutable std::vector<Double_t> _wksp; //! do not persist

  Double_t evaluate() const;

  ClassDef(RooInvPoly,1) // InvPoly PDF
};

#endif
