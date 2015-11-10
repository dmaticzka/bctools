import re
from filecmp import cmp
from scripttest import TestFileEnvironment

bindir = "bin/"
datadir = "test/data/"
testdir = "test/testenv_merge_pcr_dupes/"
env = TestFileEnvironment(testdir)
# relative to test file environment
bindir_rel = "../../" + bindir
datadir_rel = "../../" + datadir


def test_call_without_parameters():
    "Call merge_pcr_duplicates.py withouth any additional parameters."
    run = env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        expect_error=True
    )
    assert(re.search("too few arguments", run.stderr))


def test_call_fileout():
    "Call merge_pcr_duplicates.py with infile and outfile."
    infile = "pcr_dupes_sorted_2.bed"
    inlib = "pcr_dupes_randomdict.fastq"
    outfile = "merged_pcr_dupes.bed"
    env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        datadir_rel + infile,
        datadir_rel + inlib,
        "--outfile", outfile,
    )
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes.bed"
    ))


def test_call_fileout_fastalib():
    "Call merge_pcr_duplicates.py with infile and outfile, use fasta random barcode library"
    infile = "pcr_dupes_sorted_2.bed"
    inlib = "pcr_dupes_randomdict.fa"
    outfile = "merged_pcr_dupes.bed"
    env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        datadir_rel + infile,
        datadir_rel + inlib,
        "--outfile", outfile,
        "--fasta-library",
    )
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes.bed"
    ))


def test_call_stdout():
    "Call merge_pcr_duplicates.py with infile."
    infile = "pcr_dupes_sorted_2.bed"
    inlib = "pcr_dupes_randomdict.fa"
    outfile = "stdout_merged_pcr_dupes.bed"
    run = env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        datadir_rel + infile,
        datadir_rel + inlib,
        "--fasta-library",
    )
    with open(testdir + outfile, "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes.bed"
    ))


def test_call_no_readids_in_common():
    "Call merge_pcr_duplicates.py with a library that includes none of the required ids."
    infile = "pcr_dupes_sorted_2.bed"
    inlib = "pcr_dupes_randomdict_no_common_ids.fa"
    outfile = "should_not_be_crated.txt"
    run = env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        datadir_rel + infile,
        datadir_rel + inlib,
        "--outfile", outfile,
        "--fasta-library",
        expect_error=True
    )
    assert(run.returncode == 1)


def test_call_barcodes_not_available_for_all_entries():
    "Call merge_pcr_duplicates.py with infile and outfile."
    infile = "pcr_dupes_sorted_2.bed"
    inlib = "pcr_dupes_randomdict_missingsome.fa"
    outfile = "merged_pcr_dupes_incomplete.bed"
    run = env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        datadir_rel + infile,
        datadir_rel + inlib,
        "--outfile", outfile,
        "--fasta-library",
        expect_stderr=True
    )
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes_incomplete.bed"
    ))
    assert(re.search("WARNING", run.stderr))


def test_call_barcodes_withN():
    "Call merge_pcr_duplicates.py with barcodes containing uncalled bases."
    infile = "pcr_dupes_sorted_2.bed"
    inlib = "pcr_dupes_randomdict_withN.fa"
    outfile = "merged_pcr_dupes_withN.bed"
    env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        datadir_rel + infile,
        datadir_rel + inlib,
        "--outfile", outfile,
        "--fasta-library",
    )
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes_withN.bed"
    ))
