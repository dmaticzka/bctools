import re
from filecmp import cmp
from scripttest import TestFileEnvironment

bindir = "bin/"
datadir = "test/data/"
testdir = "test/testenv_extract_aln_ends_bt2/"
env = TestFileEnvironment(testdir)
# relative to test file environment
bindir_rel = "../../" + bindir
datadir_rel = "../../" + datadir


def test_call_without_parameters():
    "Call extract_aln_ends_bt2.py withouth any additional parameters."
    run = env.run(
        bindir_rel + "extract_aln_ends_bt2.py",
        expect_error=True
    )
    assert(re.search("too few arguments", run.stderr))


def test_call_fileout():
    "Call extract_aln_ends_bt2.py with infile and outfile."
    infile = "tworeads.sam"
    outfile = "tworeads_aln_ends.bed"
    env.run(
        bindir_rel + "extract_aln_ends_bt2.py",
        datadir_rel + infile,
        "--outfile", outfile
    )
    assert(cmp(
        testdir + outfile,
        datadir + "tworeads_aln_ends.bed"
    ))


def test_call_stdout():
    "Call extract_aln_ends_bt2.py with infile, write to stdout."
    infile = "tworeads.sam"
    outfile = "tworeads_aln_ends_stdout.bed"
    run = env.run(
        bindir_rel + "extract_aln_ends_bt2.py",
        datadir_rel + infile
    )
    with open(testdir + outfile, "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + outfile,
        datadir + "tworeads_aln_ends.bed"
    ))
