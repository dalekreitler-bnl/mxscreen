#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 18:29:25 2020

@author: dale
"""

import expparams

def main():
    frameName14 = "../burn_5ms_000002.cbf"
    reader = expparams.CbfReader(frameName=frameName14)
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