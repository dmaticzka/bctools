#!/usr/bin/env python

tool_description = """
Merge PCR duplicates identified by random barcode. By default output is written to stdout.

Input:
bed6 file with random barcode in name field

Output:
bed6 file with random barcode in name field and number of PCR duplicates as score

Example usage:
- read PCR duplicates from file duplicates.bed and write merged results to file merged.bed:
merge_pcr_duplicates.py duplicates.bed --out merged.bed
"""

# status: development
# * TODO:
#     * implement tests
#     * implement filter for barcodes containing N
#     * implement merging
#     * implement high pass filter

import argparse
import logging

# avoid ugly python IOError when stdout output is piped into another program
# and then truncated (such as piping to head)
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

# parse command line arguments
parser = argparse.ArgumentParser(description=tool_description)

# positional arguments
parser.add_argument(
    "infile",
    help="Path to fastq file.")
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

args = parser.parse_args()
if args.debug:
    logging.basicConfig(level=logging.DEBUG)
elif args.verbose:
    logging.basicConfig(level=logging.INFO)
logging.info("Parsed arguments:")
logging.info("  infile: '{}'".format(args.infile))
if args.outfile:
    logging.info("  outfile: enabled writing to file")
    logging.info("  outfile: '{}'".format(args.outfile))
logging.info("")
