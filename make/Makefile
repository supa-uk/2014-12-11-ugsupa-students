# Count words.

include config.mk

TXT_FILES=$(wildcard books/*.txt)
$(warning The value of TXT_FILES is $(TXT_FILES))
DAT_FILES=$(patsubst books/%.txt, %.dat, $(TXT_FILES))
JPG_FILES=$(patsubst books/%.txt, %.jpg, $(TXT_FILES))

%.dat : books/%.txt $(COUNT_SRC)
	$(COUNT_EXE) $< $@

%.jpg : %.dat $(PLOT_SRC)
	$(PLOT_EXE) $< $@

.PHONY : dats
dats : $(DAT_FILES)

.PHONY : jpgs
jpgs : $(JPG_FILES)

analysis.tar.gz : $(DAT_FILES) $(JPG_FILES) $(COUNT_SRC) $(PLOT_SRC)
	tar -czf $@ $^

.PHONY : clean
clean : 
	rm -f $(DAT_FILES)
	rm -f $(JPG_FILES)
	rm -f analysis.tar.gz
