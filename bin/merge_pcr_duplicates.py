#!/usr/bin/env python

tool_description = """
Merge PCR duplicates identified by random barcode. By default output is written to stdout.

Input:
* bed6 file containing alignments with fastq read-id in name field
* fasta library with fastq read-id as sequence ids

Output:
bed6 file with random barcode in name field and number of PCR duplicates as score

Example usage:
- read PCR duplicates from file duplicates.bed and write merged results to file merged.bed:
merge_pcr_duplicates.py duplicates.bed bclibrary.fa --out merged.bed
"""

# status: development
# * TODO:
#     * implement filter for barcodes containing N
#     * implement merging
#     * implement high pass filter

import argparse
import logging
from Bio import SeqIO

# avoid ugly python IOError when stdout output is piped into another program
# and then truncated (such as piping to head)
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

# parse command line arguments
parser = argparse.ArgumentParser(description=tool_description)

# positional arguments
parser.add_argument(
    "infile",
    help="Path to bed6 file containing alignments.")
parser.add_argument(
    "bclib",
    help="Path to fasta barcode library.")
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
logging.info("  bclib: '{}'".format(args.bclib))
if args.outfile:
    logging.info("  outfile: enabled writing to file")
    logging.info("  outfile: '{}'".format(args.outfile))
logging.info("")

# load barcode library into dictionary
input_handle = open(args.bclib, "rU")
input_seq_iterator = SeqIO.parse(input_handle, "fasta")
barcode_dict = {record.id: record.seq for record in input_seq_iterator}
if args.debug:
    for bcid, bcseq in barcode_dict.items():
        logging.debug("barcode id: " + bcid)
        logging.debug("barcode seq: " + bcseq)
