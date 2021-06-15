import numpy
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


def call_payoff(prices, strike):
    return numpy.maximum((prices - strike), 0)


def put_payoff(prices, strike):
    return numpy.maximum((strike - prices), 0)


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


spot = 100
strike = 100
maturity = 1
rate = 0.02
dividend = 0
vol = .10
noOfSim = 10000

callMC = MonteCarloOptionPricer()
callMC.simulateAssetPrices_GBM(spot, rate, maturity, vol, noOfSim, dividend)
callMC.option_pricer_GBM(call_payoff, strike)
print(callMC.optionPrice)

call = B3.europeanCallOptionPrice(spot, strike, maturity, rate, dividend, vol)

print(call)
