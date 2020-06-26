
# -*- coding: utf-8 -*-
"""
25Jun2020

@author: dkreitler


"""


from mxscreen.experimentparams import experimentparams as ep
import numpy as np
from mxscreen.burn import burner
import matplotlib.pyplot as plt

def main():
    
    f1 = "/home/dale/Xray/mxscreen_test_data/1-JJ-A1_1/test01_23800_master.h5"
    f2 = "/home/dale/Xray/mxscreen_test_data/1-JJ-A1_1/mxs_01/SPOT.XDS"
    
    params = ep.ExperimentParams(firstFrame=f1)
    spotXDSArray1 = np.genfromtxt(f2)
    res = burner.SpotArrayPixToRes.pixToRes(spotXDSArray1, params)
    psi = burner.SpotArrayPixToRes.pixToPsi(spotXDSArray1, params)
    plt.hist(psi)
    plt.show()
    sf = burner.SpotFilter(spotXDSArray1, resArray=res, psiArray=psi)
    
    ranges = {'resRange': (1,2),
              'psiRange': (-0.1,0.1),
              'frameRange': (0,300),} #test kwarg input
    
    bsg = burner.BurnSpotGroup(sf,ranges)
    bsg.fitDecayModel()
    bsg._decayStrategy.plotSegments()
    print(bsg.modelHalfLife)
    return

if __name__ == "__main__":
    main()