#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 16:12:21 2020

@author: dkreitler
"""


from mxscreen.spotfinder import spotfinders
from mxscreen.utils import mxpaths
from mxscreen.indexer import indexers
from abc import ABC, abstractmethod


class MxPipelineDirector:
    
    _builder = None
    
    def __init__(self, builder):
        self._builder = builder
        
    def getMxPipeline(self, spotFinderFormat="dozor"):
        
        mxPipeline = MxPipeline()
        
        #define mxpath
        mxPath = self._builder.getPaths()
        mxPipeline.setPaths(mxPath)
        
        #set spot finder, give spot finder mxPath
        spotFinder = self._builder.getSpotFinder(spotFinderFormat)
        spotFinder._mxpath = mxPath
        mxPipeline.setSpotFinder(spotFinder)
        
        #set indexer, give indexer mxPath
        indexer = self._builder.getIndexer()
        indexer._mxpath = mxPath
        mxPipeline.setIndexer(indexer)
        
        return mxPipeline
        
class MxPipeline:
    
    def __init__(self):
        self._mxPath = None
        self._spotFinder = None
        self._indexer = None
        
    def setPaths(self, mxPath):
        self._mxPath = mxPath
        
    def setSpotFinder(self, spotFinder):
        self._spotFinder = spotFinder
        
    def setIndexer(self, indexer):
        self._indexer = indexer
        
    def makeSpotFile(self):
        self._spotFinder.run()
        
    def run(self):
        self._spotFinder.run()
        self._indexer.run()
        self._indexer.writeReport()
        
    def runSlow(self):
        self._spotFinder.run()
        self._indexer.runSlow()
        self._indexer.writeReport()
    

class Builder:
    
    def getPaths(self):
        pass
    
    def getSpotFinder(self, spotFinderFormat):
        pass
    
    def getIndexer(self):
        pass

    def getAnalyzer(self):
        pass


class MxPipelineBuilder(Builder):
    
    def getPaths(self):
        return mxpaths.MxPath()
    
    def getSpotFinder(self, spotFinderFormat):
        spotFinderFactory = spotfinders.SpotFinderFactory()
        spotFinder = spotFinderFactory.getSpotFinder(spotFinderFormat)
        return spotFinder
    
    def getIndexer(self):
        return indexers.DialsIndexer()
    
    def getAnalyzer(self):
        pass
    

