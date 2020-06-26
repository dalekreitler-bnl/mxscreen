
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
    
    burnExperiment = burner.BurnExperiment(f2,f1,nResShells=20,nPsiWedges=1,
                                           frameRangeAll=(100,500))
    burnExperiment.bounds()
    burnExperiment.rangesDictList()
    burnExperiment.spotGroupList()
    burnExperiment.fitSpotGroups()
    
    
    return

if __name__ == "__main__":
    main()