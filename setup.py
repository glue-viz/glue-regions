#!/usr/bin/env python

from __future__ import print_function

from setuptools import setup, find_packages

entry_points = """
[glue.plugins]
glue-regions=glue-regions:setup
"""

with open('README.rst') as infile:
    LONG_DESCRIPTION = infile.read()

with open('glue-regions/version.py') as infile:
    exec(infile.read())

setup(name='glue-regions',
      version=__version__,
      description='astropy regions support for glue',
      long_description=LONG_DESCRIPTION,
      url="https://github.com/glue-viz/glue-plugin-template",
      author='',
      author_email='',
      packages = find_packages(),
      package_data={},
      entry_points=entry_points
    )
