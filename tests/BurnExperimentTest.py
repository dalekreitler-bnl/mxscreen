
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
    
    f1 = "/Users/dkreitler/xray/mxscreen_test_data/proteinaseK_static_burn_center_24539_master.h5"
    f2 = "/Users/dkreitler/xray/mxscreen_test_data/SPOT_BURN_PK_DIALS.XDS"
    f3 = "/home/dale/Xray/mxscreen_test_data/BURN_SPOT_DIALS.XDS"
    
    burnExperimentDials = burner.BurnExperiment(f2,
                                                f1,
                                                nResShells=8,
                                                resRangeAll=(1,10),
                                                nPsiWedges=1,
                                                psiRangeAll=(0,360),
                                                frameRangeAll=(1,200),
                                                decayStrategy="doubleExponential")
    burnExperimentDials.resBounds()
    burnExperimentDials.psiBounds()
    burnExperimentDials.rangesDictList()
    burnExperimentDials.spotGroupList()
    burnExperimentDials.fitSpotGroups()
    results = burnExperimentDials.experimentPlot()
    
    print(results)

    plt.plot(results[:,0],results[:,1],
             results[:,0],results[:,1],'bo')
    plt.ylabel('Half life (Frame no.)')
    plt.xlabel('resolution bin number')
    plt.title("Decay rate versus spot resolution")
    plt.show()
    
    
    return

if __name__ == "__main__":
    main()