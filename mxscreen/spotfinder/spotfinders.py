#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:00:56 2020

@author: dkreitler
"""


from abc import ABC, abstractmethod
import subprocess
import os
import numpy as np


class SpotFinder(ABC):
    
    @abstractmethod
    def setupEnvironment(self):
        pass
    
    @abstractmethod
    def createInputFiles(self):
        pass
    
    @abstractmethod
    def generateSpotXDS(self):
        pass
    
    @abstractmethod
    def runSpotFinder(self):
        pass
    
    @abstractmethod
    def run(self):
        pass


class SpotFinderFactory:
    
    def getSpotFinder(self, spotFinder="dozor"):
        
        if spotFinder == "dozor" or spotFinder == "Dozor":
            return DozorSpotFinder()
    
        elif spotFinder == "dials" or spotFinder == "Dials":
            return DialsSpotFinder()
        
        else:
            print("Currently only supporting dozor or dials spotfinders")
            raise ValueError(spotFinder)
            
        return
        

class DozorSpotFinder(SpotFinder):
    
    """
    run dozor_par; convert to SPOT.XDS
    """
    
    def __init__(self, mxpath=None):
        self._mxpath = mxpath
        
    def setupEnvironment(self):
        os.chdir(self._mxpath.runDir)
        return
        
    def createInputFiles(self):
        print(self._mxpath.masterH5Path)
        subprocess.run(["env \
                        LD_LIBRARY_PATH=/usr/local/crys-local/ccp4-7.0/lib \
                        eiger2params {} \
                        > dozor.dat".format(self._mxpath.masterH5Path)],
                        shell=True)
        return
        
    def runSpotFinder(self):
        subprocess.run(["env",
                        "LD_LIBRARY_PATH=/usr/local/crys-local/ccp4-7.0/lib",
                        "dozor_par",
                        "-p",
                        "dozor.dat"])
        return
    
    def generateSpotXDS(self):
        
        def saveSpotXDSArrayToFile(fileHandle, spotXDSArray):
            if spotXDSArray.size == 0:
                pass
            else:
                np.savetxt(fileHandle,
                           spotXDSArray,
                           fmt='%1.2f %1.2f %1.2f %1.2f')
                return
            
        def dozortoSpotXDSArray(fileName, nSpotMin=5):
            npArray = np.genfromtxt(fileName, skip_header=3)
            #reformat with dummy z coord. because only one frame
            frameNumber = parseSpotFileName(fileName)
            if len(npArray) > nSpotMin:
                spotXDSArray = np.c_[npArray[:,1],
                                     npArray[:,2],
                                     np.ones(len(npArray[:,2]))*frameNumber,
                                     npArray[:,3]]
            else:
                spotXDSArray = np.array([])
            return spotXDSArray, frameNumber
        
        def parseSpotFileName(fileName):
            frameNumber = fileName[0:5]
            return int(frameNumber)

        if os.path.isfile("SPOT.XDS"):
            os.remove("SPOT.XDS")
    
        for fileName in os.listdir(self._mxpath.runDir):
            if fileName.endswith("spot"):
                print(fileName)
                spotXDSArray, _ = dozortoSpotXDSArray(fileName)
                with open("SPOT.XDS","a") as spotFile:
                    saveSpotXDSArrayToFile(spotFile, spotXDSArray)
                os.remove(fileName)
        return
    
    def run(self):
        self.setupEnvironment()
        self.createInputFiles()
        self.runSpotFinder()
        self.generateSpotXDS()
        return
    
        
class DialsSpotFinder(SpotFinder):
    """
    run dials.find_spots; convert to SPOT.XDS
    """
    
    def __init__(self, mxpath=None):
        self._mxpath = mxpath
        
    def setupEnvironment(self):
        os.chdir(self._mxpath.runDir)
        return
        
    def createInputFiles(self):
        pass
        
    def runSpotFinder(self):
        subprocess.run(["dials.find_spots",
                        "{}".format(self._mxpath.masterH5Path),
                        "nproc=24"])
        return
    
    def runSpotFinder(self,nproc=24):
        subprocess.run(["dials.find_spots",
                        "{}".format(self._mxpath.masterH5Path),
                        "nproc={}".format(nproc)])
    
    def generateSpotXDS(self):
        subprocess.run(["dials.export",
                        "format=xds",
                        "strong.pickle"])
        subprocess.run(["mv",
                        "xds/SPOT.XDS",
                        "."])
        os.rmdir("xds")
        return
    
    def run(self):
        self.setupEnvironment()
        self.runSpotFinder()
        self.generateSpotXDS()
        return
        
        
