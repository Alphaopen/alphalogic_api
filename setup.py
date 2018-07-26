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
BUILD_NUMBER = 4   # (Issues version)

stub_version = '%d.%d.%d' % (VERSION_MAJOR, VERSION_MINOR, BUILD_NUMBER)

cur = 'win32' if sys.platform == 'win32' else platform.linux_distribution()[0].lower()
ext = '.zip' if sys.platform == 'win32' else '.tar.gz'

bin_name = 'alphalogic_api-%s-%s%s' % (cur, stub_version, ext)


if __name__ == '__main__':
    setup(
        name='alphalogic_api',
        version=stub_version,
        description=__doc__.replace('\n', '').strip(),
        author='Alphaopen LLC',
        author_email='www.alphaopen.com',
        url='http://www.alphaopen.com/',
        py_modules=['alphalogic_api'],
        include_package_data=True,
        packages=[
            'alphalogic_api',
            'alphalogic_api.objects',
            'alphalogic_api.protocol'
        ],
        license='Commercial',
        platforms=['linux2', 'win32'],
        install_requires=[
            'protobuf==3.6.0',
            'grpcio==1.12.1',
            'grpcio-tools==1.12.1',
        ],
    )
