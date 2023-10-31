#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
import shutil
import glob
import sys


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


if not os.path.exists('build'):
    os.mkdir('build')

setup(
    name="pyuscope-kitchen",
    version="4.4.0",
    author="John McMaster",
    author_email='john@labsmore.com',
    description=("pyuscope community plugins"),
    license="BSD",
    keywords="microscope",
    url='https://github.com/Labsmore/pyuscope-kitchen',
    packages=find_packages(exclude=['build']),
    # FIXME
    install_requires=[],
    long_description="FIXME",
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)
