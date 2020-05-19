#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:54:57 2020

@author: dkreitler
"""


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mxscreen",
    version="0.0.1dev",
    author="Dale Kreitler",
    author_email="dkreitler@bnl.gov",
    description="Spotfinding and indexing of single frames from rasters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dalekreitler-bnl/mxscreen.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: GNU General Public",
    ],
    install_requires=['numpy'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            "mxscreen=mxscreen.scripts.mxpipeline:main"
            ]
    }
)