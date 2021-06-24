
import numpy as np
import pandas as pd
import math
from scipy.stats import norm
import matplotlib.pyplot as plt
import B3_VanillaOptionsinBlackScholesWorld as B3


class MonteCarloOptionPricer:
    def __init__(self):
        self.assetPrice = None
        self.discountFactor = None
        self.optionPrice = None
        self.payOffPaths = None
        self._dt = None

    def simulateAssetPrices_GBM(self, spot, rate, maturity, vol, noofSimulations, dividend=None):
        rand = np.random.standard_normal(noofSimulations)
        S_T = np.zeros((noofSimulations, 2))
        S_T[:, 0] = spot
        if dividend is None:
            dividend = 0
        S_T[:, 1] = (S_T[:, 0] * np.exp(
            (rate - dividend) * maturity - 0.5 * vol ** 2 * maturity + vol * np.sqrt(maturity) * rand))
        self.assetPrice = S_T
        self.discountFactor = self.zerocouponbond(rate, maturity)

    def zerocouponbond(self, rate, maturity):
        return math.exp(-rate * maturity)

    def option_pricer_GBM(self, payoffObj, strike, paths="All"):
        if paths == "All":
            payoff = payoffObj(self.assetPrice[:, 1], strike)
        else:
            payoff = payoffObj(self.assetPrice[:paths, 1], strike)
        self.optionPrice = (payoff * self.discountFactor).mean()
        self.payOffPaths = payoff

    def _assetPrice(self, currentprice, rate, vol, dividend):
        rand = np.random.standard_normal(currentprice.shape[0])
        return currentprice + (rate-dividend)*currentprice*self._dt + currentprice*vol*np.sqrt(self._dt)*rand


    def simulateAssetPrice_Euler(self,spot, rate, maturity, vol, noofSimulations, steps, dividend=None):
        self._dt = maturity/steps
        if dividend is None:
            dividend = 0
        assetPaths = np.zeros((noofSimulations, steps))
        assetPaths[:, 0] = spot
        for i in np.arange(1, steps):
            assetPaths[:, i] = self._assetPrice(assetPaths[:, i-1], rate, vol, dividend)
        self.assetPaths = assetPaths
        self.discountFactor = self.zerocouponbond(rate, maturity)

    def option_pricer_euler(self, payoffObj, strike, paths="All"):
        last = self.assetPaths.shape[1] - 1
        if paths == "All":
            payoff = payoffObj(self.assetPaths[:, last], strike)
        else:
            payoff = payoffObj(self.assetPrice[:paths, last], strike)
        self.optionPrice = (payoff * self.discountFactor).mean()
        self.payOffPaths = payoff

def call_payoff(prices, strike):
    return np.maximum((prices - strike), 0)


def put_payoff(prices, strike):
    return np.maximum((strike - prices), 0)


def forward_payoff(prices, strike):
    return prices - strike


def digitalCall_Payoff(prices, strike):
    if prices - strike > 0:
        return 1
    else:
        return 0


def digitalPut_Payoff(prices, strike):
    if strike - prices > 0:
        return 1
    else:
        return 0


def straddle(prices, strike):
    call = call_payoff(prices, strike)
    put = put_payoff(prices, strike)
    straddle = call + put
    return straddle



def main():
    spot = 100
    strike = 100
    maturity = 1
    rate = 0.02
    dividend = 0
    vol = 0.01
    noOfSim = 30000

    strikes = [strike + 5*i  for i in np.arange(0, 10)]
    strikes.extend([strike - 5*i  for i in np.arange(0, 10)])
    strikes.sort()

    vols = [vol + 0.001*i for i in np.arange(0, 10)]
    maturities = [maturity + 0.5*i for i in np.arange(0, 10)]
    rates = [rate + 0.01*i for i in np.arange(0,10)]

    callMC = MonteCarloOptionPricer()
    callMC.simulateAssetPrices_GBM(spot, rate, maturity, vol, noOfSim, dividend)
    prices = []
    for strike in strikes:
        callMC.option_pricer_GBM(call_payoff, strike)
        prices.append(callMC.optionPrice)

    fig, ax = plt.subplots()
    ax.plot(strikes, prices, label="Call Option Price")
    ax.set_xlabel('Strikes')
    ax.set_ylabel('Option Price')
    ax.set_title("Prices Test")
    #ax.legend()
    plt.show()


    callMC = MonteCarloOptionPricer()
    callMC.simulateAssetPrices_GBM(spot, rate, maturity, vol, noOfSim, dividend)
    callMC.option_pricer_GBM(call_payoff, strike)
    print("GBM: {}".format(callMC.optionPrice))
    # print(call)

    call = B3.europeanCallOptionPrice(spot, strike, maturity, rate, dividend, vol)
    # put = B3.europeanPutOptionPrice(spot, strike, maturity, rate, dividend, vol)
    print("BS : {}".format(call))

    # strad = MonteCarloOptionPricer()
    # strad.simulateAssetPrices_GBM(spot, rate, maturity, vol, noOfSim, dividend)
    # strad.option_pricer_GBM(straddle,strike)
    # print(strad.optionPrice)
    # print(call+put)

    callEU = MonteCarloOptionPricer()
    callEU.simulateAssetPrice_Euler(spot, rate, maturity, vol, noOfSim, 250)
    callEU.option_pricer_euler(call_payoff, strike)
    print("Euler : {}".format(callEU.optionPrice))

    # x = [i+1 for i in range(0, test.assetPaths.shape[1])]
    # fig, ax = plt.subplots()
    # ax.plot(x, test.assetPaths.transpose())#, label="Asset Price")
    # ax.set_xlabel('TimeStep')
    # ax.set_ylabel('Asset Price')
    # ax.set_title("Prices")
    # #ax.legend()
    # plt.show()
