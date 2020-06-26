#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:03:09 2020

@author: dale
"""


from mxscreen.experimentparams import experimentparams as ep
import numpy as np
from mxscreen.burn import burner
from mxscreen.burn import decaystrategy
import matplotlib.pyplot as plt

def main():
    
    f1 = "/home/dale/Xray/mxscreen_test_data/1-JJ-A1_1/test01_23800_master.h5"
    f2 = "/home/dale/Xray/mxscreen_test_data/1-JJ-A1_1/mxs_01/SPOT.XDS"
    params = ep.ExperimentParams(firstFrame=f1)
    spotXDSArray1 = np.genfromtxt(f2)
    res = burner.SpotArrayPixToRes.pixToRes(spotXDSArray1, params)
    psi = burner.SpotArrayPixToRes.pixToPsi(spotXDSArray1, params)
    sf = burner.SpotFilter(spotXDSArray1, resArray=res, psiArray=psi)
    
    ranges = {'resRange': (1,50),
              'psiRange': (0.9,1.5),
              'frameRange': (0,800),
              'fakeRange': (100,200)} #test kwarg input
    
    fvs = sf.frameVsSpots(**ranges)
    fvi = sf.frameVsInt(**ranges)
    ds = decaystrategy.BayesianSegmentsDecay(fvi)
    ds.fitDecayModel()
    ds.plotSegments()
    print(ds.optimalSlope())
    print(ds._pwlf.calc_slopes())
    print(ds.fitIndices)
    print(ds._optimalSlope)
    print(ds.modelHalfLife)
    plt.figure()
    plt.plot(fvs[:,0],fvs[:,1])
    plt.xlabel('frame no.')
    plt.ylabel('Total no. of spots on frame')
    plt.show()
    
    return

if __name__ == "__main__":
    main()