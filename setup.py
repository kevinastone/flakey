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
    ],
    entry_points={
        'flake8.extension': [
            'B20 = flakey.checks:BannedFunctionChecker',
        ],
    },
)
