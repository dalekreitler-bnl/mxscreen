#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 09:46:46 2020

@author: dkreitler
"""



from mxscreen.spotfinder import spotfinders
from mxscreen.utils import mxpaths
import time

def main():
    mxpath = mxpaths.MxPath()
    spotfinder = spotfinders.DialsSpotFinder(mxpath)
    tic = time.perf_counter()
    spotfinder.run()
    toc = time.perf_counter()
    print(toc-tic, " : seconds")
    
    return

if __name__ == "__main__":
    main()