#!/usr/bin/env python3
"""
Unit and regression test for the 1_che696_project package.
"""

# Import package, test suite, and other packages as needed
import sys
import unittest
from contextlib import contextmanager
from io import StringIO
import logging

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
DISABLE_REMOVE = logger.isEnabledFor(logging.DEBUG)

#from matcalc import canvas
from a_che696_project.matcalc import main, parse_cmdline


class TestProject(unittest.TestCase):

    def testNotEqualDimen(self):
        test_input = ['5,-2,3;-3,9,1;2,-1,-7', '1;2']
        parse_cmdline(test_input)
        with capture_stderr(main, test_input) as output:
            self.assertTrue("identical" in output)

    def testNoSolver(self): # Testing to see if Jacobi works as the default
        test_input = ['5,-2,3;-3,9,1;2,-1,-7', '1;2;3']
        parse_cmdline(test_input)
        with capture_stdout(main, test_input) as output:
            self.assertTrue("[ 0.57749612  0.45105771 -0.32800935]" in output)

    def testNotDiagDomMatrix(self): # Testing to see if the matrix is diagonally dominant
        test_input = ['1,1,1;2,3,5;4,0,5', '1;2;3']
        parse_cmdline(test_input)
        with capture_stderr(main, test_input) as output:
            self.assertTrue("diagonally dominant" in output)

    def testJacobi(self): # Testing to see if the Jacobi method yields the correct answer
        test_input = ["-s", "j", '5,-2,3;-3,9,1;2,-1,-7', '1;2;3']
        parse_cmdline(test_input)
        with capture_stdout(main, test_input) as output:
            self.assertTrue("[ 0.57749612  0.45105771 -0.32800935]" in output)

    def testGauss(self): # Testing to see if the Gauss method yields the correct answer
        test_input = ["-s", "g", '5,-2,3;-3,9,1;2,-1,-7', '1;2;3']
        parse_cmdline(test_input)
        with capture_stdout(main, test_input) as output:
            self.assertTrue("[ 0.57749612  0.45105771 -0.32800935]" in output)

    def testSiedel(self): # Testing to see if the Gauss-Siedel method yields the correct answer
        test_input = ["-s", "s", '5,-2,3;-3,9,1;2,-1,-7', '1;2;3']
        parse_cmdline(test_input)
        with capture_stdout(main, test_input) as output:
            self.assertTrue("[ 0.5776533   0.45030048 -0.32795644]" in output)


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