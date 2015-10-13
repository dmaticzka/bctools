#!/usr/bin/env python

tool_description = """
Given coordinates of the aligned reads, calculate positions of the crosslinked nucleotides.
Crosslinked nts are assumed to be one nt upstream of the 5'-end of the read.

By default output is written to stdout.

Input:
* bed6 file of the aligned reads
*

Example usage:
- convert read coordinates from file in.bed to coordinates of the crosslinking events, written to out.bed:
coords2clnt.py in.bed --outfile out.bed

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
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
elif args.verbose:
    logging.basicConfig(level=logging.INFO, format="%(filename)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(format="%(filename)s - %(levelname)s - %(message)s")
logging.info("Parsed arguments:")
if args.outfile:
    logging.info("  outfile: enabled writing to file")
    logging.info("  outfile: '{}'".format(args.outfile))
logging.info("  outfile: '{}'".format(args.outfile))
logging.info("")
