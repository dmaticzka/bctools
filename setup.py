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
        "extract_bcs.py",
    ],
    install_requires=[
        "scripttest",
        "argparse",
        "biopython",
    ]
)
