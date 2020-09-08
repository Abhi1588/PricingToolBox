import numpy as np
import pandas as pd


def forward_PriceBS(spot, strike, rate, maturity, volatility, dividend):
    #Theorem 2.1
    return np.exp(-rate*maturity)*(np.exp((rate-dividend)*maturity)*spot - strike)
