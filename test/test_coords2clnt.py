from filecmp import cmp
import re
from scripttest import TestFileEnvironment

bindir = "bin/"
datadir = "test/data/"
testdir = "test/testenv_coords2clnt/"
env = TestFileEnvironment(testdir)
# relative to test file environment
bindir_rel = "../../" + bindir
datadir_rel = "../../" + datadir


def test_call_without_parameters():
    "Call coords2clnt.py withouth any additional parameters."
    run = env.run(
        bindir_rel + "coords2clnt.py",
        expect_error=True
    )
    assert(re.search("usage", run.stderr))


def test_call_fileout():
    "Call coords2clnt.py with infile and outfile."
    infile = "merged_pcr_dupes.bed"
    outfile = "merged_pcr_dupes_clnts.bed"
    env.run(
        bindir_rel + "coords2clnt.py",
        datadir_rel + infile,
        "--outfile", outfile
    )
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes_clnts.bed"
    ))


def test_call_fileout_threeprime():
    "Call coords2clnt.py with infile and outfile. Use threeprime position."
    infile = "merged_pcr_dupes.bed"
    outfile = "merged_pcr_dupes_clnts_threeprime.bed"
    env.run(
        bindir_rel + "coords2clnt.py",
        datadir_rel + infile,
        "--outfile", outfile,
        "-3"
    )
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes_clnts_threeprime.bed"
    ))


def test_call_stdout():
    "Call coords2clnt.py with infile, write to stdout."
    infile = "merged_pcr_dupes.bed"
    outfile = "stdout_only_positional_args.bed"
    run = env.run(
        bindir_rel + "coords2clnt.py",
        datadir_rel + infile
    )
    with open(testdir + outfile, "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes_clnts.bed"
    ))
