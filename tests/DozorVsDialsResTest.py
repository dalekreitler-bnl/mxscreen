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
    
    f1 = "/Users/dkreitler/xray/mxscreen_test_data/proteinaseK_static_burn_center_24539_master.h5"
    f2 = "/Users/dkreitler/xray/mxscreen_test_data/SPOT_BURN_PK_DIALS.XDS"
    f3 = "/Users/dkreitler/xray/mxscreen_test_data/SPOT_BURN_PK_DOZOR.XDS"
    
    burnExperimentDials = burner.BurnExperiment(f2,
                                                f1,
                                                nResShells=10,
                                                resRangeAll=(1,5),
                                                nPsiWedges=1,
                                                psiRangeAll=(0,180),
                                                frameRangeAll=(2,175),
                                                decayStrategy="doubleExponential")

    burnExperimentDials.psiBounds()
    dialsBounds=burnExperimentDials.resBounds()
    print('dialsBounds',dialsBounds)
    boundsdict={'resBounds': dialsBounds}
    burnExperimentDozor = burner.BurnExperiment(f3,
                                                f1,
                                                nResShells=10,
                                                resRangeAll=(1,5),
                                                nPsiWedges=1,
                                                psiRangeAll=(270,360),
                                                frameRangeAll=(2,175),
                                                decayStrategy="doubleExponential",
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
             label='dials')
    plt.plot(resultsDozor[:,0],resultsDozor[:,1],'g-o',
             label='dozor')
    plt.legend()
    plt.ylabel('Half life as Frame no.')
    plt.xlabel('resolution bin number')
    plt.show()
    
    
    return

if __name__ == "__main__":
    main()