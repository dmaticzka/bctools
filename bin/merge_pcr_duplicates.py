#!/usr/bin/env python

import argparse
import logging
from sys import stdout
import pandas as pd
from subprocess import check_call
from shutil import rmtree
from tempfile import mkdtemp
from os.path import isfile
# avoid ugly python IOError when stdout output is piped into another program
# and then truncated (such as piping to head)
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

tool_description = """
Merge PCR duplicates according to random barcode library.

Barcodes containing uncalled base 'N' are removed. By default output is written
to stdout.

Input:
* bed6 file containing alignments with fastq read-id in name field
* fastq library of random barcodes

Output:
* bed6 file with random barcode in name field and number of PCR duplicates as
  score, sorted by fields chrom, start, stop, strand, name

Example usage:
- read PCR duplicates from file duplicates.bed and write merged results to file
  merged.bed:
merge_pcr_duplicates.py duplicates.bed bclibrary.fa --out merged.bed
"""

epilog = """
Author: Daniel Maticzka
Copyright: 2015
License: Apache
Email: maticzkd@informatik.uni-freiburg.de
Status: Testing
"""

# parse command line arguments
parser = argparse.ArgumentParser(description=tool_description,
                                 epilog=epilog,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
# positional arguments
parser.add_argument(
    "alignments",
    help="Path to bed6 file containing alignments.")
parser.add_argument(
    "bclib",
    help="Path to fastq barcode library.")
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
    version='0.2.0')

args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
elif args.verbose:
    logging.basicConfig(level=logging.INFO, format="%(filename)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(format="%(filename)s - %(levelname)s - %(message)s")
logging.info("Parsed arguments:")
logging.info("  alignments: '{}'".format(args.alignments))
logging.info("  bclib: '{}'".format(args.bclib))
if args.outfile:
    logging.info("  outfile: enabled writing to file")
    logging.info("  outfile: '{}'".format(args.outfile))
logging.info("")

# see if alignments are empty and the tool can quit
n_alns = sum(1 for line in open(args.alignments))
if n_alns == 0:
    logging.warning("WARNING: Working on empty set of alignments, writing empty output.")
    eventalnout = (open(args.outfile, "w") if args.outfile is not None else stdout)
    eventalnout.close()
    exit(0)

# check input filenames
if not isfile(args.bclib):
    raise Exception("ERROR: barcode library '{}' not found.")
if not isfile(args.alignments):
    raise Exception("ERROR: alignments '{}' not found.")

try:
    tmpdir = mkdtemp()
    logging.debug("tmpdir: " + tmpdir)

    # prepare alinments
    syscall2 = "cat " + args.alignments + " | awk -F \"\\t\" 'BEGIN{OFS=\"\\t\"}{split($4, a, \" \"); $4 = a[1]; print}'| sort -k4,4 > " + tmpdir + "/alns.csv"
    check_call(syscall2, shell=True)

    # join barcode library and alignments
    syscall3 = "cat " + args.bclib + " | awk 'BEGIN{OFS=\"\\t\"}NR%4==1{gsub(/^@/,\"\"); id=$1}NR%4==2{bc=$1}NR%4==3{print id,bc}' | sort -k1,1 | join -1 1 -2 4 - " + tmpdir + "/alns.csv " + " | awk 'BEGIN{OFS=\"\\t\"}{print $3,$4,$5,$2,$6,$7}' > " + tmpdir + "/bcalib.csv"
    check_call(syscall3, shell=True)

    # get alignments combined with barcodes
    bcalib = pd.read_csv(
        tmpdir + "/bcalib.csv",
        sep="\t",
        names=["chrom", "start", "stop", "bc", "score", "strand"])
finally:
    logging.debug("removed tmpdir: " + tmpdir)
    rmtree(tmpdir)

# fail if alignments given but combined library is empty
if bcalib.empty:
    raise Exception("ERROR: no common entries for alignments and barcode library found. Please check your input files.")

# warn if not all alignments could be assigned a barcode
n_bcalib = len(bcalib.index)
if n_bcalib < n_alns:
    logging.warning(
        "{} of {} alignments could not be associated with a random barcode.".format(n_alns - n_bcalib, n_alns))

# remove entries with barcodes that has uncalled base N
bcalib_cleaned = bcalib.drop(bcalib[bcalib.bc.str.contains("N")].index)
n_bcalib_cleaned = len(bcalib_cleaned)
# if n_bcalib_cleaned < n_bcalib:
#     msg = "{} of {} alignments had random barcodes containing uncalled bases and were dropped.".format(
#         n_bcalib - n_bcalib_cleaned, n_bcalib)
#     if n_bcalib_cleaned < (0.8 * n_bcalib):
#         logging.warning(msg)
#     else:
#         logging.info(msg)

# count and merge pcr duplicates
# grouping sorts by keys, so the ouput will be properly sorted
merged = bcalib_cleaned.groupby(['chrom', 'start', 'stop', 'strand', 'bc']).size().reset_index()
merged.rename(columns={0: 'ndupes'}, copy=False, inplace=True)

# write coordinates of crosslinking event alignments
eventalnout = (open(args.outfile, "w") if args.outfile is not None else stdout)
merged.to_csv(
    eventalnout,
    columns=['chrom', 'start', 'stop', 'bc', 'ndupes', 'strand'],
    sep="\t", index=False, header=False)
eventalnout.close()
