DIR= /home/atorello/Deamination/Data/2018-01-17

TARGETS= \
	10_23425_TCCAGA_parsed.txt   \
	2_23417_CGCATT_parsed.txt    \
	11_23426_GTCCCT_parsed.txt   \
	3_23418_CCGAGT_parsed.txt    \
	4_23419_CAAACA_parsed.txt    \
	12_23427_TAATGA_parsed.txt   \
	1_23416_GATTTA_parsed.txt    \
	5_23420_GGAGTC_parsed.txt    \
	13_23428_AAACTA_parsed.txt   \
	6_23421_TCCGCT_parsed.txt    \
	14_23429_CTTAGC_parsed.txt   \
	7_23422_GACGAA_parsed.txt    \
	15_23430_TCGTCC_parsed.txt   \
	8_23423_TGTTTC_parsed.txt    \
	16_23431_TTCGAG_parsed.txt   \
	9_23424_CGGTTA_parsed.txt

all: $(TARGETS)

%_merged.txt: $(DIR)/%_read1.fastq.gz $(DIR)/%_read2.fastq.gz
	python merge_reads.py $^ > $@

%_parsed.txt: %_merged.txt
	python parse_reads.py $< > $@
