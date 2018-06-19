#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

from gzopen import gzopen

def lut_from_starcode_file(f):
   '''Use the output file of starcode to build a lookup table
   to replace fingerprints.'''

   dict_of_fingerprints = dict()
   for line in f:
      canonical, count, other = line.rstrip().split('\t')
      for item in other.split(','):
         dict_of_fingerprints[item] = canonical
   return dict_of_fingerprints


def replace_fingerprints_and_split(dict_of_fingerprints, f):
   '''Use the lookup table to replace the fingerprints by their
   normalized version (i.e. correct sequencing errors). Also
   extract oligo barcode and UMI from the fingerprint.'''

   sep = 'AGATACAGAGATAATACA'
   for line in f:
      fingerprint, readout = line.split()
      try:
         bcd,umi = dict_of_fingerprints[fingerprint].split(sep)
      except KeyError:
         continue
      sys.stdout.write('%s\t%s\t%s\n' % (bcd, umi, readout))


if __name__ == '__main__':
   # The starcode file is passed as second argument
   # but it must be processed first. If user passed a
   # dash symbol (-), read from stdin.
   if sys.argv[2] == '-':
      dict_of_fingerprints = lut_from_starcode_file(sys.stdin)
   else:
      with gzopen(sys.argv[2]) as f:
         dict_of_fingerprints = lut_from_starcode_file(f)

   with gzopen(sys.argv[1]) as f:
      replace_fingerprints_and_split(dict_of_fingerprints, f)
