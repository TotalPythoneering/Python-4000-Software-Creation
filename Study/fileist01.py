#!/usr/bin/env python3
# MISSION: The complete set of examples and source code for ''Python 4000: The
# Software Creation Process (Gig Success)''.
# STATUS: Public Release
# VERSION: 1.0.0
# NOTES: Project: https://github.com/TotalPythoneering/Python-4000-Software-Creation
# DATE: 2019-08-15 07:17:56
# FILE: fileist01.py
# AUTHOR: Randall Nagy
#
import os
import os.path
import sys
import datetime as dt

class Fileist:
    '''
    Scan a folder hierarchy, selecting the top 'n' set of
    older / newer files.
    '''
    def __init__(self, root='.', suffix=''):
        ''' The root folder to scan, as well as an ending
        character sequence to match.'''
        self.root = root
        self.results = []
        self.suffix = suffix.lower()

    def _cleanup(self):
        ''' Format the final date and time, and prep for next usage. '''
        results = []
        for result in self.results:
            ztime = dt.datetime.fromtimestamp(result[1])
            results.append([result[0], ztime.strftime("%Y-%m-%d, %H:%M")])
        self.results.clear()
        return results

    def _prime(self, file, mtime, newest):
        ''' Build the initial list, in the sorted order. '''
        if not self._prospect(file, mtime, newest):
            self.results.append((file, mtime))

    def _prospect(self, file, mtime, newest):
        ''' Add a file if it belongs in the sorted list.
        No list-size management takes place. False if
        the file is not added, else True.'''
        for ss, node in enumerate(self.results):
            should = node[1] < mtime                    
            if not newest:
                should = not should
            if should:
                self.results.insert(ss, (file, mtime))
                return True
        return False
                            
    def locate(self, max_=25, newest=True):
        ''' Single interface to file-location & collection activities. '''
        for root, dirs, nodes in os.walk(self.root):
            for node in nodes:
                match = node.lower()
                if not match.endswith(self.suffix):
                    continue
                file = root + os.path.sep + node
                try:
                    st = os.stat(file, follow_symlinks=False)
                except:
                    print('!', end='')
                    continue
                mtime = st.st_mtime
                if len(self.results) < max_:
                    self._prime(file, mtime, newest)
                    print('+', end='')
                elif self._prospect(file, mtime, newest):
                    print('.', end='')
                    if len(self.results) > max_:
                        self.results.pop(max_)
            sys.stdout.flush()
        print()
        return self._cleanup()

if __name__ == '__main__':
    ''' Official C.L.I. '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", type=int, help="Number to list.")
    parser.add_argument("-o", "--oldest", action='store_true', help="Oldest, not newest.")
    parser.add_argument("-s", "--suffix", help="File suffix (case ignored.)")
    parsed = parser.parse_args()
    if not parsed.list:
        parsed.list = 25
    if not parsed.suffix:
        parsed.suffix = ''
    walker = Fileist('.', suffix=parsed.suffix)
    for ss, info in enumerate(
            walker.locate(max_=parsed.list,
            newest=not parsed.oldest), 1):
        print(f'{ss}\t{info[1]} - {info[0]}')


