import math 
import random 
import numpy as np

from scipy import stats

class options_calculation():
    
    def __init__(self, expiry, strike, spot, vol, r):
        
        self.expiry = expiry
        self.strike = strike
        self.spot = spot
        self.vol = vol
        self.r = r
    
    def MCcalculation(self, paths):
        
        self.variance = self.vol**2 * self.expiry
        self.root_Variance = math.sqrt(self.variance)
        
        #this is for the (-1/2* sigma^2 which comes from Ito's lemma)
        self.itoCorr = -0.5 * self.variance
        
        #corresponds to the S0e^(rT - 1/2 sigma^2T)
        self.movedSpot = self.spot * math.exp(self.r * self.expiry + self.itoCorr)
        
        self.runningSum = 0
        
        for i in range(0, paths):
            
            #creates a gaussian distribution for the Brownian motions
            thisGauss = np.random.normal()
            
            #not sure what this is
            thisSpot = self.movedSpot * math.exp(self.root_Variance * thisGauss)
            
            thisPayoff =  thisSpot - self.strike
            
            thisPayoff = thisPayoff if thisPayoff > 0 else 0
            self.runningSum += thisPayoff
            
        self.mean = self.runningSum / paths
        self.mean *= math.exp(-self.r * self.expiry)
        
        return round(self.mean,2)
    
    def bsm_call_value(self):
        
        S0 = float(self.spot)
        
        d1 = (math.log(S0 / self.strike) + (self.r + 0.5 * self.vol ** 2) * self.expiry) / (self.vol / math.sqrt(self.expiry))
        d2 = (math.log(S0 / self.strike) + (self.r - 0.5 * self.vol ** 2) * self.expiry) / (self.vol / math.sqrt(self.expiry))
        
        value = (S0 * stats.norm.cdf(d1, 0.0, 1.0) - self.strike * math.exp(-self.r * self.expiry) * stats.norm.cdf(d2, 0.0, 1.0))
        
        return value
        
        
