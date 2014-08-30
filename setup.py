#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from flakey import __version__

setup(
    name='flakey',
    version=__version__,
    description='Custom flake8 rules for your projects',
    author='Kevin Stone',
    author_email='kevinastone@gmail.com',
    url='https://github.com/kevinastone/flakey',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'setuptools',
        'six',
    ],
    test_suite='tests',
    entry_points={
        'flake8.extension': [
            'B = flakey.checks:BannedFunctionChecker',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
