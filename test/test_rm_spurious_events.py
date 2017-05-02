from past.builtins import cmp
import re
from scripttest import TestFileEnvironment

bindir = "bin/"
datadir = "test/data/"
testdir = "test/testenv_rm_spurious_events/"
env = TestFileEnvironment(testdir)
# relative to test file environment
bindir_rel = "../../" + bindir
datadir_rel = "../../" + datadir


def test_call_without_parameters():
    "Call coords2clnt.py withouth any additional parameters."
    run = env.run(
        bindir_rel + "rm_spurious_events.py",
        expect_error=True
    )
    assert(re.search("usage", run.stderr))


def test_call_fileout():
    "Call rm_spurious_events.py with infile and outfile."
    infile = "merged_pcr_dupes_spurious.bed"
    outfile = "merged_pcr_dupes_spurious_filtered.bed"
    env.run(
        bindir_rel + "rm_spurious_events.py",
        datadir_rel + infile,
        "--outfile", outfile
    )
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes_spurious_filtered.bed"
    ))


def test_call_fileout_threshold_50p():
    "Call rm_spurious_events.py with infile and outfile, setting threshold for detection of spurious events to 50%."
    infile = "merged_pcr_dupes_spurious.bed"
    outfile = "merged_pcr_dupes_spurious_filtered_thresh05.bed"
    env.run(
        bindir_rel + "rm_spurious_events.py",
        datadir_rel + infile,
        "--outfile", outfile,
        "--threshold", 0.5,
    )
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes_spurious_filtered_thresh05.bed"
    ))


def test_call_not_sorted():
    "Call rm_spurious_events.py with bed entries that are not sorted and outfile."
    infile = "merged_pcr_dupes_spurious_notsorted.bed"
    outfile = "merged_pcr_dupes_spurious_filtered2.bed"
    env.run(
        bindir_rel + "rm_spurious_events.py",
        datadir_rel + infile,
        "--outfile", outfile
    )
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes_spurious_filtered2.bed"
    ))
