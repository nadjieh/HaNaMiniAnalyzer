
pdf:
	mkdir -p out
	pdflatex -output-directory=./out/ Slides.tex
	pdflatex -output-directory=./out/ Slides.tex
	mv out/Slides.pdf .
	rm -rf *data*pdf *bestfits.pdf *correlation.pdf out Chi2.ps

pu:
	./pu_analyzer.py

all: pu pdf
