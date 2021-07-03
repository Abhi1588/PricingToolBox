import numpy as np
import pandas as pd
import math
from scipy.stats import norm
import matplotlib.pyplot as plt

def forwardPrice(spot,strike,maturity,rate,dividend,vol = None):
    return math.exp(-rate*maturity)*((math.exp((rate-dividend)*maturity)*spot) - strike)

def europeanCallOptionPrice(spot,strike,maturity,rate,dividend,vol):
    d1 = (math.log(spot/strike) + (rate -dividend + 0.5*vol**2)*(maturity))/(vol*math.sqrt(maturity))
    d2 = d1 - vol*math.sqrt(maturity)
    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)
    return spot*math.exp(-dividend*maturity)*Nd1 - strike*math.exp(-rate*maturity)*Nd2

def europeanPutOptionPrice(spot,strike,maturity,rate,dividend,vol):
    d1 = (math.log(spot/strike) + (rate -dividend + 0.5*vol**2)*(maturity))/(vol*math.sqrt(maturity))
    d2 = d1 - vol*math.sqrt(maturity)
    Nd1 = norm.cdf(-d1)
    Nd2 = norm.cdf(-d2)
    return (spot*math.exp(-dividend*maturity)*Nd1 - strike*math.exp(-rate*maturity)*Nd2)*-1

def digitalCall(spot,strike,maturity,rate,dividend,vol):
    d1 = (math.log(spot/strike) + (rate -dividend + 0.5*vol**2)*(maturity))/(vol*math.sqrt(maturity))
    d2 = d1 - vol*math.sqrt(maturity)
    Nd2 = norm.cdf(d2)
    return (math.exp(-rate*maturity)*Nd2)

def digitalPut(spot,strike,maturity,rate,dividend,vol):
    d1 = (math.log(spot/strike) + (rate -dividend + 0.5*vol**2)*(maturity))/(vol*math.sqrt(maturity))
    d2 = d1 - vol*math.sqrt(maturity)
    Nd2 = norm.cdf(-d2)
    return (math.exp(-rate*maturity)*Nd2)

def zerocouponbond(rate,maturity):
    return math.exp(-rate*maturity)





