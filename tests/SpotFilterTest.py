
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:07:25 2020

@author: dkreitler

resolution filter and psi angle filter work
19Jun2020

Can filter based on spot threshold, resolution, psi
histogram of psi angles is good sanity check
19Jun2020
"""


from mxscreen.experimentparams import experimentparams as ep
import numpy as np
from mxscreen.burn import burner
import matplotlib.pyplot as plt
import os

def main():
    f1 = "/GPFS/CENTRAL/xf17id2/dkreitler/1-JJ-A1_1/test01_23800_master.h5"
    f2 = "/GPFS/CENTRAL/xf17id2/dkreitler/1-JJ-A1_1/mxs_01/SPOT.XDS"
    params = ep.ExperimentParams(firstFrame=f1)
    spotXDSArray1 = np.genfromtxt(f2)
    res = burner.SpotArrayPixToRes.pixToRes(spotXDSArray1, params)
    psi = burner.SpotArrayPixToRes.pixToPsi(spotXDSArray1, params)
    sf = burner.SpotFilter(spotXDSArray1, resArray=res, psiArray=psi)
    fvs = sf.frameVsSpots((1,50),(0,0.5))
    fvi = sf.frameVsInt(resRange=(1,50),psiRange=(-0.1,0.1))
    plt.plot(fvi[:,0],np.log(fvi[:,1]),marker='o')
    plt.show()
    os.chdir('/GPFS/CENTRAL/xf17id2/dkreitler/1-JJ-A1_1/')
    np.savetxt("test_int.txt",fvi)
    return

if __name__ == "__main__":
    main()