#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from GNSSTools import __version__


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# the setup
setup(
    name='GNSSTools',
    version=__version__,
    description='An automatic testing toolchain for GNSS receivers',
    long_description=read('README'),
    url='https://github.com/tutgnss/GNSS_visualization_tools',
    authors='A-Mari','Yanickdefrance'
    license='MIT',
    keywords='GNSS simulators receivers ',
    packages=find_packages(exclude=('docs', 'tests', 'env')),
    include_package_data=True,
    install_requires=[
    ],
    extras_require={
    'dev': [],
    'docs': [],
    'testing': [],
    },
    classifiers=[],
    )