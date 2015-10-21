#!/usr/bin/env python

from distutils.core import setup

setup(
    name='bctools',
    version='0.0.1',
    description='A set of tools for handling barcodes in NGS data.',
    author='Daniel Maticzka',
    author_email='maticzkd@informatik.uni-freiburg.de',
    url='https://github.com/tzk/bctools',
    long_description=open('README.md').read(),
    scripts=[
        "bin/extract_bcs.py",
        "bin/extract_aln_ends_bt2.py",
        "bin/convert_bc_to_binary_RY.py",
        "bin/coords2clnt.py",
        "bin/merge_pcr_duplicates.py",
        "bin/remove_tail.py",
        "bin/rm_spurious_events.py",
    ],
    install_requires=[
        "scripttest",
        "argparse",
        "biopython",
        "pandas>=0.14.1",
        "pybedtools>=0.6.6",
    ]
)
