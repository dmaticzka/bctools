#!/usr/bin/env python

tool_description = """
Remove spurious events originating from errors in random sequence tags.

This script compares all events sharing the same coordinates.
Among each group of events the maximum number of PCR duplicates is determined.
All events that are supported by less than 10 percent of this maximum count are removed.

By default output is written to stdout.

Input:
* bed6 file containing crosslinking events with score field set to number of PCR duplicates

Output:
* bed6 file with spurious crosslinking events removed, sorted by fields chrom, start, stop, strand

Example usage:
- remove spurious events from spurious.bed and write results to file cleaned.bed:
rm_spurious_events.py spurious.bed --out cleaned.bed

Status: Testing
"""

import argparse
import logging
from sys import stdout
import pandas as pd

# avoid ugly python IOError when stdout output is piped into another program
# and then truncated (such as piping to head)
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

# parse command line arguments
parser = argparse.ArgumentParser(description=tool_description)

# positional arguments
parser.add_argument(
    "events",
    help="Path to bed6 file containing alignments.")
# optional arguments
parser.add_argument(
    "-o", "--outfile",
    help="Write results to this file.")
parser.add_argument(
    "-t", "--threshold",
    type=float,
    default=0.1,
    help="Threshold for spurious event removal."
)
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
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
elif args.verbose:
    logging.basicConfig(level=logging.INFO, format="%(filename)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(format="%(filename)s - %(levelname)s - %(message)s")
logging.info("Parsed arguments:")
logging.info("  alignments: '{}'".format(args.events))
logging.info("  threshold: '{}'".format(args.threshold))
if args.outfile:
    logging.info("  outfile: enabled writing to file")
    logging.info("  outfile: '{}'".format(args.outfile))
logging.info("")

# check threshold parameter value
if args.threshold < 0 or args.threshold > 1:
    raise ValueError("Threshold must be in [0,1].")

# load alignments
alns = pd.read_csv(
    args.events,
    sep="\t",
    names=["chrom", "start", "stop", "read_id", "score", "strand"])

# remove all alignments that not enough PCR duplicates with respect to
# the group maximum
grouped = alns.groupby(['chrom', 'start', 'stop', 'strand'], group_keys=False)
alns_cleaned = grouped.apply(lambda g: g[g["score"] >= args.threshold * g["score"].max()])

# write coordinates of crosslinking event alignments
alns_cleaned_out = (open(args.outfile, "w") if args.outfile is not None else stdout)
alns_cleaned.to_csv(
    alns_cleaned_out,
    columns=['chrom', 'start', 'stop', 'read_id', 'score', 'strand'],
    sep="\t", index=False, header=False)
alns_cleaned_out.close()
