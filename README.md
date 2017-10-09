[![Build Status](https://travis-ci.org/dmaticzka/bctools.svg?branch=master)](https://travis-ci.org/dmaticzka/bctools)

# bctools

Tools for handling barcodes and UMIs in NGS data.

bctools

* merges PCR duplicates according to unique molecular barcodes (UMIs) [merge_pcr_duplicates.py]
* filters out spurious events produced by erroneous UMIs [rm_spurious_events.py]
* extracts barcodes from arbitrary positions relative to the read starts [extract_bcs.py]
* cleans up readthroughs into UMIs with paired-end sequencing [remove_tail.py] and
* handles binary RY-space barcodes as used with uvCLAP and FLASH [convert_bc_to_binary_RY.py]

## Installation

bctools is available via [bioconda](https://bioconda.github.io) and can be easily installed via

```bash
conda install bctools -c bioconda -c conda-forge
```
