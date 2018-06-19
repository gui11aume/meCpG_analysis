#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

from collections import defaultdict

def tally(f):
   '''Count the events associated with very oligo barcode.'''

   # Events are stored in a nested dictrionary with
   # the following deep structure:
   # barcode -> umi -> readout -> read count
   deep_dict_of_bcd = \
      defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

   # After aggregating the results per UMI, the results
   # are stored in a shallower structure
   shallow_dict_of_bcd = \
      defaultdict(lambda: defaultdict(int))

   for line in f:
      bcd, umi, readout = line.split()
      deep_dict_of_bcd[bcd][umi][readout] += 1

   # One barcode at a time, count events.
   for bcd in deep_dict_of_bcd:
      dict_of_umi = deep_dict_of_bcd[bcd]
      for umi in dict_of_umi:
         dict_of_readouts = dict_of_umi[umi]
         # 1. Remove readouts with a single read.
         for readout,count in dict_of_readouts.items():
            if count < 2: del dict_of_readouts[readout]
         # 2. Associate each UMI to a single readout (by majority).
         if not dict_of_readouts: continue
         winner = max(dict_of_readouts, key=dict_of_readouts.get)
         shallow_dict_of_bcd[bcd][winner] += 1
      # 3. Print the results
      cntr = shallow_dict_of_bcd[bcd]
      if not cntr: continue # Can have been depleted at step 1.
      output = ['%s:%d' % (readout, cntr[readout]) for \
          readout in sorted(cntr, key=cntr.get, reverse=True)]
      sys.stdout.write(bcd + '\t' + ','.join(output) + '\n')



if __name__ == '__main__':
   with open(sys.argv[1]) as f:
      tally(f)
