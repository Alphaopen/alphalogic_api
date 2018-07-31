#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python stub library for Alphalogic adapters.
"""

import sys
import platform
from setuptools import setup


VERSION_MAJOR = 0  # (System version)
VERSION_MINOR = 0  # (Tests version)
BUILD_NUMBER = 6   # (Issues version)

ver = '%d.%d.%d' % (VERSION_MAJOR, VERSION_MINOR, BUILD_NUMBER)

cur = 'win32' if sys.platform == 'win32' else platform.linux_distribution()[0].lower()
ext = '.zip' if sys.platform == 'win32' else '.tar.gz'

bin_name = 'alphalogic_api-%s-%s%s' % (cur, ver, ext)


if __name__ == '__main__':

    with open('README.md', 'r') as fh:
        long_description = fh.read()

    setup(
        name='alphalogic_api',
        version=ver, 
        description=__doc__.replace('\n', '').strip(),
        long_description=long_description,
        author='Alphaopen',
        author_email='mo@alphaopen.com',
        url='https://github.com/Alphaopen/alphalogic_api',
        py_modules=['alphalogic_api'],
        include_package_data=True,
        packages=[
            'alphalogic_api',
            'alphalogic_api.objects',
            'alphalogic_api.protocol'
        ],
        classifiers=(
            "Programming Language :: Python :: 2.7",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        license='MIT',
        platforms=['linux2', 'win32'],
        install_requires=[
            'protobuf==3.6.0',
            'grpcio==1.12.1',
            'grpcio-tools==1.12.1',
        ],
    )
