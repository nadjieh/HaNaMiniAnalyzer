      
LL = "(higgsReg.b1Index >= 0 ? jetsBtag[higgsReg.b1Index] > 0.460 : 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.460 : 0)"
ML = "((higgsReg.b1Index >= 0 ? jetsBtag[higgsReg.b1Index] > 0.800 : 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.460: 0)) | ((higgsReg.b1Index >=0 ? jetsBtag[higgsReg.b1Index] > 0.460: 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.800: 0))"
TL = "((higgsReg.b1Index >= 0 ? jetsBtag[higgsReg.b1Index] > 0.935 : 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.460: 0)) | ((higgsReg.b1Index >=0 ? jetsBtag[higgsReg.b1Index] > 0.460: 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.935: 0))"
MM = "((higgsReg.b1Index >= 0 ? jetsBtag[higgsReg.b1Index] > 0.800 : 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.800: 0)) | ((higgsReg.b1Index >=0 ? jetsBtag[higgsReg.b1Index] > 0.800: 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.800: 0))"
TM = "((higgsReg.b1Index >= 0 ? jetsBtag[higgsReg.b1Index] > 0.935 : 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.800: 0)) | ((higgsReg.b1Index >=0 ? jetsBtag[higgsReg.b1Index] > 0.800: 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.935: 0))"
TT = "((higgsReg.b1Index >= 0 ? jetsBtag[higgsReg.b1Index] > 0.935 : 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.935: 0)) | ((higgsReg.b1Index >=0 ? jetsBtag[higgsReg.b1Index] > 0.935: 0) && (higgsReg.b2Index >=0 ? jetsBtag[higgsReg.b2Index] > 0.935: 0))"         


mHcut = "abs(higgs.mass - 125) < 25"
width = "0.18 + (0.175* aMu.mass)"
chi2B = "pow((abjet.mass-aMu.mass),2)/pow(%s,2) < 5" %(width)
chi2H = "pow((higgs.mass-125),2)/pow(10.56,2) < 5"
chi2Sum = "(pow((abjet.mass-aMu.mass),2)/pow(%s,2)+pow((higgs.mass-125),2)/pow(10.56,2)) < 20" %(width)


Cuts = {"Trigger":"",
		"MuPt":"muPt[0]>25 && muPt[1]>10",
		"JetPt": "muPt[0]>25 && muPt[1]>10" + " && jetsPt[0]>20 && jetsPt[0]>15",
		"OptimCuts":"jetsPt[0]>20 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2",
		"JetPt25":"jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2",
		"MET":"jetsPt[0]>20 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30",
		"METJet25":"jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30",
		"Chi2B":"jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30 && %s" %(chi2B), 
		"Chi2H":"jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30 && %s" %(chi2H),
		"Chi2Sum":"jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30 && %s" %(chi2Sum),
		"LL" : "%s && jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30 && %s" %(LL, chi2Sum),
		"ML" : "%s && jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30 && %s" %(ML, chi2Sum),
		"TL" : "%s && jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30 && %s" %(TL, chi2Sum),
		"MM" : "%s && jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30 && %s" %(MM, chi2Sum),
		"TM" : "%s && jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30 && %s" %(TM, chi2Sum),
		"TT" : "%s && jetsPt[0]>25 && jetsPt[1]>15 && muPt[0]>25 && muPt[1]>10 && metSig < 2 && met < 30 && %s" %(TT, chi2Sum),		
}

dphi_ = "abs(abjetReg.phi - aMu.phi)"
dphi = (dphi_ + ">= 3.14 ? 6.28 - "+ dphi_ + ": "+ dphi_) 
deta = "abs(abjetReg.eta - aMu.eta)"
DR = "sqrt(pow(%s,2) + pow(%s,2))" % (dphi , deta)

lb0Px = "muPt[0]*cos(muPhi[0])+jetsPt[0]*cos(jetsPhi[0])"
lb0Py = "muPt[0]*sin(muPhi[0])+jetsPt[0]*sin(jetsPhi[0])"
lb0Pz = "muPt[0]*sinh(muEta[0])+jetsPt[0]*sinh(jetsEta[0])"
mu0En = "sqrt((muPt[0]*muPt[0]) + (%s * %s))" %(lb0Pz,lb0Pz)
lb0En = "jetsE[0] + %s" %(mu0En)
lb0M = "sqrt(pow(%s,2)+pow(%s,2)+pow(%s,2)-pow(%s,2))" %(lb0Px, lb0Py, lb0Pz, lb0En)

lb1Px = "muPt[0]*cos(muPhi[0])+jetsPt[1]*cos(jetsPhi[1])"
lb1Py = "muPt[0]*sin(muPhi[0])+jetsPt[1]*sin(jetsPhi[1])"
lb1Pz = "muPt[0]*sinh(muEta[0])+jetsPt[1]*sinh(jetsEta[1])"
mu1En = "sqrt((muPt[0]*muPt[0]) + (%s * %s))" %(lb1Pz,lb1Pz)
lb1En = "jetsE[1] + %s" %(mu1En)
lb1M = "sqrt(pow(%s,2)+pow(%s,2)+pow(%s,2)-pow(%s,2))" %(lb1Px, lb1Py, lb1Pz, lb1En)

lb2Px = "muPt[1]*cos(muPhi[1])+jetsPt[0]*cos(jetsPhi[0])"
lb2Py = "muPt[1]*sin(muPhi[1])+jetsPt[0]*sin(jetsPhi[0])"
lb2Pz = "muPt[1]*sinh(muEta[1])+jetsPt[0]*sinh(jetsEta[0])"
mu2En = "sqrt((muPt[1]*muPt[1]) + (%s * %s))" %(lb2Pz,lb2Pz)
lb2En = "jetsE[0] + %s" %(mu2En)
lb2M = "sqrt(pow(%s,2)+pow(%s,2)+pow(%s,2)-pow(%s,2))" %(lb2Px, lb2Py, lb2Pz, lb2En)

lb3Px = "muPt[1]*cos(muPhi[1])+jetsPt[1]*cos(jetsPhi[1])"
lb3Py = "muPt[1]*sin(muPhi[1])+jetsPt[1]*sin(jetsPhi[1])"
lb3Pz = "muPt[1]*sinh(muEta[1])+jetsPt[1]*sinh(jetsEta[1])"
mu3En = "sqrt((muPt[1]*muPt[1]) + (%s * %s))" %(lb3Pz,lb3Pz)
lb3En = "jetsE[1] + %s" %(mu3En)
lb3M = "sqrt(pow(%s,2)+pow(%s,2)+pow(%s,2)-pow(%s,2))" %(lb3Px, lb3Py, lb3Pz, lb3En)
outname = "checkYields_Oct14_MassProd"
amuMass = "aMu.mass"
abMass = "abjet.mass"
mH = "higgs.mass"
mHReg = "higgsReg.mass"
hRegPt = "higgsReg.pt"
hPt = "higgs.pt"
myW = "bWs.W2L*Weight"
myWLM = "bWs.W1L1M*Weight"
myWLT ="bWs.W1L1T*Weight"
myWMM ="bWs.W2M*Weight"
myWMT ="bWs.W1M1T*Weight"
myWTT ="bWs.W2T*Weight"

