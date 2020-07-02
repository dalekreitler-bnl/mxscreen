# -*- coding: utf-8 -*-



import numpy as np
from mxscreen.burn import decaystrategy as ds
from mxscreen.experimentparams import experimentparams as ep

class SpotArrayPixToRes:
    
    '''
    tools for converting x,y pixel coordinates to polar coordinates for
    resolution and/or psi filtering, psi corresponds to detector surface
    polar coordinates.
    '''
    
    @classmethod
    def reCenter(cls, spotXDSArray, experimentParams):
        xyPixArray = np.zeros(spotXDSArray[:,0:2].shape)
        xyPixArray[:,0] = spotXDSArray[:,0] - experimentParams.beamx
        xyPixArray[:,1] = spotXDSArray[:,1] - experimentParams.beamy
        return xyPixArray
      
    @classmethod
    def pixTomm(cls, npArray, experimentParams):
        npArray[:,0] *= experimentParams.pixelSize
        npArray[:,1] *= experimentParams.pixelSize
        return npArray
        
    @classmethod
    def xyToRes(cls, xyArray, experimentParams):
        d = experimentParams.detDistance
        w = experimentParams.wavelength
        r = np.sqrt(xyArray[:,1]**2 + xyArray[:,0]**2)
        return w/(2*np.sin(0.5*np.arctan(r/d)))
    
    @classmethod
    def pixToRes(cls, spotXDSArray, experimentParams):
        spotXDSArray = SpotArrayPixToRes.reCenter(spotXDSArray,
                                                  experimentParams)
        spotXDSArray = SpotArrayPixToRes.pixTomm(spotXDSArray,
                                                 experimentParams)
        r = SpotArrayPixToRes.xyToRes(spotXDSArray,
                                      experimentParams)
        return r
    
    @classmethod
    def pixToPsi(cls, spotXDSArray, experimentParams):
        rcArray = SpotArrayPixToRes.reCenter(spotXDSArray,
                                             experimentParams)
        psi = np.arctan2(rcArray[:,1],rcArray[:,0])*180/np.pi
        psi[psi < 0] = 360 + psi[psi < 0]
        return psi

class SpotFilter:
    
    '''
    requires SPOT.XDS numpy array and either resolution or psi arrays for
    creating mask, the resolution array is computed from x,y detector
    coordinates, spotsVsFrame, intVsFrame will output Nx2 array on a per frame
    basis (N number of frames), filtered by resolution and/or psi angle.
    Resolution or psi range tuple units must be consistent with corresponding
    resolution or psi array.
    
    methods frameVsSpots and frameVsInts can also filter arrays based on
    number of spots; for removing weak data from end of burn, could be helpful
    for subsequent decay rate modeling
    '''
    
    def __init__(self,
                 spotXDSArray=None,
                 resArray=None,
                 psiArray=None,):
    
        self._spotXDSArray = spotXDSArray
        self._resArray = resArray
        self._psiArray = psiArray
    
    def spotMask(self, **kwargs):
        
        mask = np.ones(len(self._spotXDSArray), dtype=bool)
        
        if kwargs['resRange']:
            r = self._resArray
            mask *= (r > kwargs['resRange'][0])*(r < kwargs['resRange'][1])
            
        if kwargs['psiRange']:
            psi = self._psiArray
            mask *= (psi > kwargs['psiRange'][0])* \
                    (psi < kwargs['psiRange'][1])
            
        if kwargs['frameRange']:
            frames = self._spotXDSArray[:,2]
            mask *= (frames > kwargs['frameRange'][0])* \
                    (frames < kwargs['frameRange'][1])
        return mask
    
    def applyMask(self, mask):
        
        spots = self._spotXDSArray[mask,:]
        filteredSpotXDSArray = spots[np.argsort(spots[:,2]),:]
        return filteredSpotXDSArray
    
    def spotsVsFrame(self, spotThreshold=5, **kwargs):

        mask = self.spotMask(**kwargs)
        spots = self.applyMask(mask)
        frameNumber, nSpots = np.unique(spots[:,2],return_counts=True)
        return np.asarray((frameNumber,nSpots)).T[nSpots > spotThreshold,:]
    
    def intVsFrame(self, spotThreshold=5, **kwargs):
   
        #need to sort by frame no. column, then sum rows with same frame no.
        spotMask = self.spotMask(**kwargs)
        spots = self.applyMask(spotMask)
        frameNumber, nSpots = np.unique(spots[:,2],return_counts=True)
        mask = np.concatenate([[True],spots[1:,2]!=spots[:-1,2]])
        indices, = np.nonzero(mask)
        intensity = np.add.reduceat(spots[:,3],indices,axis=0) 
        return np.asarray((frameNumber,intensity)).T[nSpots > spotThreshold,:]
    
class BurnSpotGroup:
    
    def __init__(self,
                 spotFilter=None,
                 ranges=None):

        self._spotFilter = spotFilter
        self._intensityArray = self._spotFilter.intVsFrame(**ranges)
        self._spotsArray = self._spotFilter.spotsVsFrame(**ranges)
        self._decayStrategy = ds.BayesianSegmentsDecay(self._intensityArray)
        self._ranges = ranges
        
    def fitDecayModel(self):
        self._decayStrategy.fitDecayModel()
        return
    
    @property
    def ranges(self):
        return self._ranges
    
    @property
    def modelHalfLife(self):
        return self._decayStrategy.modelHalfLife
    
    @property
    def fitIndices(self):
        return self._decayStrategy.fitIndices

class BurnExperiment:
    
    '''
    Collection of BurnSpotGroup objects
    
    Encompasses all spots observed during burn experiment, generates partition
    filters for spots, e.g. resolution ranges (observed or given), psi ranges
    (for anisotropy check), or frame no.
    
    Includes methods for reporting and visualizing results of BurnSpotGroups.
    '''
    
    def __init__(self,
                 pathToSpotXDS,
                 firstFrame,
                 resRangeAll=None,
                 nResShells=5,
                 psiRangeAll=None,
                 nPsiWedges=1,
                 frameRangeAll=None,
                 nFrameBatches=1,
                 **kwargs):
        
        self._spotXDSArray = np.loadtxt(pathToSpotXDS)
        self._params = ep.ExperimentParams(firstFrame=firstFrame)
        self._resArray = SpotArrayPixToRes.pixToRes(self._spotXDSArray,
                                                    self._params)
        self._psiArray = SpotArrayPixToRes.pixToPsi(self._spotXDSArray,
                                                    self._params)
        self._spotFilter = SpotFilter(self._spotXDSArray,
                                      resArray=self._resArray,
                                      psiArray=self._psiArray)
        self._nResShells = nResShells
        self._nPsiWedges = nPsiWedges
        self._nFrameBatches = nFrameBatches
        
        if resRangeAll:
            self._resRangeAll = resRangeAll
            
        else:
            self._resRangeAll = (self._resArray.min(),1000)
            
        if psiRangeAll:
            self._psiRangeAll = psiRangeAll
            
        else:
            self._psiRangeAll = (self._psiArray.min(),
                                 self._psiArray.max())
        
        if frameRangeAll:
            self._frameRangeAll = frameRangeAll
            
        if kwargs:
            self._resBounds = kwargs['resBounds']
            
    def resBounds(self):
        """create cut offs for filtering spots"""
            
        #self._resBounds = 1/np.array(resBounds)[::-1]
        sortRes = self._resArray[self._resArray.argsort()]
        sortRes = sortRes[(sortRes > self._resRangeAll[0])*\
                          (sortRes < self._resRangeAll[1])]
        
        if self._nResShells > 1:
            print(len(sortRes))
            dimSize = np.floor_divide(len(sortRes),self._nResShells)
            print('DIMSIZE',dimSize)
        
            self._resBounds = np.resize(sortRes,
                                        (self._nResShells+1,
                                         dimSize-1))[:,0]
            print("RESBOUNDS ",self._resBounds)
            
        else:
            self._resBounds = np.array([sortRes.min(),sortRes.max()])
            
        return self._resBounds
            
    def psiBounds(self):
        
        psiBounds = [self._psiRangeAll[0]]
        deltaPsi = np.absolute(self._psiRangeAll[1]-
                               self._psiRangeAll[0]) / self._nPsiWedges
        
        for k in range(1,self._nPsiWedges + 1):
            psiBounds.append(k*deltaPsi + self._psiRangeAll[0])
        self._psiBounds = np.array(psiBounds)
        
        return

            
    def rangesDictList(self):
        
        dictList = []
        resRangeBounds = self._resBounds
        psiRangeBounds = self._psiBounds
        frameRangeBounds = np.array([self._frameRangeAll[0],
                                     self._frameRangeAll[1]])
        print('resRangeBounds ',resRangeBounds)
        keys = ['resBin',
                'psiWedge',
                'resRange',
                'psiRange',
                'frameRange']
        

        for i in range(0,len(frameRangeBounds)-1):
            psiWedgeCount = 0
            for j in range(0,len(psiRangeBounds)-1):
                resBinCount = 0
                for k in range(0,len(resRangeBounds)-1):
                    r = (resRangeBounds[k],resRangeBounds[k+1])
                    p = (psiRangeBounds[j],psiRangeBounds[j+1])
                    f = (frameRangeBounds[i],frameRangeBounds[i+1])
                    rangesDict = dict(zip(keys,[resBinCount,
                                                psiWedgeCount,
                                                r,p,f]))
                    resBinCount += 1
                    dictList.append(rangesDict)
                psiWedgeCount += 1
                    
        self._rangesDictList = dictList
            
        return

    def spotGroupList(self):
        
        self._burnSpotGroupList = []
        for ranges in self._rangesDictList:
            burnSpotGroup = BurnSpotGroup(spotFilter=self._spotFilter,
                                          ranges=ranges)
            self._burnSpotGroupList.append(burnSpotGroup)

        return
    
    
    def fitSpotGroups(self):
        
        for burnSpotGroup in self._burnSpotGroupList:
            burnSpotGroup.fitDecayModel()
            print("RANGESTEST",burnSpotGroup.ranges)
            burnSpotGroup._decayStrategy.plotSegments(**burnSpotGroup.ranges)
            
        return
    
    def experimentPlot(self):
        
        summaryArray = np.zeros((len(self._burnSpotGroupList),4))
        for i,burnSpotGroup in enumerate(self._burnSpotGroupList):
            summaryArray[i,0] = i
            summaryArray[i,1] = burnSpotGroup._decayStrategy.modelHalfLife
            summaryArray[i,2] = burnSpotGroup.ranges['resRange'][0]
            summaryArray[i,3] = burnSpotGroup.ranges['resRange'][1] 
        
        return summaryArray
        
        
    
    
        
    

