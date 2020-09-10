import numpy as np
import pandas as pd


def forward_PriceBS(spot, strike, rate, maturity, dividend, frequency = "annual"):

    if frequency == "annual":
        [x + 1 for x in range(0, 2)]
        D = spot*

    elif frequency == "semi":



    # Theorem 2.1
    return np.exp(-rate*maturity)*(np.exp((rate-dividend)*maturity)*spot - strike)


def main():
    print(forward_PriceBS(100,120,0.05,2,0.01,0))


main()
