#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:50:05 2020

@author: dkreitler
"""

from mxscreen.pipeline import pipelines


def main():
    
    mxPipelineBuilder = pipelines.MxPipelineBuilder()
    
    mxPipelineDirector = pipelines.MxPipelineDirector(mxPipelineBuilder)
    
    mxPipelineDozor = mxPipelineDirector.getMxPipeline("dozor")
    
    mxPipelineDials = mxPipelineDirector.getMxPipeline("dials")
    
    mxPipelineDozor.run()
    
    mxPipelineDials.run()
    
    
if __name__ == "__main__":
    main()
    