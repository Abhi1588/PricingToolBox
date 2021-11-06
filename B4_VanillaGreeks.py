import B3_VanillaOptions_MC_BlackScholes as B3MC
import B3_VanillaOptionsinBlackScholesWorld as B3BS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def delta_call_BSM(spot,strike,maturity,rate,vol,dividend=None):
    if dividend is None:
        dividend = 0
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5*vol**2)*(maturity))/(vol*np.sqrt(maturity))
    Nd1 = norm.cdf(d1)
    return np.exp(-dividend*maturity)*Nd1

def _dN(x):
    return np.exp((-x**2)/2)/(np.sqrt(2*np.pi))

def gamma_call_BSM(spot,strike,maturity,rate,vol,dividend=None):
    if dividend is None:
        dividend = 0
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5*vol**2)*(maturity))/(vol*np.sqrt(maturity))
    dN = _dN(d1)
    return (dN/(spot*vol*np.sqrt(maturity)))*np.exp(-dividend*maturity)

def vega_call_BSM(spot,strike,maturity,rate,vol,dividend=None):
    if dividend is None:
        dividend = 0
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5*vol**2)*(maturity))/(vol*np.sqrt(maturity))
    dN = _dN(d1)
    return np.exp(-dividend*maturity)*spot*np.sqrt(maturity)*dN

def theta_call_BSM(spot,strike,maturity,rate,vol,dividend=None):
    if dividend is None:
        dividend = 0
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5*vol**2)*(maturity))/(vol*np.sqrt(maturity))
    d2 = d1 - vol*np.sqrt(maturity)
    dN = _dN(d1)
    return -np.exp(-dividend*maturity)*spot*dN*vol/(2*np.sqrt(maturity)) + \
           dividend*np.exp(-dividend*maturity)*spot*norm.cdf(d1) - \
           rate*strike*np.exp(-rate*maturity)*norm.cdf(d2)

def rho_call_BSM(spot,strike,maturity,rate,vol,dividend=None):
    if dividend is None:
        dividend = 0
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5*vol**2)*(maturity))/(vol*np.sqrt(maturity))
    d2 = d1 - vol*np.sqrt(maturity)
    return strike*maturity*np.exp(-rate*maturity)*norm.cdf(d2)

def delta_call_finite_difference(spot,strike,maturity,rate,vol,dividend=None):
    if dividend is None:
        dividend = 0
    e = 0.0001  ##this works better than using 0.0001*spot
    call_up = B3BS.europeanCallOptionPrice(spot + e, strike, maturity, rate, dividend, vol)
    call = B3BS.europeanCallOptionPrice(spot, strike, maturity, rate, dividend, vol)
    return (call_up-call)/e

def gamma_call_finite_difference(spot,strike,maturity,rate,vol,dividend=None):
    if dividend is None:
        dividend = 0
    e = 0.0001
    call_up = B3BS.europeanCallOptionPrice(spot + e, strike, maturity, rate, dividend, vol)
    call_dn = B3BS.europeanCallOptionPrice(spot - e, strike, maturity, rate, dividend, vol)
    call = B3BS.europeanCallOptionPrice(spot, strike, maturity, rate, dividend, vol)
    return (call_up - 2*call + call_dn)/e**2


def vega_call_finite_difference(spot, strike, maturity, rate, vol, dividend=None):
    if dividend is None:
        dividend = 0
    e = 0.0001  ##this works better than using 0.0001*spot
    call_up = B3BS.europeanCallOptionPrice(spot , strike, maturity, rate, dividend, vol + e)
    call = B3BS.europeanCallOptionPrice(spot, strike, maturity, rate, dividend, vol)
    return (call_up-call)/e


def rho_call_finite_difference(spot, strike, maturity, rate, vol, dividend=None):
    if dividend is None:
        dividend = 0
    e = 0.0001  ##this works better than using 0.0001*spot
    call_up = B3BS.europeanCallOptionPrice(spot , strike, maturity, rate + e, dividend, vol)
    call = B3BS.europeanCallOptionPrice(spot, strike, maturity, rate, dividend, vol)
    return (call_up-call)/e

def theta_call_finite_difference(spot, strike, maturity, rate, vol, dividend=None):
    if dividend is None:
        dividend = 0
    e = 0.0001  ##this works better than using 0.0001*spot
    call_up = B3BS.europeanCallOptionPrice(spot , strike, maturity + e, rate, dividend, vol)
    call = B3BS.europeanCallOptionPrice(spot, strike, maturity, rate, dividend, vol)
    return (call_up-call)/e

#region MonteCarlo Greeks
def delta_call_MonteCarlo(spot, strike, rate, maturity, vol, noOfSim = 1000, dividend = None):
    total_Delta = 0
    total_Delta2 = 0
    callMC = B3MC.MonteCarloOptionPricer()
    callMC.simulateAssetPrices_GBM(spot, rate, maturity, vol, noOfSim, dividend)
    for _ in range(0,callMC.assetPrice.shape[0]):
        if callMC.assetPrice[ _, 1] > strike:
            I = 1
        else:
            I = 0
        delta = callMC.zerocouponbond(rate, maturity)*callMC.assetPrice[ _, 1]/spot*I
        total_Delta += delta
        total_Delta2 += delta**2
    return total_Delta/noOfSim, total_Delta2/noOfSim



#endregion
