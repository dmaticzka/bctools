#!/usr/bin/env python

tool_description = """
Convert fasta nucleotides to IUPAC nucleotide codes for binary barcodes.
By default output is written to stdout.

A and G are converted to nucleotide code R. T, U and C are converted to Y.

Example usage:
- write converted sequences from file in.fa to file file out.fa:
convert_bc_to_binary_RY.py in.fa --outfile out.fa

Status:
- development
"""

import argparse
import logging
from string import maketrans
from sys import stdout
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

# avoid ugly python IOError when stdout output is piped into another program
# and then truncated (such as piping to head)
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

# parse command line arguments
parser = argparse.ArgumentParser(description=tool_description)

# positional arguments
parser.add_argument(
    "infile",
    help="Path to fasta input file.")
# optional arguments
parser.add_argument(
    "-o", "--outfile",
    help="Write results to this file.")
parser.add_argument(
    "-v", "--verbose",
    help="Be verbose.",
    action="store_true")
parser.add_argument(
    "-d", "--debug",
    help="Print lots of debugging information",
    action="store_true")


def translate_nt_to_RY(seq):
    """Translates nucleotides to RY (A,G -> R; C,U,T -> Y).

    >>> translate_nt_to_RY("ACGUTACGUT")
    RYRYYRYRYY
    """
    trans_table = maketrans("AGCUT", "RRYYY")
    trans_seq = seq.translate(trans_table)
    logging.debug(seq + " -> " + trans_seq)
    return trans_seq


def translate_nt_to_RY_iterator(robj):
    """Translate SeqRecords sequences to RY alphabet."""
    for record in robj:
        record.seq = Seq(translate_nt_to_RY(str(record.seq)),
                         IUPAC.unambiguous_dna)
        yield record

# handle arguments
args = parser.parse_args()
if args.debug:
    logging.basicConfig(level=logging.DEBUG)
elif args.verbose:
    logging.basicConfig(level=logging.INFO)
logging.info("Parsed arguments:")
if args.outfile:
    logging.info("  outfile: enabled writing to file")
    logging.info("  outfile: '{}'".format(args.outfile))
logging.info("  outfile: '{}'".format(args.outfile))
logging.info("")

# get input iterator
input_handle = open(args.infile, "rU")
input_seq_iterator = SeqIO.parse(input_handle, "fasta")
convert_seq_iterator = translate_nt_to_RY_iterator(input_seq_iterator)
output_handle = (open(args.outfile, "w") if args.outfile is not None else stdout)
SeqIO.write(convert_seq_iterator, output_handle, "fasta")
output_handle.close()
