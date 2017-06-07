from filecmp import cmp
import re
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
        expect_error=True,
    )
    assert(re.search("usage", run.stderr))


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


def test_call_extended_ids():
    "Call merge_pcr_duplicates.py with extended ids for both alignments and barcode dictionary."
    infile = "pcr_dupes_sorted_2_extended_ids.bed"
    inlib = "pcr_dupes_randomdict_extended_ids.fastq"
    outfile = "merged_pcr_dupes_extended_ids.bed"
    env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        datadir_rel + infile,
        datadir_rel + inlib,
        "--outfile", outfile,
    )
    assert cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes.bed"
    ), "files {} and {} did not match".format(testdir + outfile,
                                              datadir + "merged_pcr_dupes.bed")


def test_call_fileout_fastalib():
    "Call merge_pcr_duplicates.py with infile and outfile, use fasta random barcode library"
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


def test_call_no_readids_in_common():
    "Call merge_pcr_duplicates.py with a library that includes none of the required ids."
    infile = "pcr_dupes_sorted_2.bed"
    inlib = "pcr_dupes_randomdict_no_common_ids.fastq"
    outfile = "should_not_be_crated.txt"
    run = env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        datadir_rel + infile,
        datadir_rel + inlib,
        "--outfile", outfile,
        expect_error=True,
    )
    assert(run.returncode == 1)


# possibly reimplement this functionality, not required though
# def test_call_barcodes_not_available_for_all_entries():
#     "Call merge_pcr_duplicates.py with missing barcodes."
#     infile = "pcr_dupes_sorted_2.bed"
#     inlib = "pcr_dupes_randomdict_missingsome.fastq"
#     outfile = "merged_pcr_dupes_incomplete.bed"
#     run = env.run(
#         bindir_rel + "merge_pcr_duplicates.py",
#         datadir_rel + infile,
#         datadir_rel + inlib,
#         "--outfile", outfile,
#         expect_stderr=True,
#     )
#     assert(cmp(
#         testdir + outfile,
#         datadir + "merged_pcr_dupes_incomplete.bed"
#     ))
#     assert re.search("WARNING", run.stderr), "stderr should contain 'WARNING', was '{}'".format(run.stderr)


def test_call_barcodes_withN():
    "Call merge_pcr_duplicates.py with barcodes containing uncalled bases."
    infile = "pcr_dupes_sorted_2.bed"
    inlib = "pcr_dupes_randomdict_withN.fastq"
    outfile = "merged_pcr_dupes_withN.bed"
    env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        datadir_rel + infile,
        datadir_rel + inlib,
        "--outfile", outfile,
    )
    assert(cmp(
        testdir + outfile,
        datadir + "merged_pcr_dupes_withN.bed"
    ))


def test_call_empty_barcode_library():
    "Call merge_pcr_duplicates.py with empty barcode library."
    infile = "empty_file"
    inlib = "pcr_dupes_randomdict_withN.fastq"
    outfile = "empty_output.bed"
    env.run(
        bindir_rel + "merge_pcr_duplicates.py",
        datadir_rel + infile,
        datadir_rel + inlib,
        "--outfile", outfile,
        expect_stderr=True,
    )
    assert(cmp(
        testdir + outfile,
        datadir + "empty_file"
    ))
