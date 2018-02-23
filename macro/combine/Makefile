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


t: Ttest clean

ws: WS clean

md: med clean

WS:
	@echo "Compiling the WSProvider.C .... \n"
	$(CXX) WSProvider.C -c -o WSProvider.o -O0 $(ROOTCFLAGS) -fPIC $(HEADERS) -g
	@echo "Linking ...... \n"
	g++ WSProvider.o -o provideWS $(ROOTGLIBS) $(LIBS) -g -fPIC -O0 -I/opt/root/include -m64 -pthread $(HEADERS)
	
Ttest:
	@echo "Compiling the myT_test .... \n"
	$(CXX) myT_test.C -c -o myT_test.o -O0 $(ROOTCFLAGS) -fPIC $(HEADERS) -g
	@echo "Linking ...... \n"
	g++ myT_test.o -o doTtest $(ROOTGLIBS) $(LIBS) -g -fPIC -O0 -I/opt/root/include -m64 -pthread $(HEADERS)

med:
	@echo "Compiling the IntermediateProvider.C .... \n"
	$(CXX) IntermediateProvider.C -c -o IntermediateProvider.o -O0 $(ROOTCFLAGS) -fPIC $(HEADERS) -g
	@echo "Linking ...... \n"
	g++ IntermediateProvider.o -o provideIntermediate $(ROOTGLIBS) $(LIBS) -g -fPIC -O0 -I/opt/root/include -m64 -pthread $(HEADERS)
clean:
	@echo "Cleaning..."
	@rm -f *.o
