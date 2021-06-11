import numpy as np
import pandas as pd
import math
from scipy.stats import norm

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

def digitalCall():
    pass

def digitalPut():
    pass

def zerocouponbond():
    pass




spot = 100
strike = 100
maturity = 1
rate = 0.02
dividend = 0
vol = .10

put = europeanPutOptionPrice(spot,strike,maturity,rate,dividend,vol)
call = europeanCallOptionPrice(spot,strike,maturity,rate,dividend,vol)
fwd = forwardPrice(spot,strike,maturity,rate,dividend)

print(call - put , fwd)




