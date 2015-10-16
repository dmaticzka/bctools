#!/usr/bin/env python

tool_description = """
Extract alignment ends from sam or bam file.

The resulting bed file contains the outer coordinates of the alignments. The
bed name field is set to the read id and the score field is set to the edit
distance of the alignment. The crosslinked nucleotide is one nt upstream of the
5'-end of the bed entries.

This script only reports results for unique alignments where both mates were
aligned, all other alignments are discarded. For the interpretation of SAM
intervals, a relative orientation of the two mates of FR ("forward-reverse") is
assumed.

By default output is written to stdout.

Input:
* sam or bam file containing bowtie2 alignments (paired-end sequencing)

Output:
* bed6 file containing outer coordinates

Example usage:
- Extract coordinates from file input.bam and write to file output.bed
extract_aln_ends_bt2.py input.bam --out output.bed
"""

epilog = """
Author: Daniel Maticzka
Copyright: 2015
License: Apache
Email: maticzkd@informatik.uni-freiburg.de
Status: Development
"""

import argparse
import logging
from sys import stdout
import pandas as pd


class DefaultsRawDescriptionHelpFormatter(argparse.ArgumentDefaultsHelpFormatter,
                                          argparse.RawDescriptionHelpFormatter):
    # To join the behaviour of RawDescriptionHelpFormatter with that of ArgumentDefaultsHelpFormatter
    pass

# avoid ugly python IOError when stdout output is piped into another program
# and then truncated (such as piping to head)
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

# parse command line arguments
parser = argparse.ArgumentParser(description=tool_description,
                                 epilog=epilog,
                                 formatter_class=DefaultsRawDescriptionHelpFormatter)
# positional arguments
parser.add_argument(
    "sam",
    help="Path to sam/bam file containing alignments.")
# optional arguments
parser.add_argument(
    "-o", "--outfile",
    help="Write results to this file.")
# misc arguments
parser.add_argument(
    "-v", "--verbose",
    help="Be verbose.",
    action="store_true")
parser.add_argument(
    "-d", "--debug",
    help="Print lots of debugging information",
    action="store_true")
parser.add_argument(
    '--version',
    action='version',
    version='0.1.0')

args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
elif args.verbose:
    logging.basicConfig(level=logging.INFO, format="%(filename)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(format="%(filename)s - %(levelname)s - %(message)s")
logging.info("Parsed arguments:")
logging.info("  sam: '{}'".format(args.sam))
if args.outfile:
    logging.info("  outfile: enabled writing to file")
    logging.info("  outfile: '{}'".format(args.outfile))
logging.info("")
