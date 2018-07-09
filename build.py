# -*- coding: utf-8 -*-
import os
import sys
from subprocess import call

if __name__ == '__main__':
    cwd = os.getcwd()
    print 'Current working directory: ', cwd
    output_dir = os.path.join(cwd, 'Output')
    ext = 'zip' if sys.platform == 'win32' else 'gztar'
    call(['python', 'setup.py', 'sdist', '-d', output_dir, '--formats=' + ext])

