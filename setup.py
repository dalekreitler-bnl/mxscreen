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
    description="Analysis of initial MX diffraction experiments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dalekreitler-bnl/mxscreen",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: MIT",
    ],
    install_requires=['numpy',
                      'GPyOpt',
                      'pwlf'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            "mxscreen_dozor=mxscreen.scripts.mxpipeline:mainDozor",
            "mxscreen_dozor_slow=mxscreen.scripts.mxpipeline:mainDozorSlow",
            "mxscreen_dials=mxscreen.scripts.mxpipeline:mainDials",
            ]
    }
)
