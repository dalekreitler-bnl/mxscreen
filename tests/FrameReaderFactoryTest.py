#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:18:17 2020

@author: dale
"""


from mxscreen.experimentparams import framereaders


def main():
    frameName = "burn_5ms_000002.cbf"
    frameReaderFactory = framereaders.FrameReaderFactory()
    frameReader = frameReaderFactory.getFrameReader("cbf")
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