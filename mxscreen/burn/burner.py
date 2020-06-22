# -*- coding: utf-8 -*-



import numpy as np


class SpotArrayPixToRes:
    
    '''
    tools for converting x,y pixel coordinates to polar coordinates for
    resolution and/or psi filtering.
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
        psi = np.arctan(rcArray[:,1]/rcArray[:,0])
        return psi

class SpotFilter:
    
    '''
    requires SPOT.XDS numpy array and either resolution or psi arrays for
    creating mask, the resolution array is computed from x,y detector
    coordinates, frameVsSpots frameVsInts will output Nx2 array on a per frame
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
    
    def spotMask(self, resRange=None, psiRange=None):
        
        mask = np.ones(len(self._spotXDSArray), dtype=bool)
        
        if resRange:
            r = self._resArray
            mask *= (r > resRange[0])*(r < resRange[1])
            
        if psiRange:
            psi = self._psiArray
            mask *= (psi > psiRange[0])*(psi < psiRange[1])

        return mask
    
    def applyMask(self, mask):
        
        spots = self._spotXDSArray[mask,:]
        filteredSpotXDSArray = spots[np.argsort(spots[:,2]),:]
        return filteredSpotXDSArray

    
    def frameVsSpots(self, resRange=None, psiRange=None, spotThreshold=5):
        mask = self.spotMask(resRange, psiRange)
        spots = self.applyMask(mask)

        frameNumber, nSpots = np.unique(spots[:,2],return_counts=True)
        return np.asarray((frameNumber,nSpots)).T[nSpots > spotThreshold,:]
    
    def frameVsInt(self, resRange=None, psiRange=None, spotThreshold=5):
        
        #need to sort by frame no. column, then sum rows with same frame no.
        spotMask = self.spotMask(resRange, psiRange)
        spots = self.applyMask(spotMask)
        frameNumber, nSpots = np.unique(spots[:,2],return_counts=True)
        mask = np.concatenate([[True],spots[1:,2]!=spots[:-1,2]])
        indices, = np.nonzero(mask)
        intensity = np.add.reduceat(spots[:,3],indices,axis=0)
        
        return np.asarray((frameNumber,intensity)).T[nSpots > spotThreshold,:]
        
    

