import B3_VanillaOptions_MC_BlackScholes as B3MC
import B3_VanillaOptionsinBlackScholesWorld as B3BS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def delta_call(spot,strike,maturity,rate,vol,dividend=None):
    if dividend is None:
        dividend = 0
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5*vol**2)*(maturity))/(vol*np.sqrt(maturity))
    Nd1 = norm.cdf(d1)
    return -np.exp(-dividend*maturity)*Nd1

def _dN(x):
    return np.exp((-x**2)/2)/(np.sqrt(2*np.pi))

def gamma_call(spot,strike,maturity,rate,vol,dividend=None):
    if dividend is None:
        dividend = 0
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5*vol**2)*(maturity))/(vol*np.sqrt(maturity))
    dN = _dN(d1)
    return dN/(spot*vol*np.sqrt(maturity))





