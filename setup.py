#!/usr/bin/env python

from setuptools import setup, find_packages
import os
import whats


def extra_dependencies():
    import sys
    ret = []
    if sys.version_info < (2, 7):
        ret.append('argparse')
    return ret


def read(*names):
    values = dict()
    extensions = ['.txt', '.md']
    for name in names:
        value = ''
        for extension in extensions:
            filename = name + extension
            if os.path.isfile(filename):
                value = open(name + extension).read()
                break
        values[name] = value
    return values

long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(
    name='whats',
    version=whats.__version__,
    description='search the first result via the command line',
    long_description=long_description,
    keywords='whats help console command line ask',
    author='PengTao Shi',
    author_email='shispt18@gmail.com',
    url='https://github.com/shispt/whats',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'whats = whats.whats:main',
        ]
    },
    install_requires=[
        'requests',
        'lxml',
        'readability-lxml',
    ] + extra_dependencies(),
)
