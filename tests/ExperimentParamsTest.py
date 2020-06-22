#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:22:44 2020

@author: dkreitler
"""

from mxscreen.experimentparams import experimentparams

def main():
    
    ep = experimentparams.ExperimentParams(firstFrame="/home/dkreitler/mxscreen_test_data/rasterImages/Lyso_13_r_Raster_792_master.h5")
    print(ep.detDistance)
    print(ep.pixelSize)
    print(ep.beamx)
    print(ep.beamy)
    return

if __name__ == "__main__":
    main()