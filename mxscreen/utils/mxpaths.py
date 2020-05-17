#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 18:18:24 2020

@author: dkreitler
"""

import os

class MxPath:
    
    #run results go in MxPath.runDir
    
    def __init__(self):
        self._wdir = "/home/dkreitler/mxscreen_test_data/rasterImages"
        self._dirList = os.listdir("/home/dkreitler/mxscreen_test_data/rasterImages")
        self.masterH5 = [f for f in self._dirList if f.endswith("master.h5")][0]
        self.masterH5Path = os.path.join(self._wdir, self.masterH5)
        self.makeMxDirectory()
               
    def checkForMxDirectory(self):
        return any([f.startswith("mxs_") for f in self._dirList])
    
    def makeMxDirectory(self):
        if self.checkForMxDirectory():
            runNumber = sum([f.startswith("mxs_") for f in self._dirList]) + 1
            newRunDir = os.path.join(self._wdir,
                                     "mxs_{:02d}".format(runNumber))
            self.runDir = newRunDir
            os.mkdir(newRunDir)
        else:
            self.runDir = os.path.join(self._wdir,"mxs_01")
            os.mkdir(self.runDir)
        
    