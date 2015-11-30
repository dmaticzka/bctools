import re
from filecmp import cmp
from scripttest import TestFileEnvironment

bindir = "bin/"
datadir = "test/data/"
testdir = "test/testenv_extract_aln_ends/"
env = TestFileEnvironment(testdir)
# relative to test file environment
bindir_rel = "../../" + bindir
datadir_rel = "../../" + datadir


def test_call_without_parameters():
    "Call extract_aln_ends.py withouth any additional parameters."
    run = env.run(
        bindir_rel + "extract_aln_ends.py",
        expect_error=True
    )
    assert(re.search("too few arguments", run.stderr))


def test_call_fileout():
    "Call extract_aln_ends.py with infile and outfile."
    infile = "twomates.sam"
    outfile = "tworeads_aln_ends.bed"
    env.run(
        bindir_rel + "extract_aln_ends.py",
        datadir_rel + infile,
        "--outfile", outfile,
    )
    assert(cmp(
        testdir + outfile,
        datadir + "tworeads_aln_ends.bed"
    ))


def test_call_fileout_baminput():
    "Call extract_aln_ends.py with infile and outfile."
    infile = "twomates.bam"
    outfile = "tworeads_aln_ends_baminput.bed"
    env.run(
        bindir_rel + "extract_aln_ends.py",
        datadir_rel + infile,
        "--outfile", outfile,
    )
    assert(cmp(
        testdir + outfile,
        datadir + "tworeads_aln_ends.bed"
    ))


def test_call_stdout():
    "Call extract_aln_ends.py with infile, write to stdout."
    infile = "twomates.sam"
    outfile = "tworeads_aln_ends_stdout.bed"
    run = env.run(
        bindir_rel + "extract_aln_ends.py",
        datadir_rel + infile,
    )
    with open(testdir + outfile, "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + outfile,
        datadir + "tworeads_aln_ends.bed"
    ))
