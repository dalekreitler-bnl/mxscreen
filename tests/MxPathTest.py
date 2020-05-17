#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:42:11 2020

@author: dkreitler
"""


"mxs_XX directory passed test"

from mxscreen.utils import mxpaths

def main():
    mxpath = mxpaths.MxPath()
    print(mxpath.runDir)
    
if __name__=="__main__":
    main()