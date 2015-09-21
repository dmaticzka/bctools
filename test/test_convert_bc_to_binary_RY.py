import re
from filecmp import cmp
from scripttest import TestFileEnvironment

datadir = "test/data/"
testdir = "test/testenv_convert_bc/"
env = TestFileEnvironment(testdir)
# relative to test file environment
datadir_rel = "../../" + datadir


def test_call_without_parameters():
    "Call tool withouth any additional parameters."
    run = env.run(
        "../../extract_bcs.py",
        expect_error=True
    )
    assert(re.search("too few arguments", run.stderr))


def test_call_fileout():
    "Call tool with infile and outfile."
    infile = "result.fa"
    outfile = "converted_bcs.fa"
    env.run(
        "../../convert_bc_to_binary_RY.py",
        datadir_rel + infile,
        "--outfile", outfile
    )
    assert(cmp(
        testdir + outfile,
        datadir + "converted_bcs.fa"
    ))


def test_call_stdout():
    "Call tool with infile."
    infile = "result.fa"
    outfile = "stdout_only_positional_args.fastq"
    run = env.run(
        "../../convert_bc_to_binary_RY.py",
        datadir_rel + infile
    )
    with open(testdir + outfile, "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + outfile,
        datadir + "converted_bcs.fa"
    ))
