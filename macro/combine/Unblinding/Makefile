HIG_COMBINE_DIR = /home/hbakhshi/Desktop/tHq/HiggsAnalysis/CombinedLimit/

HOMELIB		= $(HOME)/lib
ROOFITLIB	=$(ROOFITSYS)/lib
ROOTINC		=-I$(shell root-config --incdir)
ROOTLIBS	=$(shell root-config --libs) -lMinuit #-lRooFit -lRooFitCore -lRooStats 
ROOTCFLAGS	=$(shell root-config --cflags)
ROOTGLIBS	=$(shell root-config --glibs) -lMinuit #-lRooFit -lRooFitCore -lRooStats
ROOFITLIBS       =-L$(ROOFITLIB) -lRooFit -lRooFitCore -lRooStats 
COMBLIB		=-L$(HOMELIB) -lHiggsAnalysisCombinedLimit
ROOFITINC	=-I$(ROOFITSYS)/include
MYHEADERS=-I$(HIG_COMBINE_DIR)/interface
CXX=g++

GLIBS		=$(ROOTGLIBS) 
LIBS		= $(ROOTLIBS)
LIBS		+= $(ROOFITLIBS)
LIBS		+= $(COMBLIB)
HEADERS 	+= $(MYHEADERS)
HEADERS 	+= $(ROOFITINC)

CXXFLAGS = -c -O0 $(ROOTCFLAGS) -fPIC $(HEADERS) -g

all: TTest
 
RooInvPoly.C : RooInvPoly.h
	@echo "Generating dictionary ..."
	@rootcint -f RooInvPoly.C -c RooInvPoly.h

RooInvPoly.o : RooInvPoly.C

TTest : TTest.o RooInvPoly.o
	g++ TTest.o RooInvPoly.o -o TTest $(ROOTGLIBS) $(LIBS) -g -fPIC -O0 -I/opt/root/include -m64 -pthread $(HEADERS)	
clean:
	@echo "Cleaning..."
	@rm -f *.o
	@rm -f RooInvPoly_rdict.pcm RooInvPoly.C
