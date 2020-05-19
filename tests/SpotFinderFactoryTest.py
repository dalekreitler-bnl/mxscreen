#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 15:41:55 2020

@author: dkreitler
"""


from mxscreen.spotfinder import spotfinders
from mxscreen.utils import mxpaths

def main():
    
    sff = spotfinders.SpotFinderFactory()
    
    sfDozor = sff.getSpotFinder("dozor")
    
    sfDials = sff.getSpotFinder("dials")
    
    mxpathDozor = mxpaths.MxPath()
    
    mxpathDials = mxpaths.MxPath()
    
    sfDozor._mxpath = mxpathDozor
    
    sfDials._mxpath = mxpathDials
    
    sfDozor.run()
    
    sfDials.run()
    
    return

if __name__ == "__main__":
    main()

"""
factory generates both dials and dozor spotfinders
writes to separate mxs_XX result directories
"""