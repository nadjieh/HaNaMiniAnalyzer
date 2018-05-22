HOMELIB		= $(HOME)/lib
ROOFITLIB	=$(ROOFITSYS)/lib
ROOTINC		=-I$(shell root-config --incdir)
ROOTLIBS	=$(shell root-config --libs) -lMinuit #-lRooFit -lRooFitCore -lRooStats 
ROOTCFLAGS	=$(shell root-config --cflags)
ROOTGLIBS	=$(shell root-config --glibs) -lMinuit #-lRooFit -lRooFitCore -lRooStats
ROOFITLIBS       =-L$(ROOFITLIB) -lRooFit -lRooFitCore -lRooStats 
COMBLIB		=-L$(HOMELIB) -lHiggsAnalysisCombinedLimit
ROOFITINC	=-I$(ROOFITSYS)/include
MYHEADERS=-I../interface
CXX=g++

GLIBS		=$(ROOTGLIBS) 
LIBS		= $(ROOTLIBS)
LIBS		+= $(ROOFITLIBS)
LIBS		+= $(COMBLIB)
HEADERS 	+= $(MYHEADERS)
HEADERS 	+= $(ROOFITINC)

CXXFLAGS = -c -O0 $(ROOTCFLAGS) -fPIC $(HEADERS) -g

all: doTtest provideIntermediate clean

t: doTtest clean

ws: provideWS clean

md: provideIntermediate clean

provideWS: WSProvider.o
	g++ WSProvider.o -o provideWS $(ROOTGLIBS) $(LIBS) -g -fPIC -O0 -I/opt/root/include -m64 -pthread $(HEADERS)
doTtest: myT_test.o
	g++ myT_test.o -o doTtest $(ROOTGLIBS) $(LIBS) -g -fPIC -O0 -I/opt/root/include -m64 -pthread $(HEADERS)

provideIntermediate: IntermediateProvider.o
	g++ IntermediateProvider.o -o provideIntermediate $(ROOTGLIBS) $(LIBS) -g -fPIC -O0 -I/opt/root/include -m64 -pthread $(HEADERS)
clean:
	@echo "Cleaning..."
	@rm -f *.o
