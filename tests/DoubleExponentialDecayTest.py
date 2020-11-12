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
    
    f1 = "/Users/dkreitler/xray/mxscreen_test_data/1-JJ-A1_1/test01_23800_master.h5"
    f2 = "/Users/dkreitler/xray/mxscreen_test_data/1-JJ-A1_1/mxs_01/SPOT.XDS"
    params = ep.ExperimentParams(firstFrame=f1)
    spotXDSArray1 = np.genfromtxt(f2)

    res = burner.SpotArrayPixToRes.pixToRes(spotXDSArray1, params)
    psi = burner.SpotArrayPixToRes.pixToPsi(spotXDSArray1, params)
    sf = burner.SpotFilter(spotXDSArray1, resArray=res, psiArray=psi)
    
    ranges = {'resRange': (1,2),
              'psiRange': (0,180), #degrees
              'frameRange': (45,600),}
    
    fvs = sf.spotsVsFrame(**ranges)
    fvi = sf.intVsFrame(**ranges)
    ds = decaystrategy.DoubleExponentialDecay(fvi)
    ds.fitDecayModel()
    ds.plotSegments()
    print(ds._modelParams)
    print(ds.modelHalfLife)

    
    return

if __name__ == "__main__":
    main()