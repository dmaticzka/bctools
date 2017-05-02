from past.builtins import cmp
import re
from scripttest import TestFileEnvironment

bindir = "bin/"
datadir = "test/data/"
testdir = "test/testenv_remove_tail/"
env = TestFileEnvironment(testdir)
# relative to test file environment
bindir_rel = "../../" + bindir
datadir_rel = "../../" + datadir


def test_call_without_parameters():
    "Call remove_tail.py withouth any additional parameters."
    run = env.run(
        bindir_rel + "remove_tail.py",
        expect_error=True
    )
    assert(re.search("usage", run.stderr))


def test_invalid_length():
    "Call remove_tail.py with negative length."
    run = env.run(
        bindir_rel + "remove_tail.py",
        datadir_rel + "reads.fastq",
        -7,
        expect_error=True,
    )
    assert(run.returncode != 0)


def test_positional_args_only():
    "Remove nts from 3' tail, print result to stdout."
    run = env.run(
        bindir_rel + "remove_tail.py",
        datadir_rel + "readswithtail.fastq",
        7,
    )
    with open(testdir + "stdout_only_positional_args.fastq", "w") as b:
        b.write(run.stdout)
    assert(cmp(
        testdir + "stdout_only_positional_args.fastq",
        datadir + "readswithtailremoved.fastq"))


def test_writing_fastq_to_file():
    "Remove nts from 3' tail, write result to file."
    env.run(
        bindir_rel + "remove_tail.py",
        datadir_rel + "readswithtail.fastq",
        7,
        "--outfile", "outfile.fastq",
    )
    assert(cmp(
        testdir + "outfile.fastq",
        datadir + "readswithtailremoved.fastq"))
