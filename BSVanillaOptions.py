import numpy as np
import pandas as pd
from scipy.stats import norm



def forward_valueBS(spot, rate, maturity, strike):


    return spot - np.exp(-rate*maturity)*strike



def option_priceBS(spot, strike, rate, maturity, volatility, flag = 1):

    d_plus = (1/volatility*(np.sqrt(maturity)))*(np.log(spot/strike) + (rate + (volatility**2)/2)*maturity)
    d_minus = d_plus - volatility*np.sqrt(maturity)
    price = flag*(spot*norm.cdf(flag*d_plus) - strike*np.exp(-rate*maturity)*norm.cdf(flag*d_minus))

    return price



def main():
    print(forward_valueBS(100, 0.05, 2, 110))
    print(option_priceBS(100,110,0.05,2,0.01))
    print(option_priceBS(100,110,0.05,2,0.01,-1))
    print("Parity: {}".format(option_priceBS(100,110,0.05,2,0.01) - option_priceBS(100,110,0.05,2,0.01,-1)))

main()
