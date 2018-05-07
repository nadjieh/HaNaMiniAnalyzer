import argparse as argparse
#from RecoLuminosity.LumiDB import argparse
import math
from HttStyles import GetStyleHtt
from HttStyles import MakeCanvas
import ROOT
import numpy as np
from array import array

G_mu=1.16637*0.00001

m_u=0.0023
m_d=0.0048
m_s=0.2
m_c=1.64
m_t=178
m_b=4.88
m_e=0.00510998928
m_mu=0.10565836
m_tau=1.777
Lambda_QCD=0.216
mpole_c=1.23
mpole_b=4.25
mpole_t=170.3

def get_flavour(scale):
  if scale>m_t:
	return 6
  elif scale>m_b:
        return 5
  elif scale>m_c:
        return 4
  elif scale>m_s:
        return 3
  elif scale>m_d:
        return 2
  elif scale>m_u:
        return 1
  else:
	return 0

def get_factor(model,particles,tanbeta):
   if model==1:
	if particles==1:#up-type quarks
	    return (1.0/tanbeta)
	elif particles==2: #down-type quarks
	    return (-1.0/tanbeta)
	elif particles==3: #leptons
	    return (-1.0/tanbeta)
   elif model==2:
        if particles==1:#up-type quarks
            return (1.0/tanbeta)
        elif particles==2: #down-type quarks
            return (tanbeta)
        elif particles==3: #leptons
            return (tanbeta)
   elif model==3:
        if particles==1:#up-type quarks
            return (1.0/tanbeta)
        elif particles==2: #down-type quarks
            return (-1.0/tanbeta)
        elif particles==3: #leptons
            return (tanbeta)
   elif model==4:
        if particles==1:#up-type quarks
            return (1.0/tanbeta)
        elif particles==2: #down-type quarks
            return (tanbeta)
        elif particles==3: #leptons
            return (-1.0/tanbeta)

def gamma_tau(tanbeta,ma,model):
   xb=get_factor(model,3,tanbeta) 
   gamma=0
   if ma>2*m_tau:
      gamma=(G_mu/(4*(2**0.5)*math.pi))*xb*xb*ma*m_tau*m_tau*(1-4*((m_tau*m_tau)/(ma*ma)))**0.5
   return gamma

def gamma_mu(tanbeta,ma,model):
   xb=get_factor(model,3,tanbeta) 
   gamma=(G_mu/(4*(2**0.5)*math.pi))*xb*xb*ma*m_mu*m_mu*(1-4*((m_mu*m_mu)/(ma*ma)))**0.5
   return gamma

def running_alpha(scale):
   Nf=get_flavour(scale)
   beta0=11-(2.0/3)*Nf
   beta1=51-(19.0/3)*Nf
   beta2=2857-(5033.0/9)*Nf+(325.0/27)*Nf*Nf
   lmu=math.log((1.0*scale*scale)/(Lambda_QCD*Lambda_QCD))
   run=((4*math.pi)/(beta0*lmu))*(1-(2*(beta1/(beta0*beta0))*(math.log(lmu)/lmu))+((4*beta1*beta1)/(beta0*beta0*beta0*beta0*lmu*lmu))*((math.log(lmu)-0.5)*(math.log(lmu)-0.5)+((beta2*beta0)/(8*beta1*beta1))-(5.0/4)))
   return run

def get_qx(scale):
   return running_alpha(scale)/math.pi

def get_qc(scale):
   qx=get_qx(scale)
   qc=1.0
   if (m_c<=scale) and (m_b>scale):
	qc=((25.0*qx/6.0)**(12.0/25))*(1.0+1.014*qx+1.389*qx*qx+1.091*qx*qx*qx)
   if (m_b<=scale) and (m_t>scale):
        qc= ((23.0*qx/6.0)**(12.0/23))*(1.0+1.175*qx+1.501*qx*qx+0.1725*qx*qx*qx)
   if (m_t<=scale):
        qc= ((7.0*qx/2.0)**(4.0/7))*(1.0+1.398*qx+1.793*qx*qx-0.6834*qx*qx*qx)
   return qc

#def running_mass(scale,mq):
#   Nf=get_flavour(scale#)
#   running=1
#   if mq>Lambda_QCD:
#      running=mq*(1-(4.0/3)*(running_alpha(mq)/math.pi)+(1.0414*Nf-14.3323)*((running_alpha(mq)/math.pi)*(running_alpha(mq)/math.pi))+(-0.65269*Nf*Nf+26.9239*Nf-198.7068)*(running_alpha(mq)/math.pi)*(running_alpha(mq)/math.pi)*(running_alpha(mq)))
#   if mq==0.130:
#      running=0.2
#   if mq<0.12:
#      running=mq
#   return running

def running_mass(scale,quark):
    if quark==1:
	return m_u
    if quark==2:
        return m_d
    if quark==4:
        return m_s
    if quark==3:
        return (mpole_c*get_qc(scale)/get_qc(m_c))
    if quark==5:
        return (mpole_t*get_qc(scale)/get_qc(m_t))
    if quark==6:
        return (mpole_b*get_qc(scale)/get_qc(m_b))

def gamma_quarks(tanbeta,ma,model,quark):
   xb=1
   if (quark==1 or quark==3 or quark==5):
      xb=get_factor(model,1,tanbeta)
   else:
      xb=get_factor(model,2,tanbeta)
   mq=1
   if quark==1:
     mq=m_u
   elif quark==2:
     mq=m_d
   elif quark==4:
     mq=m_s
   elif quark==3:
     mq=m_c
   elif quark==5:
     mq=m_t
   elif quark==6:
     mq=m_b
   scale=ma #renormalization scale strong coupling constant
   Nf=get_flavour(scale)
   qcdcorrections=1+5.67*(running_alpha(scale)/math.pi)+(35.94-1.36*Nf)*(running_alpha(scale)/math.pi)*(running_alpha(scale)/math.pi)+(164.14-25.77*Nf+0.26*Nf*Nf)*(running_alpha(scale)/math.pi)*(running_alpha(scale)/math.pi)*(running_alpha(scale)/math.pi)+(running_alpha(scale)/math.pi)*(running_alpha(scale)/math.pi)*(3.83-math.log(1.0*ma*ma/(mpole_t*mpole_t))+(1.0/6)*math.log(running_mass(ma,quark)*running_mass(ma,quark)/(ma*ma))*math.log(running_mass(ma,quark)*running_mass(ma,quark)/(ma*ma)))
   gamma=0
   if (2*mq)<ma:
      gamma=(3*G_mu/(4*(2**0.5)*math.pi))*xb*xb*ma*running_mass(ma,quark)*running_mass(ma,quark)*((1-(4.0*mq*mq)/(ma*ma))**0.5)*qcdcorrections
   return gamma

def get_f(x):
   if x<=1:
      return math.asin((1.0*x)**0.5)*math.asin((1.0*x)**0.5)
   else:
      return (-1.0/4)*(math.log((1+(1-1.0/x)**0.5)/(1-(1-1.0/x)**0.5))-1j*math.pi)*(math.log((1+(1-1.0/x)**0.5)/(1-(1-1.0/x)**0.5))-1j*math.pi)

def get_A12(x):
   return (2.0*get_f(x)/x)

def gamma_photon(tanbeta,ma,model):
   alpha=1.0/130
   Nc=3
   qu=2.0/3
   qd=-1.0/3
   xbu=get_factor(model,1,tanbeta)
   xbd=get_factor(model,2,tanbeta)
   xbl=get_factor(model,3,tanbeta)
   termt=Nc*qu*qu*xbu*get_A12((1.0*ma*ma)/(4*m_t*m_t))
   termb=Nc*qd*qd*xbd*get_A12((1.0*ma*ma)/(4*m_b*m_b))
   termc=Nc*qu*qu*xbu*get_A12((1.0*ma*ma)/(4*m_c*m_c))
   terms=Nc*qd*qd*xbd*get_A12((1.0*ma*ma)/(4*m_s*m_s))
   termd=Nc*qd*qd*xbu*get_A12((1.0*ma*ma)/(4*m_d*m_d))
   termu=Nc*qu*qu*xbd*get_A12((1.0*ma*ma)/(4*m_u*m_u))
   termmu=xbl*get_A12((1.0*ma*ma)/(4*m_mu*m_mu))
   terme=xbl*get_A12((1.0*ma*ma)/(4*m_e*m_e))
   termtau=xbl*get_A12((1.0*ma*ma)/(4*m_tau*m_tau))
   gamma=(G_mu*alpha*alpha*ma*ma*ma/(128*(2**0.5)*math.pi*math.pi*math.pi))*abs(termt+termb+termc+terms+termu+termd+terme+termmu+termtau)*abs(termt+termb+termc+terms+termu+termd+terme+termmu+termtau)
   return gamma

def gamma_gg(tanbeta,ma,model):
   Nf=get_flavour(ma)
   xbu=get_factor(model,1,tanbeta)
   xbd=get_factor(model,2,tanbeta)
   termt=1.0*xbu*get_A12((1.0*ma*ma)/(4*m_t*m_t))
   termb=1.0*xbd*get_A12((1.0*ma*ma)/(4*m_b*m_b))
   termc=1.0*xbu*get_A12((1.0*ma*ma)/(4*m_c*m_c))
   gamma=(G_mu*running_alpha(ma)*running_alpha(ma)*ma*ma*ma/(36*(2**0.5)*math.pi*math.pi*math.pi))*abs(3.0*(termt+termb+termc)/4)*abs(3.0*(termt+termb+termc)/4)*(1+((97.0/4)-(7.0/6)*Nf)*(running_alpha(ma)/math.pi))
   return gamma

def get_total_width(model,ma,tanbeta):
   return (gamma_quarks(tanbeta,ma,model,1)+gamma_quarks(tanbeta,ma,model,2)+gamma_quarks(tanbeta,ma,model,3)+gamma_quarks(tanbeta,ma,model,4)+gamma_quarks(tanbeta,ma,model,5)+gamma_quarks(tanbeta,ma,model,6)+gamma_tau(tanbeta,ma,model)+gamma_mu(tanbeta,ma,model)+gamma_gg(tanbeta,ma,model)+gamma_photon(tanbeta,ma,model))

def make_legend():
   output = ROOT.TLegend(0.50, 0.73, 0.89, 0.90, "", "brNDC")
   output.SetNColumns(3)
   output.SetLineWidth(0)
   output.SetLineStyle(0)
   output.SetFillStyle(0)
   output.SetBorderSize(0)
   output.SetTextFont(62)
   return output

def add_model(model,tanbeta):
    lowX=0.21
    lowY=0.20
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    lumi.SetTextSize(0.04)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextFont(62)
    #lumi.AddText("2HDM+S type "+str(model)+", tan#beta = "+str(tanbeta))
    if model!=1:
       lumi.AddText("2HDM+S type-"+str(model)+",")
    if model==1:
       lumi.AddText("2HDM+S type-"+str(model))
    if model!=1:
       lumi.AddText("tan#beta = "+str(tanbeta))
    return lumi

