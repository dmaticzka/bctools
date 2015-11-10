import re
from filecmp import cmp
from scripttest import TestFileEnvironment

bindir = "bin/"
datadir = "test/data/"
testdir = "test/testenv_convert_bc/"
env = TestFileEnvironment(testdir)
# relative to test file environment
bindir_rel = "../../" + bindir
datadir_rel = "../../" + datadir


def test_call_without_parameters():
    "Call convert_bc_to_binary_RY.py withouth any additional parameters."
    run = env.run(
        bindir_rel + "convert_bc_to_binary_RY.py",
        expect_error=True
    )
    assert(re.search("too few arguments", run.stderr))


def test_call_fileout():
    "Call convert_bc_to_binary_RY.py with infile and outfile, read and write fastq format."
    infile = "extracted_bcs.fastq"
    outfile = "converted_bcs.fastq"
    env.run(
        bindir_rel + "convert_bc_to_binary_RY.py",
        datadir_rel + infile,
        "--outfile", outfile
    )
    assert(cmp(
        testdir + outfile,
        datadir + "converted_bcs.fastq"
    ))


def test_call_stdout():
    "Call convert_bc_to_binary_RY.py with infile, read and write fastq format."
    infile = "extracted_bcs.fastq"
    outfile = "stdout_only_positional_args.fastq"
    run = env.run(
        bindir_rel + "convert_bc_to_binary_RY.py",
        datadir_rel + infile
    )
    with open(testdir + outfile, "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + outfile,
        datadir + "converted_bcs.fastq"
    ))


def test_call_fileout_fasta():
    "Call convert_bc_to_binary_RY.py with infile and outfile, read and write fasta format."
    infile = "result.fa"
    outfile = "converted_bcs.fa"
    env.run(
        bindir_rel + "convert_bc_to_binary_RY.py",
        datadir_rel + infile,
        "--outfile", outfile,
        "--fasta-format",
    )
    assert(cmp(
        testdir + outfile,
        datadir + "converted_bcs.fa"
    ))


def test_call_stdout_fasta():
    "Call convert_bc_to_binary_RY.py with infile, read and write fasta format."
    infile = "result.fa"
    outfile = "stdout_only_positional_args.fa"
    run = env.run(
        bindir_rel + "convert_bc_to_binary_RY.py",
        datadir_rel + infile,
        "--fasta-format",
    )
    with open(testdir + outfile, "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + outfile,
        datadir + "converted_bcs.fa"
    ))
