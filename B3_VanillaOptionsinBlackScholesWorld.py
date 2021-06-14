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



def main():
    spot = 100
    strike = 100
    maturity = 1
    rate = 0.02
    dividend = 0
    vol = .05


    # Put Call Parity
    put = europeanPutOptionPrice(spot,strike,maturity,rate,dividend,vol)
    call = europeanCallOptionPrice(spot,strike,maturity,rate,dividend,vol)
    fwd = forwardPrice(spot,strike,maturity,rate,dividend)
    print("Put Call Parity \nCall :{} - Put :{} = {} \nForward: {}".format(call,put,call-put,fwd))
    print("+"*20)
    #Price of call is monotonically decreasing in strike
    lStrike = []
    lcallPrice = []
    for i in range(strike-90, strike+110, 10):
        lStrike.append(i)
        lcallPrice.append(europeanCallOptionPrice(spot,i,maturity,rate,dividend,vol))

    fig, ax = plt.subplots()
    ax.plot(lStrike, lcallPrice, label = "call price")
    ax.set_xlabel('strikes')  # Add an x-label to the axes.
    ax.set_ylabel('option price')  # Add a y-label to the axes.
    ax.set_title("Call Option Price vs Strike")  # Add a title to the axes.
    ax.legend()
    plt.show()
    print("+"*20)

    #Price of call is between S and S - k e^(-rt)

    f = spot - strike*math.exp(-rate*maturity)

    if f < call and call < spot:
        print("True")

    print("+"*20)

    #Price of call is monotonically increasign in vol
    lvol = []
    lcallPrice = []
    for i in np.arange(vol*.5, vol*1.5, 0.005):
        lvol.append(i)
        lcallPrice.append(europeanCallOptionPrice(spot,strike,maturity,rate,dividend,i))

    fig, ax = plt.subplots()
    ax.plot(lvol, lcallPrice, label = "call price")
    ax.set_xlabel('vol')  # Add an x-label to the axes.
    ax.set_ylabel('option price')  # Add a y-label to the axes.
    ax.set_title("Call Option Price vs vol")  # Add a title to the axes.
    ax.legend()
    plt.show()
    print("+"*20)

    Dcall = digitalCall(spot,strike,maturity,rate,dividend,vol)
    Dput = digitalPut(spot,strike,maturity,rate,dividend,vol)
    zcb = zerocouponbond(rate,maturity)

    call_short = europeanCallOptionPrice(spot,strike+1,maturity,rate,dividend,vol)

    spread = call - call_short

    print(Dcall+Dput, "ZCB : {}".format(zcb))

    print(Dcall,"Spread: {}".format(spread))




