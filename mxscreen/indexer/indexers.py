#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 09:54:05 2020

@author: dkreitler
"""


from abc import ABC, abstractmethod
import os
import numpy as np
import subprocess
import json

class Indexer(ABC):
    
    @abstractmethod
    def setupEnvironment(self):
        pass
    
    @abstractmethod
    def createInputFiles(self):
        pass
    
    @abstractmethod
    def indexSingleFrame(self):
        pass
    
    @abstractmethod
    def writeReport(self):
        pass
    
    @abstractmethod
    def run(self):
        pass

class DialsIndexer(Indexer):
    
    def __init__(self, mxpath=None):
        
        self._mxpath = mxpath
        self._dirListIndex = []
        
        return
        
    def setupEnvironment(self):
        os.chdir(self._mxpath.runDir)
        return
    
    def createInputFiles(self): 
        
        self.setupEnvironment()
        
        if os.path.isfile("SPOT.XDS"):
            spotXDSArray = np.genfromtxt("SPOT.XDS")
            maxFrameNumber = int(spotXDSArray[:,2].max(axis=0))
            spotArray = np.zeros((maxFrameNumber,2))  
            subprocess.run(["dials.import",
                           "{}".format(self._mxpath.masterH5Path)]) 
            
            for frame in range(0,maxFrameNumber):
                frameCutLow = (spotXDSArray[:,2] >= frame)
                frameCutHigh = (spotXDSArray[:,2] < frame + 1)
                filter_ = frameCutLow*frameCutHigh
                spotXDSArrayFiltered = spotXDSArray[filter_]
                filteredRows, _ = spotXDSArrayFiltered.shape
                
                if filteredRows > 10:
                    spotArray[frame,:] = frame + 1, filteredRows
                    singleFrameDir = "{:06d}".format(frame)
                    self._dirListIndex.append(singleFrameDir)
                    os.mkdir(singleFrameDir)
                    os.chdir(singleFrameDir)
                    np.savetxt("SPOT.XDS", spotXDSArrayFiltered,
                               fmt='%1.2f %1.2f %1.2f %1.2f')
                    os.chdir(self._mxpath.runDir)
                    
        else:
            print("No SPOT.XDS file found in directory")
            print("Did a spotfinder run?")
            
        return
    
    def indexSingleFrame(self, dirName):
            os.chdir(dirName)
            subprocess.run(["dials.import_xds",
                            "method=reflections",
                            "SPOT.XDS"])
            process = subprocess.Popen(["dials.index",
                                        "../datablock.json",
                                        "spot_xds.pickle",
                                        "detector.fix=all",
                                        "beam.fix=all"])
            os.chdir("..")
            return process
    
    def run(self):
        
        self.setupEnvironment()
        self.createInputFiles()
        processList = []
        for dir_ in self._dirListIndex:
            processList.append(self.indexSingleFrame(dir_))   
        for process in processList:
            process.wait()
        return
    
    def runSlow(self):
        
        self.setupEnvironment()
        self.createInputFiles()
        for dir_ in self._dirListIndex:
            process = self.indexSingleFrame(dir_)
            process.wait()
        return
        
        
    def writeReport(self):
        
        with open("mx.index.log","w") as resultsFile:
        
            for dir_ in self._dirListIndex:
                experimentsJson = os.path.join(dir_, "experiments.json")
                if os.path.isfile(experimentsJson):
                    with open(experimentsJson) as jdata:
                        xtal = json.load(jdata)['crystal'][0]
                        a = xtal['real_space_a']
                        a = np.array(a)
                        a = np.sqrt((a*a).sum())
                        b = xtal['real_space_b']
                        b = np.array(b)
                        b = np.sqrt((b*b).sum())
                        c = xtal['real_space_c']
                        c = np.array(c)
                        c = np.sqrt((c*c).sum())            
                else:
                    a,b,c = -1,-1,-1
                    
                resultString = "{},{:0.2f},{:0.2f},{:0.2f}".format(dir_,a,b,c)
                print(resultString)
                resultsFile.writelines(resultString + "\n")
        return

    
