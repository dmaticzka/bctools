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
    "Call convert_bc_to_binary_RY.py with infile and outfile."
    infile = "result.fa"
    outfile = "converted_bcs.fa"
    env.run(
        bindir_rel + "convert_bc_to_binary_RY.py",
        datadir_rel + infile,
        "--outfile", outfile
    )
    assert(cmp(
        testdir + outfile,
        datadir + "converted_bcs.fa"
    ))


def test_call_stdout():
    "Call convert_bc_to_binary_RY.py with infile."
    infile = "result.fa"
    outfile = "stdout_only_positional_args.fastq"
    run = env.run(
        bindir_rel + "convert_bc_to_binary_RY.py",
        datadir_rel + infile
    )
    with open(testdir + outfile, "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + outfile,
        datadir + "converted_bcs.fa"
    ))
