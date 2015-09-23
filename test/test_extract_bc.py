import re
from filecmp import cmp
from scripttest import TestFileEnvironment

bindir = "bin/"
datadir = "test/data/"
testdir = "test/testenv_extract_bc/"
env = TestFileEnvironment(testdir)
# relative to test file environment
bindir_rel = "../../" + bindir
datadir_rel = "../../" + datadir


def test_call_without_parameters():
    "Call extract_bcs.py withouth any additional parameters."
    run = env.run(
        bindir_rel + "extract_bcs.py",
        expect_error=True
    )
    assert(re.search("too few arguments", run.stderr))


def test_illegal_bcpattern():
    "Check if extract_bcs.py reports illegal barcode pattern"
    run = env.run(
        bindir_rel + "extract_bcs.py",
        datadir_rel + "/reads.fastq",
        "ILLEGAL",
        expect_error=True
    )
    assert(run.returncode != 0)


def test_bcpattern_without_bc():
    "Check if extract_bcs.py complains about missing barcode nts in pattern."
    run = env.run(
        bindir_rel + "extract_bcs.py",
        datadir_rel + "reads.fastq",
        "NNNNNNN",
        expect_error=True
    )
    assert(run.returncode != 0)


def test_positional_args_only():
    "Extract and remove barcodes, print result to stdout."
    run = env.run(
        bindir_rel + "extract_bcs.py",
        datadir_rel + "reads.fastq",
        "XXXNNXXX",
    )
    with open(testdir + "stdout_only_positional_args.fastq", "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + "stdout_only_positional_args.fastq",
        datadir + "result.fastq"))


def test_positional_args_only_verbose():
    "Extract and remove barcodes with verbose switch enabled, print result to stdout."
    run = env.run(
        bindir_rel + "extract_bcs.py",
        datadir_rel + "reads.fastq",
        "XXXNNXXX",
        "--verbose",
        expect_error=True
    )
    with open(testdir + "stdout_only_positional_args.fastq", "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + "stdout_only_positional_args.fastq",
        datadir + "result.fastq"))


def test_positional_args_only_debug():
    "Extract and remove barcodes with debug switch enabled, print result to stdout."
    run = env.run(
        bindir_rel + "extract_bcs.py",
        datadir_rel + "reads.fastq",
        "XXXNNXXX",
        "--debug",
        expect_error=True
    )
    with open(testdir + "stdout_only_positional_args.fastq", "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + "stdout_only_positional_args.fastq",
        datadir + "result.fastq"))


def test_writing_fastq_to_file():
    "Extract and remove barcodes, write result to file."
    env.run(
        bindir_rel + "extract_bcs.py",
        datadir_rel + "reads.fastq",
        "XXXNNXXX",
        "--outfile", "outfile.fastq",
    )
    assert(cmp(
        testdir + "outfile.fastq",
        datadir + "result.fastq"))


def test_writing_bcs_to_file():
    "Extract and remove barcodes, write extracted barcodes to separate fastq file."
    env.run(
        bindir_rel + "extract_bcs.py",
        datadir_rel + "reads.fastq",
        "XXXNNXXX",
        "--bcs", "extracted_bcs.fa",
    )
    assert(cmp(
        testdir + "extracted_bcs.fa",
        datadir + "result.fa"
    ))
