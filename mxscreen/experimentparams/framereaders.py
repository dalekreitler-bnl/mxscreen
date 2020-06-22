#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 16:14:46 2020

@author: dale
"""
from abc import ABC, abstractmethod
import subprocess
import h5py

class FrameReader(ABC):
    
    @abstractmethod
    def loadFirstFrame(self):
        pass
    
    @abstractmethod
    def getDetector(self):
        pass
    
    @abstractmethod
    def getDetDistance(self):
        pass
    
    @abstractmethod
    def getPixelSize(self):
        pass
    
    @abstractmethod
    def getExposureTime(self):
        pass
    
    @abstractmethod
    def getWavelength(self):
        pass
    
    @abstractmethod
    def getBeamx(self):
        pass
    
    @abstractmethod
    def getBeamy(self):
        pass
    
    @abstractmethod
    def getStartAngle(self):
        pass
    
    @abstractmethod
    def getAngleIncrement(self):
        pass

class FrameReaderFactory:
    
    @classmethod
    def getFrameReader(self, frameFormat):
        if frameFormat == "cbf":
            return CbfReader()
        elif frameFormat == "hdf5":
            return Hdf5Reader()
        else:
            raise ValueError(frameFormat)
        
class CbfReader(FrameReader):
    
    def __init__(self, frameName=None):
        self._frameName = frameName
        
    def loadFirstFrame(self, frameName):
        self._frameName = frameName
        self._frameHead = subprocess.run(['head',
                                          '-19',
                                          '{}'.format(self._frameName)],
                                         stdout=subprocess.PIPE)
        
    def getParamString(self, paramName, paramIndex):
        paramLine = subprocess.run(['grep',
                                      paramName],
                                     input=self._frameHead.stdout,
                                     stdout=subprocess.PIPE)
        paramString = paramLine.stdout.decode().split()[paramIndex]
        return paramString
        
    def getDetector(self):
        paramString = subprocess.run(['grep',
                                      'Detector'],
                                     input=self._frameHead.stdout,
                                     stdout=subprocess.PIPE)
        detectorStringList = paramString.stdout.decode().split()
        detectorModel1 = detectorStringList[3].lower()
        detectorModel2 = detectorStringList[4].lower()[0:2]
        detectorString = detectorModel1 + ' ' + detectorModel2
        return detectorString
    
    def getDetDistance(self):
        paramString = self.getParamString('Detector_distance', 2)
        detDistance = float(paramString)
        detDistance *= 1000
        return detDistance
    
    def getPixelSize(self):
        paramString = self.getParamString('Pixel_size', 2)
        pixelSize = float(paramString)
        return pixelSize
    
    def getExposureTime(self):
        paramString = self.getParamString('Exposure_time', 2)
        exposureTime = float(paramString)
        return exposureTime
    
    def getWavelength(self):
        paramString = self.getParamString('Wavelength', 2)
        wavelength = float(paramString)
        return wavelength
    
    def getBeamx(self):
        paramString = self.getParamString('Beam_xy', 2)
        beamx = float(paramString[1:8])
        return beamx
    
    def getBeamy(self):
        paramString = self.getParamString('Beam_xy', 3)
        beamy = float(paramString[0:7])
        return beamy
    
    def getStartAngle(self):
        paramString = self.getParamString('Start_angle', 2)
        startAngle = float(paramString)
        return startAngle
        
    def getAngleIncrement(self):
        paramString = self.getParamString('Angle_increment', 2)
        angleIncrement = float(paramString)
        return angleIncrement
    
class Hdf5Reader(FrameReader):
    
    def __init__(self, frameName=None):
        self._masterFrame = frameName
        
    def loadFirstFrame(self, masterFrame):
        f = h5py.File(masterFrame,'r')
        self._h5DetectorGroup = f['entry/instrument/detector']
        self._h5BeamGroup = f['entry/instrument/beam']
        
    def getDetector(self):
        detectorString = self._h5DetectorGroup['description'][()].decode()[8:]
        detectorString = detectorString.lower()
        return detectorString
    
    def getDetDistance(self):
        return self._h5DetectorGroup['detector_distance'][()]*1000
    
    def getPixelSize(self):
        return 1000*self._h5DetectorGroup['x_pixel_size'][()]
    
    def getExposureTime(self):
        pass
    
    def getWavelength(self):
        return self._h5BeamGroup['incident_wavelength'][()]
    
    def getBeamx(self):
        return self._h5DetectorGroup['beam_center_x'][()]
    
    def getBeamy(self):
        return self._h5DetectorGroup['beam_center_y'][()]
    
    def getStartAngle(self):
        pass
    
    def getAngleIncrement(self):
        pass
    
    