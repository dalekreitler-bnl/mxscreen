#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 13:09:52 2020

@author: dale
"""

from GPyOpt.methods import BayesianOptimization
import pwlf
import numpy as np
import matplotlib.pyplot as plt

class DecayStrategy:
    
    def fitDecayModel(self):
        pass
    
    def fitIndices(self):
        pass
    
    def modelHalfLife(self):
        pass
    
class LogLinDecayStrategy(DecayStrategy):
    
    def fitDecayModel(self):
        pass
    
    def fitIndices(self):
        pass
    
    def optimalSlope(self):
        pass
    
    def modelHalfLife(self):
        pass
    
class BayesianSegmentsDecay(LogLinDecayStrategy):
    
    """
    Use Bayesian optimization to determine optimal number of line segments
    needed for piecewise linear fit of some signal as a function of frame no.
    The optimal line segment is then chosen with following procedure:
        1. remove line segments with fewer than prespecified no. of points
        2. Return line segment with most negative slope
        3. Half life is calculated based on this value using the formula:
            (Assume signal, I; slope, m)
            I = I0*exp(-m*t)
            At I0 = 0.5*I ==> log(0.5)/alpha = t_0.5
    """

    def __init__(self, signalArray):

        self._frames = signalArray[:,0]
        self._logSignal = np.log(signalArray[:,1])
        self._pwlf = pwlf.PiecewiseLinFit(self._frames, self._logSignal)
        
    def fitDecayModel(self):

        def objFun(x):
            f = np.zeros(x.shape[0])
            for i, j in enumerate(x):
                self._pwlf.fitfast(x)
                f = self._pwlf.ssr
                print('f is ',f, ' when j[i] is ', j[i])
                
            return f

        bounds = [{'name': 'var_1', 'type': 'discrete',
                   'domain': np.arange(2, 4)}]
        
        np.random.seed(212121)

        myBopt = BayesianOptimization(objFun, domain=bounds, model_type='GP')
        myBopt.run_optimization(max_iter=10, verbosity=True)

        #myBopt.x_opt and myBopt.fx_opt will return optimum values of
        #parameters and objective function

        self._fitBreaks = self._pwlf.fit(myBopt.x_opt)
        self._optimalSlope, self._optimalIndices = self.optimalSlope()
            
        
        return
    
    def plotSegments(self, **kwargs):
        xHat = np.linspace(min(self._frames), max(self._frames), num=5000)
        yHat = self._pwlf.predict(xHat)
        plt.figure()
        plt.plot(self._frames, self._logSignal, 'o',
                 self._frames[self._optimalIndices],
                 self._logSignal[self._optimalIndices],'o',)
        plt.plot(xHat, yHat, '-',c='r')
        if kwargs:
            plt.figtext(0,
                        1,
                        "Resolution Limits (A) \n {}-{}"\
                            .format(format(kwargs['resRange'][0],'0.2f'),
                                    format(kwargs['resRange'][1],'0.2f')))
        plt.xlabel('frame no.')
        plt.ylabel('log(SUM(intensity))')
        plt.show()
        return
    
    def optimalSlope(self):
        #returns most negative slope from segments with more than threshold
        #number of points

        slopes=self._pwlf.calc_slopes()
        fb = self._fitBreaks
        x = self._frames
        
        slopesIndex = slopes.argsort()
        bestSlope = slopes[slopesIndex][0]
        
        for j in slopesIndex:
            mask = (x>=fb[j])*(x<fb[j+1])
            segX = x[mask]
            segXIndices = mask.nonzero()
            if len(segX) > 30:
                bestSlope = slopes[j]
                print('Optimal slope is ', slopes[j])
                break
            
        return bestSlope, segXIndices

    @property
    def fitIndices(self):
        return self._optimalIndices
    
    @property
    def modelHalfLife(self):
        return np.log(0.5)/self._optimalSlope
    

