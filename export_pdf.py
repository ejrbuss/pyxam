#!/usr/bin/env python3
# Author: Eric Buss <ebuss@ualberta.ca>

import os as _os
import shutil as _shutil
import subprocess as _subprocess

import pyxam as _pyxam

def export(file, temp, out):
    args = ['pdflatex', file]
    _subprocess.call(args, cwd=temp)
    try:
        file = file.replace('.tex', '.pdf')
        _shutil.copy(temp + '/' + file, out + '/' + file) 
    except FileNotFoundError:
        print('bash call ', args, ' failed')

if __name__ == '__main__':
    print('This is a library file. Use pyxam.py')
    exit()
