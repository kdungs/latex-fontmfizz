clean:
	rm -f fontmfizz.sty
	rm -f fontmfizz.tex
	rm -rf build/
	rm -rf release/

fontmfizz.sty: fontmfizz_template.sty
	./build.py $<

fontmfizz.tex: fontmfizz_template.tex fontmfizz.sty
	./build.py $<

build/fontmfizz.pdf: fontmfizz.tex
	mkdir -p build
	latexmk -lualatex -output-directory=build fontmfizz

release: build/fontmfizz.pdf
	mkdir -p release
	cp LICENSE release/
	cp README release/
	cp build/fontmfizz.pdf release/
	cp font-mfizz.ttf release/
	cp fontmfizz.sty release/
	cp fontmfizz.tex release/
