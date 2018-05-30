#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import merge_reads

class TestUtils(unittest.TestCase):


   def test_parse(self):

      fname1 = 'test_file1.fastq'
      fname2 = 'test_file2.fastq'

      with open(fname1) as f, open(fname2) as g:

         # First pair of reads.
         read_pair = next(merge_reads.PairedEndRead.parse(f, g))

         expected_read1 = 'TACACGTGTTTGGATCGATCTACCTGTCCTTCCGCACTAATGA' \
               'ATTCGTTGCATTGTTGCTGTAAACAAGTAGAT'
         expected_qual1 = 'BBBBBECGGGGGGGGGGGGGGFEGGGGGGGGGGGGGGGGGGGG' \
               'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG'
         expected_read2 = 'TCTTGTTTACAGCAACAATGCAACGAATTCATTAGTGCGGAAG' \
               'GACAGGTAGATCGATCCAAACACGTGAAAGAT'
         expected_qual2 = 'BCCCCGGGGGGGGGGGFGGGGGGGEFGGGGGGGGGGGGGGGGG' \
               'GGGFGGGGGGGGGGGGGGGGGGGGDGGGGGGG'

         self.assertEqual(read_pair.read1, expected_read1)
         self.assertEqual(read_pair.qual1, expected_qual1)
         self.assertEqual(read_pair.read2, expected_read2)
         self.assertEqual(read_pair.qual2, expected_qual2)

         # Second pair of reads.
         read_pair = next(merge_reads.PairedEndRead.parse(f, g))

         expected_read1 = 'TACCGTCCTGTAGATCGATCGACCTGAAGGAACGCACTAATGA' \
               'ATTCGTTGCAAGATGAATAAGAATCCGAAAGA'
         expected_qual1 = 'CCCCCGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG' \
               'GGGGGGGGGGGGGGGGGGGGGFGGGGGGGFEE'
         expected_read2 = 'ATCGGATTCTTATTCATCTTGCAACGAATTCATTAGTGCGTTC' \
               'CTTCAGGTCAATCGATCTACAGGACGGTGAGA'
         expected_qual2 = 'BCCCCGGGGGGGGGGGGGGGGFGGCG?BFGEGG>GGGGGGGGG' \
               'GGGGGGGGG@GGGDDGGGGGGGGGGGGGGEGC'

         self.assertEqual(read_pair.read1, expected_read1)
         self.assertEqual(read_pair.qual1, expected_qual1)
         self.assertEqual(read_pair.read2, expected_read2)
         self.assertEqual(read_pair.qual2, expected_qual2)

         # Third pair of reads.
         read_pair = next(merge_reads.PairedEndRead.parse(f, g))

         expected_read1 = 'GGACCGAAGGTAGATCGATCGGTAGGCCGACACGCACTAATGA' \
               'ATTCGTTGCAAAGACATAAATGATACTTAGAT'
         expected_qual1 = 'BCBCCGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG' \
               'GGGGGGGGGGGGGFGGGGGGGGGGGGGGGGGG'
         expected_read2 = 'GTATGATTTATGTCTTTGCAACGAATTCATTAGTGCGTGTCGG' \
               'CCTACCGATCGATCTACCTTCCGTCCAGATTT'
         expected_qual2 = 'BBBBCGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG' \
               'GGGGGGGGGGGGGGGGGGFGGGGGGGGGGGGG'

         self.assertEqual(read_pair.read1, expected_read1)
         self.assertEqual(read_pair.qual1, expected_qual1)
         self.assertEqual(read_pair.read2, expected_read2)
         self.assertEqual(read_pair.qual2, expected_qual2)

         # Fourth pair of reads.
         read_pair = next(merge_reads.PairedEndRead.parse(f, g))

         expected_read1 = 'TACACGTGTTTGGATCGATCTACCTGTCCTTCCGCACTAATGA' \
               'ATTCGTTGCATTGTTGCTGTAAACAAGTAGAT'
         expected_qual1 = 'BBBBBECGGGGGGGGGGGGGGFEGGGGGGGGGGGGGGGGGGGG' \
               'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG'
         expected_read2 = 'ATCGGATTCTTATTCATCTTGCAACGAATTCATTAGTGCGTTC' \
               'CTTCAGGTCAATCGATCTACAGGACGGTGAGA'
         expected_qual2 = 'BCCCCGGGGGGGGGGGGGGGGFGGCG?BFGEGG>GGGGGGGGG' \
               'GGGGGGGGG@GGGDDGGGGGGGGGGGGGGEGC'

         self.assertEqual(read_pair.read1, expected_read1)
         self.assertEqual(read_pair.qual1, expected_qual1)
         self.assertEqual(read_pair.read2, expected_read2)
         self.assertEqual(read_pair.qual2, expected_qual2)


   def test_merge(self):

      fname1 = 'test_file1.fastq'
      fname2 = 'test_file2.fastq'

      with open(fname1) as f, open(fname2) as g:

         # First pair of reads.
         read_pair = next(merge_reads.PairedEndRead.parse(f, g))
         read_pair.merge()

         expected = 'TTCACGTGTTTGGATCGATCTACCTGTCCTT' \
            'CCGCACTAATGAATTCGTTGCATTGTTGCTGTAAACAAGT'
         self.assertEqual(read_pair.merged, expected)

         # Second pair of reads.
         read_pair = next(merge_reads.PairedEndRead.parse(f, g))
         read_pair.merge()

         expected = 'CACCGTCCTGTAGATCGATCGACCTGAAGGA' \
            'ACGCACTAATGAATTCGTTGCAAGATGAATAAGAATCCGAA'
         self.assertEqual(read_pair.merged, expected)

         # Third pair of reads.
         read_pair = next(merge_reads.PairedEndRead.parse(f, g))
         read_pair.merge()

         expected = 'GGACGGAAGGTAGATCGATCGGTAGGCCGAC' \
            'ACGCACTAATGAATTCGTTGCAAAGACATAAATGATAC'
         self.assertEqual(read_pair.merged, expected)

         # Fourth pair of reads (must trigger an excecption).
         read_pair = next(merge_reads.PairedEndRead.parse(f, g))

         self.assertRaises(merge_reads.MergeFailureException,
               read_pair.merge)



if __name__ == '__main__':
   unittest.main()
