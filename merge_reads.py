#!/usr/bin/env python
# -*- coding:utf-8 -*-

import string
import sys
from itertools import izip
from gzopen import gzopen


class BadReadException(Exception):
   pass

class MergeFailureException(BadReadException):
   pass


class PairedEndRead:
   '''Sequence and read quality of paired-end reads.'''

   compl = string.maketrans('gatcGATC', 'ctagCTAG')

   def __init__(self, read1, read2, qual1, qual2):
      self.read1 = read1
      self.read2 = read2
      self.qual1 = qual1
      self.qual2 = qual2
   

   @classmethod
   def parse(cls, f, g):
      '''Iterator that yields objects from a pair of fastq files.'''

      for lineno,(line1,line2) in enumerate(izip(f,g)):
         if lineno % 4 == 1:
            # Read the sequence.
            read1 = line1.rstrip()
            read2 = line2.rstrip()
         if lineno % 4 == 3:
            # Read the quality and yield the object.
            qual1 = line1.rstrip()
            qual2 = line2.rstrip()
            yield cls(read1, read2, qual1, qual2)
            

   def merge(self):
      '''Merge the two reads (same as FLASH).'''

      def pos(x): return  x if x > 0 else 0 # The positive part.
      def neg(x): return -x if x < 0 else 0 # The negative part.

      def find_shift(seq1, seq2):
         '''Here-function to search optimal shift.'''

         # Snippet for readability.
         def seq_are_similar(seq1, seq2):
            threshold = .80 # Based on empirical considerations.
            identity = sum([a == b for (a,b) in zip(seq1, seq2)])
            return identity > len(seq1) * threshold

         # Based on the design of the experiment, the (target) shift is -4
         for delta in range(10):
            # Using a 'set' in the following line is a trick to
            # avoid running the case delta = 0 twice in the loop.
            for shift in set([delta -4, -delta -4]):
               if seq_are_similar(seq1[pos(shift):], seq2[neg(shift):]):
                  return shift
         # Did not find the shift.
         raise MergeFailureException



      # Reverse complement read 2.
      revread2 = self.read2[::-1].translate(self.compl)
      revqual2 = self.qual2[::-1]
   
      # Will trigger a 'MergeFailureException' if cannot find the shift.
      shift = find_shift(self.read1, revread2)

      # Initialize consensus. We will need to update the string
      # in place so we need a 'bytearray', which is mutable.
      # The left part (if any) is initialized with read1, the
      # right part with read2. There are two situations that look
      # as shown below.
      #   
      # Case 1: overlap is in 5' of the reads (shift is positive).
      # Consensus must be the union of the sequences.
      #   
      #         ------------------->
      #                  <---------------------
      #         | read1  |       read2        |
      #   
      # Case 2: overlap is in 3' of the reads (shift is negative).
      # Consensus must be the intersection of the sequences because
      # the overhangs are the sequencing adapters.
      #   
      #                  ------------------->
      #         <---------------------
      #                  |   read2   |

      cs = bytearray(self.read1[:pos(shift)] + revread2[neg(shift):])
      for i in range(pos(shift), min(len(self.read1), len(cs))):
         # The consensus byte array 'cs' contains numbers (not characters)
         # so we need to get the ascii code of 'read1' for comparisons.
         if ord(self.read1[i]) != cs[i] and self.qual1[i] > revqual2[i-shift]:
            cs[i] = self.read1[i]

      self.merged = str(cs)


if __name__ == '__main__':
   with gzopen(sys.argv[1]) as f, gzopen(sys.argv[2]) as g:
      for read_pair in PairedEndRead.parse(f, g):
         try:
            read_pair.merge()
            print read_pair.merged
         except MergeFailureException:
            pass
