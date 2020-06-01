#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 10:35:54 2020

@author: dkreitler
"""


from mxscreen.pipeline import pipelines


def mainDozor():
    
    mxPipelineBuilder = pipelines.MxPipelineBuilder()
    mxPipelineDirector = pipelines.MxPipelineDirector(mxPipelineBuilder)
    mxPipelineDozor = mxPipelineDirector.getMxPipeline("dozor")
    mxPipelineDozor.run()
    return

def mainDials():

    mxPipelineBuilder = pipelines.MxPipelineBuilder()
    mxPipelineDirector = pipelines.MxPipelineDirector(mxPipelineBuilder)
    mxPipelineDials = mxPipelineDirector.getMxPipeline("dials")
    mxPipelineDials.run()
    return
