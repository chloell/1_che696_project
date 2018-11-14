#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
matcalc.py
Solves systems of matrices using numerical methods

Handles the primary functions
"""

import sys
import argparse
import numpy as np
import math


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)

def residual(A, B, guess, row, col): #function that calculates the residual error each time a new iteration occurs
    build = 0
    for i in range(row):
        temp = B[i]
        for j in range(col):
            temp = temp - A[i,j]*guess[j]
        build += temp**2
    r = math.sqrt(build)
    return r

def gauss_siedel(A, B, row, col, w):
    if w != 1.0:
        function = print("Using the Gauss-Siedel method, the answer is:")
    else:
        function = print("Using the Gauss method, the answer is:")
    initial_guess = np.zeros(row)
    res = residual(A, B, initial_guess, row, col)
    x = initial_guess
    while res > 0.01: # the residual error must be less than this for the system to stop guessing and be considered converged
        for i in range(row):
            term = 0
            for j in range(col):
                if i != j:
                    term = term + A[i,j]*x[j]
            x[i] = (x[i] - w*x[i]) + (w/A[i,i])*(B[i] - term)
        res = residual(A, B, x, row, col)
    return function, x

def jacobi(A, B, row, col):
    function = print("Using the Jacobi method, the answer is:")
    initial_guess = np.zeros(row)
    res = residual(A, B, initial_guess, row, col)
    x = initial_guess
    while res > 0.01: # the residual error must be less than this for the system to stop guessing and be considered converged
        for i in range(row):
            term = 0
            for j in range(col):
                if i != j:
                    term = term + A[i,j]*x[j]
            x[i] = (B[i] - term)/A[i,i]
        res = residual(A, B, x, row, col)
    return function, x

def matrix_calculator(A, B, row, col, solver_type):
    if solver_type == "j": # J IS A PLACEHOLDER FOR COMMAND LINE PARSER "CHOICES" ISSUE RESOLUTION
        state, answer = jacobi(A, B, row, col)
    if solver_type == "g": # G IS A PLACEHOLDER FOR COMMAND LINE PARSER "CHOICES" ISSUE RESOLUTION
        w = 1.0
        state, answer = gauss_siedel(A, B, row, col, w)
    if solver_type == "s": # S IS A PLACEHOLDER FOR COMMAND LINE PARSER "CHOICES" ISSUE RESOLUTION
        w = 1.6 #this number was chosen because it is the most efficient number for Gauss-Siedel method, according to Dr. Nagrath
        state, answer = gauss_siedel(A, B, row, col, w)
    return state, answer

def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    #from Stackoverflow.com suggests this for storing command line inputs as an array:
    class Store_as_array(argparse._StoreAction):
        def __call__(self, parser, namespace, values, option_string=None):
            values = values.split(';')
            rows = len(values)
            m = values[0].split(',')
            i = 1
            while i < rows:
                n = values[i].split(',')
                m = np.vstack((m,n))
                i += 1
            rows, cols = m.shape
            #now " m" is the matrix that has everything in terms of a string
            # to convert everything to a string:
            newA = np.zeros((rows, cols))
            newB = np.zeros((rows))
            for j in range(rows):
                if cols != 0:
                    for k in range(cols):
                        newA[j,k] = float((m[j,k]))
                else:
                    newB[j] = float(m[j])
            if cols != 0:
                values = newA
            else:
                values = newB

            return super().__call__(parser, namespace, values, option_string)

    # initialize the parser object:
    parser = argparse.ArgumentParser()
    # parser.add_argument("-i", "--input_rates", help="The location of the input rates file",
    #                     default=DEF_IRATE_FILE, type=read_input_rates)
    #parser.add_argument("-n", "--no_attribution", help="Whether to include attribution",
                        # action='store_false')
    parser.add_argument("-s", "--solver", choices=("j","g", "s"),
                        help="Use these options to help you choose a solver: j for Jacobi, g for Gauss, s for Gauss-Siedel. Jacobi is the default.",
                        default="j")
    parser.add_argument("A", help="This is the main A matrix, as in Ax=B. Format as: '1,2,3;4,5,6;7,8,9' to create this, where ; separates the rows and , separates the columns. Make sure that the number of columns in this matrix A are the same as the number of rows in matrix B. THIS MATRIX MUST BE DIAGONALLY DOMINANT FOR THESE METHODS TO WORK!",
                        action=Store_as_array)
    parser.add_argument("B", help="This is the answer B matrix, as in Ax=B.  Format as: '1;2;3' to create this, where ; separates the rows. Make sure that the number of rows in this matrix A are the same as the number of columns in matrix A.",
                        action=Store_as_array)

    args = None
    dimen_test = None
    try: # makes sure that the Store_as_array function is working
        args = parser.parse_args(argv)
        assert isinstance(args.A, np.ndarray)
        assert isinstance(args.B, np.ndarray)
    except TypeError as t:
        warning("Type of values stored in A and B arrays are not the same:", t)
        parser.print_help()
        return args, 2

    try: # makes sure that the matrices have identical dimensions
        dimen_test = np.dot(args.A, args.B)
    except ValueError as v:
        warning("Matrices must have identical inside dimension:", v)
        parser.print_help()
        return dimen_test, 2

    return args, 0


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != 0:
        return ret
    #  print(canvas(args.no_attribution))
    m, n = np.shape(args.A)
    statement, answer = matrix_calculator(args.A, args.B, m, n, args.solver)
    statement
    print(answer)
    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
