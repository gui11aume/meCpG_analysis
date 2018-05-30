#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

import seeq

from gzopen import gzopen


def extract_fingerprint_and_GATCGATC(f):
   '''The design of the oligo is the following:
   o(12) GATCGATC o(12) CGCACTAATGAATTCGTTGC u(20)
   The nucleotides labelled "o" are oligo-specific random
   nucleotides; those labelled "u" are random UMI nucleotides
   introduced during the linear amplification or the PCR.

   The "fingerprint" is the concatenation of the random
   nucleotides with a constant sequence, i.e.
   o(12) o(12) AGATACAGAGATAATACA u(20).
   '''

   cst = seeq.compile(r'CGCACTAATGAATTCGTTGCA', 4)
   GATCGATC = seeq.compile(r'GATCGATC', 1)

   for line in f:
      # First remove the constant part, keep the left part
      # with oligo-specific nucleotides plus GATCGATC, and
      # keep the UMI on the right.
      try:
         oligo,ignore,umi = cst.match(line.rstrip()).tokenize()
         # Target length is 32. Allow at most 2 indels.
         if not 30 <= len(oligo) <= 34: continue
      except (ValueError, AttributeError):
         continue

      # Then split the oligo part to extract GATCGATC
      try:
         start,end,ignore = GATCGATC.match(oligo[10:22]).matchlist[0]
      except AttributeError:
         continue
      brcd = oligo[:10+start] + oligo[10+end:]
      readout = oligo[10+start:10+end]

      # Output fingerprint and GATCGATC
      fingerprint = brcd + 'AGATACAGAGATAATACA' + umi
      sys.stdout.write('%s\t%s\n' % (fingerprint, readout))


if __name__ == '__main__':
   with gzopen(sys.argv[1]) as f:
      extract_fingerprint_and_GATCGATC(f)
