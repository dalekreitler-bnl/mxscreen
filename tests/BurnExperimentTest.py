
# -*- coding: utf-8 -*-
"""
25Jun2020

@author: dkreitler

30Jun2020
Compare dozor vs. dials spotfinder
one res shell, one psi wedge, 1-500 frames
dozor: 188.9 frame half-life
dials: 216 frame half-life
"""


from mxscreen.experimentparams import experimentparams as ep
import numpy as np
from mxscreen.burn import burner
import matplotlib.pyplot as plt
import os

def main():
    
    f1 = "/home/dale/Xray/mxscreen_test_data/1-JJ-A1_1/test01_23800_master.h5"
    f2 = "/home/dale/Xray/mxscreen_test_data/SPOT_BURN_PK_DOZOR.XDS"
    f3 = "/home/dale/Xray/mxscreen_test_data/BURN_SPOT_DOZOR.XDS"
    
    burnExperimentDials = burner.BurnExperiment(f2,
                                                f1,
                                                nResShells=1,
                                                resRangeAll=(2.66,2.95),
                                                nPsiWedges=1,
                                                psiRangeAll=(0,360),
                                                frameRangeAll=(0,500))
    burnExperimentDials.resBounds()
    burnExperimentDials.psiBounds()
    burnExperimentDials.rangesDictList()
    burnExperimentDials.spotGroupList()
    burnExperimentDials.fitSpotGroups()
    results = burnExperimentDials.experimentPlot()
    print(results)
    os.chdir("/home/dale/Xray/mxscreen_test_data")
    np.savetxt("protK_burn_dozor_ints.csv",
               burnExperimentDials._burnSpotGroupList[0]._intensityArray,
               delimiter=",")
    plt.plot(results[:,0],results[:,1],
             results[:,0],results[:,1],'bo')
    plt.ylabel('Half life as Frame no.')
    plt.xlabel('resolution bin number')
    plt.show()
    
    
    return

if __name__ == "__main__":
    main()