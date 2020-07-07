#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:17:15 2020

@author: dale
"""


from mxscreen.experimentparams import experimentparams as ep
import numpy as np
from mxscreen.burn import burner
import matplotlib.pyplot as plt

def main():
    
    f1 = "/home/dale/Xray/mxscreen_test_data/1-JJ-A1_1/test01_23800_master.h5"
    f2 = "/home/dale/Xray/mxscreen_test_data/SPOT_BURN_PK_NE_DOZOR.XDS"
    f3 = "/home/dale/Xray/mxscreen_test_data/SPOT_BURN_PK_DOZOR.XDS"
    
    burnExperimentDials = burner.BurnExperiment(f2,
                                                f1,
                                                nResShells=5,
                                                resRangeAll=(1.3,5),
                                                nPsiWedges=1,
                                                psiRangeAll=(0,360),
                                                frameRangeAll=(0,200))

    burnExperimentDials.psiBounds()
    dialsBounds=burnExperimentDials.resBounds()
    print('dialsBounds',dialsBounds)
    boundsdict={'resBounds': dialsBounds}
    burnExperimentDozor = burner.BurnExperiment(f3,
                                                f1,
                                                nResShells=5,
                                                resRangeAll=(1.3,5),
                                                nPsiWedges=1,
                                                psiRangeAll=(0,360),
                                                frameRangeAll=(0,200),
                                                **boundsdict)
    burnExperimentDozor.psiBounds()
    #burnExperimentDozor.resBounds()
    burnExperimentDials.rangesDictList()
    burnExperimentDozor.rangesDictList()
    burnExperimentDials.spotGroupList()
    burnExperimentDozor.spotGroupList()
    burnExperimentDials.fitSpotGroups()
    burnExperimentDozor.fitSpotGroups()
    resultsDials = burnExperimentDials.experimentPlot()
    resultsDozor = burnExperimentDozor.experimentPlot()
    print('dials results\n',resultsDials)
    print('dozor results\n',resultsDozor)
    plt.plot(resultsDials[:,0],resultsDials[:,1],'b-o',
             label='near-edge')
    plt.plot(resultsDozor[:,0],resultsDozor[:,1],'g-o',
             label='center')
    plt.legend()
    plt.ylabel('Half life as Frame no.')
    plt.xlabel('resolution bin number')
    plt.show()
    
    
    return

if __name__ == "__main__":
    main()