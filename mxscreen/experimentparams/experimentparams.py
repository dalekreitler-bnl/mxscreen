#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:44:35 2020

@author: dale
"""

from mxscreen.experimentparams import framereaders

class ExperimentParamsBuilder:
 

class ExperimentParams:
    
    def __init__(self, frameFormat="cbf", firstFrame):
        
        self._frameFormat = frameFormat
        self._firstFrame = firstFrame
        
    def loadFrameReader(self):
        self._frameReader = framereaders.FrameReaderFactory(self._frameFormat)
        
    def loadFirstFrame(self):
        self._frameReader.loadFirstFrame(firstFrame)
        
    def loadExperimentParams(self):
        self.detector = self._frameReader.getDetector()
        self.detDistance = self._frameReader.getDetDistance()
        self.pixelSize = self._frameReader.getPixelSize()
        self.beamx = self._frameReader.getBeamx()
        self.beamy = self._frameReader.getBeamy()
        self.startAngle = self._frameReader.getStartAngle()
        self.angleIncrement = self._frameReader.getAngleIncrement()
        