# -*- coding: utf-8 -*-

import os
import sys
import shutil
from subprocess import call


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise Exception


if __name__ == '__main__':

    # remove previous build
    if os.path.exists('dist'):
        shutil.rmtree('dist', onerror=onerror)

    #
    ext = 'zip' if sys.platform == 'win32' else 'gztar'
    call(['python', 'setup.py', 'sdist', '--formats=' + ext, 'bdist_wheel'])

    # remove service directories
    for d in ['build', 'alphalogic_api.egg-info']:
        if os.path.exists(d):
            shutil.rmtree(d, onerror=onerror)