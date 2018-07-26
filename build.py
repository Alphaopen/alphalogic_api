# -*- coding: utf-8 -*-

import sys
from subprocess import call

if __name__ == '__main__':
    ext = 'zip' if sys.platform == 'win32' else 'gztar'
    call(['python', 'setup.py', 'sdist', '--formats=' + ext, 'bdist_wheel'])

