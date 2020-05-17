#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 12:39:24 2020

@author: dkreitler
"""


from mxscreen.spotfinder import spotfinders
from mxscreen.utils import mxpaths
from mxscreen.indexer import indexers
import time

def main():
    
    mxpath = mxpaths.MxPath()
    
    spotfinder = spotfinders.DozorSpotFinder(mxpath)
    
    t1 = time.perf_counter()
    
    spotfinder.run()
    
    t2 = time.perf_counter()
    
    spotfinderTime = t2 - t1

    dialsindexer = indexers.DialsIndexer(mxpath)

    t3 = time.perf_counter()

    dialsindexer.run()
    
    t4 = time.perf_counter()
    
    indexerTime = t4-t3
    
    dialsindexer.writeReport()
    
    return spotfinderTime, indexerTime

if __name__ == "__main__":
    
    t1 = time.perf_counter()
    
    spotfinderTime, indexerTime = main()
    
    t2 = time.perf_counter()
    
    print(spotfinderTime, ": seconds - spotfind")
    print(indexerTime, ": seconds - index")
    print(t2-t1,": seconds - total")