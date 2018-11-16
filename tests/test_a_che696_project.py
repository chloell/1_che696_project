#!/usr/bin/env python3
"""
Unit and regression test for the 1_che696_project package.
"""

# Import package, test suite, and other packages as needed
import sys
import unittest
from contextlib import contextmanager
from io import StringIO

#from matcalc import canvas
from a_che696_project.matcalc import main, parse_cmdline


class TestQuote(unittest.TestCase):
    def testNoArgs(self):
        test_input = []
        main(test_input)
        with capture_stdout(main, test_input) as output:
            self.assertTrue("Using the" in output)


    def testNoSolver(self):
        test_input = []
        main(test_input)
        with capture_stdout(main, test_input) as output:
            self.assertTrue("Using the Gauss method" in output)

    def testNotDiagDomMatrix(self):
        test_input = ["A"]
        parse_cmdline(test_input)
        with capture_stdout(main, test_input) as output:
            pass

    def testJacobi(self):
        pass

    def testGauss(self):
        pass

    def testSiedel(self):
        pass


# Utility functions

# From http://schinckel.net/2013/04/15/capture-and-test-sys.stdout-sys.stderr-in-unittest.testcase/
@contextmanager
def capture_stdout(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    out, sys.stdout = sys.stdout, StringIO()
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
    sys.stdout = out

@contextmanager
def capture_stderr(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    err, sys.stderr = sys.stderr, StringIO()
    command(*args, **kwargs)
    sys.stderr.seek(0)
    yield sys.stderr.read()
    sys.stderr = err