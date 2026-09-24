#!/usr/bin/env python3
# MISSION: The complete set of examples and source code for ''Python 4000: The
# Software Creation Process (Gig Success)''.
# STATUS: Public Release
# VERSION: 1.0.0
# NOTES: Project: https://github.com/TotalPythoneering/Python-4000-Software-Creation
# DATE: 2019-08-27 11:32:30
# FILE: tMain20190827.py
# AUTHOR: Randall Nagy
#
'''
A demonstration of how to test a CLI.
Strategy is to simply capture & comp
the results between a "primed" and a
"testing" invocation.
'''
import os
import sys

def mknode(folder, idate, ftype='.txt'):
    ''' Create a testable file / node. '''
    fn = folder + "/" + str(idate) + ftype
    with open(fn, 'w') as fh:
        print("Test file:" + fn, file=fh)
        return True
    return False

def make_test_nodes(folder):
    ''' Create a definitive testing folder. '''
    if not os.path.exists(folder):
        os.mkdir(folder)
        
    for idate in range(100, 200, 2):
        if not mknode(folder, idate):
            raise Exception("Node Creation Error.")
    for idate in range(210, 220, 3):
        if not mknode(folder, idate, '.dat'):
            raise Exception("Node Creation Error.")

def test_comp(zlines, zfile, debug=False):
    ''' Prime, then compare, testing results. '''
    if os.path.exists(zfile):
        with open(zfile, 'r') as fh:
            for ss, line in enumerate(fh.readlines()):
                now = zlines[ss].strip()
                then = line.strip()
                if debug: print(f'[{now}]\n[{then}]')
                if now != then:
                    raise Exception("Lines not equal: " + zfile)
        if debug: print("Testing success.")
    else:
        with open(zfile, 'w') as fh:
            for line in zlines:
                print(line.strip(), file=fh)
        print(f"Primed {zfile} - Next run will verify.")

def basic_tests(program, folder):
    ''' Test Official C.L.I. '''
    os.chdir(folder)
    # Test Case 0100: Test Defaults
    results = [*os.popen(program)]
    test_comp(results, "/study/0100.txt")
    # Test Case 0200: Test Newest List
    results = [*os.popen(program + ' -o')]
    test_comp(results, "/study/0200.txt")
    # Test Case 0300: Test Oldest List
    results = [*os.popen(program + ' -s dat')]
    test_comp(results, "/study/0300.txt")
    # Test Case 0400: Test Oldest List by Suffix
    results = [*os.popen(program + ' -o -s dat')]
    test_comp(results, "/study/0400.txt")
    # Test Case 0500: Test Newest List by Suffix
    results = [*os.popen(program + ' -s dat')]
    test_comp(results, "/study/0500.txt")


program = 'c:/study/fileist01.py'
folder  = 'c:/study/test_nodes'
# make_test_nodes(folder)
option = input("Test fileist01? <y/n>: ")
if option is 'y':
    basic_tests(program, folder)
else:
    print(f"Program {program} untested.", file=sys.stderr)



