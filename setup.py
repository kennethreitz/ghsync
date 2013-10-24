#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from distutils.core import setup



if sys.argv[-1] == "publish":
    os.system('python setup.py sdist upload')
    sys.exit()

required = ['github2', 'clint', 'requests', 'github3.py']


setup(
    name='ghsync',
    version='0.3.1',
    description='GitHub Syncer. Clones or Pulls all GitHub repos.',
    long_description=open('README.rst').read(),
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/kennethreitz/ghsync',
    packages= [
        'ghsync',
    ],
    install_requires=required,
    license='ISC',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
    entry_points={
        'console_scripts': [
            'ghsync = ghsync.core:run',
        ],
    }
)
