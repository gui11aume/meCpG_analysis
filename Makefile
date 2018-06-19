DIR= /home/atorello/Deamination/Data/2018-01-17

TARGETS= \
	10_23425_TCCAGA_tallied.txt   \
	2_23417_CGCATT_tallied.txt    \
	11_23426_GTCCCT_tallied.txt   \
	3_23418_CCGAGT_tallied.txt    \
	4_23419_CAAACA_tallied.txt    \
	12_23427_TAATGA_tallied.txt   \
	1_23416_GATTTA_tallied.txt    \
	5_23420_GGAGTC_tallied.txt    \
	13_23428_AAACTA_tallied.txt   \
	6_23421_TCCGCT_tallied.txt    \
	14_23429_CTTAGC_tallied.txt   \
	7_23422_GACGAA_tallied.txt    \
	15_23430_TCGTCC_tallied.txt   \
	8_23423_TGTTTC_tallied.txt    \
	16_23431_TTCGAG_tallied.txt   \
	9_23424_CGGTTA_tallied.txt

all: $(TARGETS)

merged/%_merged.txt: $(DIR)/%_read1.fastq.gz $(DIR)/%_read2.fastq.gz
	python merge_reads.py $^ > $@

parsed/%_parsed.txt: merged/%_merged.txt
	python parse_reads.py $< > $@

normalized/%_normalized.txt: parsed/%_parsed.txt
	cut -f1 $< | starcode -d2 --print-clusters | \
		python normalize_fingerprints.py $< - > $@

%_tallied.txt: normalized/%_normalized.txt
	python tally.py $< > $@

clean:
	rm -f *_tallied.txt merged/* parsed/* normalized/*
