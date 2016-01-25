#!/usr/bin/env python

import argparse
import logging
from sys import stdout
from subprocess import check_call
from shutil import rmtree
from tempfile import mkdtemp
import os
from os.path import isfile

tool_description = """
Remove spurious events originating from errors in random sequence tags.

This script compares all events sharing the same coordinates. Among each group
of events the maximum number of PCR duplicates is determined. All events that
are supported by less than 10 percent of this maximum count are removed.

Input:
* bed6 file containing crosslinking events with score field set to number of PCR
  duplicates

Output:
* bed6 file with spurious crosslinking events removed, sorted by fields chrom,
  start, stop, strand

Example usage:
- remove spurious events from spurious.bed and write results to file cleaned.bed
rm_spurious_events.py spurious.bed --out cleaned.bed
"""

epilog = """
Author: Daniel Maticzka
Copyright: 2015
License: Apache
Email: maticzkd@informatik.uni-freiburg.de
Status: Testing
"""


class DefaultsRawDescriptionHelpFormatter(argparse.ArgumentDefaultsHelpFormatter,
                                          argparse.RawDescriptionHelpFormatter):
    # To join the behaviour of RawDescriptionHelpFormatter with that of ArgumentDefaultsHelpFormatter
    pass


def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description=tool_description,
                                     epilog=epilog,
                                     formatter_class=DefaultsRawDescriptionHelpFormatter)
    # positional arguments
    parser.add_argument(
        "events",
        help="Path to bed6 file containing alignments.")
    # optional arguments
    parser.add_argument(
        "-o", "--outfile",
        required=True,
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
    logging.info("  alignments: '{}'".format(args.events))
    logging.info("  threshold: '{}'".format(args.threshold))
    if args.outfile:
        logging.info("  outfile: enabled writing to file")
        logging.info("  outfile: '{}'".format(args.outfile))
    logging.info("")

    # check threshold parameter value
    if args.threshold < 0 or args.threshold > 1:
        raise ValueError("Threshold must be in [0,1].")

    try:
        tmpdir = mkdtemp()
        logging.debug("tmpdir: " + tmpdir)

        # prepare barcode library
        syscall = "cat " + args.events + " | sort -k1,1V -k6,6 -k2,2n -k3,3 -k5,5nr | perl " + os.path.dirname(os.path.realpath(__file__)) + "/rm_spurious_events.pl --frac_max " + str(args.threshold) + "| sort -k1,1V -k2,2n -k3,3n -k6,6 -k4,4 -k5,5nr > " + args.outfile
        check_call(syscall, shell=True)
    finally:
        logging.debug("removed tmpdir: " + tmpdir)
        rmtree(tmpdir)

    # def load_alns(fname):
    #     # load alignments
    #     logging.debug("reading csv")
    #     alns = pd.read_csv(
    #         fname,
    #         sep="\t",
    #         names=["chrom", "start", "stop", "read_id", "score", "strand"])
    #     logging.debug("setting chromosome as category")
    #     logging.debug(str(alns.dtypes))
    #     # alns["chrom"] = alns["chrom"].astype("category")
    #     # alns["strand"] = alns["strand"].astype("category")
    #     # alns["read_id"] = alns["read_id"].astype("category")
    #     logging.debug(str(alns.dtypes))
    #
    #     return alns
    #
    # alns = load_alns(args.events)
    #
    # # remove all alignments that not enough PCR duplicates with respect to
    # # the group maximum
    # logging.debug("grouping")
    # grouped = alns.groupby(['chrom', 'start', 'stop', 'strand'], group_keys=False)
    # logging.debug("cleaning")
    #
    # def threshold_group(g):
    #     group_max = max(g["score"].values)
    #     group_threshold = args.threshold * group_max
    #     return g[g["score"] >= group_threshold]
    #
    # alns_cleaned = grouped.apply(threshold_group)
    #
    # # write coordinates of crosslinking event alignments
    # logging.debug("write out")
    # alns_cleaned_out = (open(args.outfile, "w") if args.outfile is not None else stdout)
    # alns_cleaned.to_csv(
    #     alns_cleaned_out,
    #     columns=['chrom', 'start', 'stop', 'read_id', 'score', 'strand'],
    #     sep="\t", index=False, header=False)
    # alns_cleaned_out.close()

if __name__ == "__main__":
    main()
