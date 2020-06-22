#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:18:17 2020

@author: dale
"""


from mxscreen.experimentparams import framereaders


def main():
    frameName = "/home/dkreitler/mxscreen_test_data/rasterImages/Lyso_13_r_Raster_792_master.h5"
    frameReaderFactory = framereaders.FrameReaderFactory()
    frameReader = frameReaderFactory.getFrameReader("hdf5")
    frameReader.loadFirstFrame(frameName)
    print(frameReader.getDetector())
    print(frameReader.getDetDistance())
    print(frameReader.getPixelSize())
    print(frameReader.getBeamx())
    print(frameReader.getBeamy())
    print(frameReader.getStartAngle())
    print(frameReader.getAngleIncrement())
    
if __name__ == "__main__":
    main()