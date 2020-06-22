#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 18:29:25 2020

@author: dale
"""

from mxscreen.experimentparams import framereaders

def main():
    frameName14 = "/home/dkreitler/mxscreen_test_data/rasterImages/Lyso_13_r_Raster_792_master.h5"
    reader = framereaders.Hdf5Reader(frameName=frameName14)
    #load frame
    reader.loadFirstFrame(frameName14)
    detector = reader.getDetector()
    detDistance = reader.getDetDistance()
    pixelSize = reader.getPixelSize()
    wavelength = reader.getWavelength()
    beamx = reader.getBeamx()
    beamy = reader.getBeamy()
    exposureTime = reader.getExposureTime()
    startAngle = reader.getStartAngle()
    angleIncrement = reader.getAngleIncrement()
    
    print(detector)
    print(detDistance)
    print(pixelSize)
    print(wavelength)
    print(beamx)
    print(exposureTime)
    print(beamy)
    print(startAngle)
    print(angleIncrement)
    
    return

if __name__ == "__main__":
    main()