import numpy as np
import pandas as pd


def forward_PriceBS(spot, rate, maturity, dividend = None, time = None):

    if not dividend is None and not time is None:
        if not len(dividend) == len(time):
            return print("dividends and payment time not match")
        else:
            D = sum([dividend[x]*np.exp(rate*(maturity-time[x])) for x in range(0,len(dividend))])
    else:
        D = 0
    # Theorem 2.1
    return spot*np.exp(rate*maturity) - D


def main():
    print(forward_PriceBS(100, 0.05, 2,[25],[1]))


main()
