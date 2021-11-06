#import B3_VanillaOptionsinBlackScholesWorld as B3BS
import B4_VanillaGreeks as B4Greeks
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Utils
spot = 100
strike = 100
maturity = 0.5
rate = 0.02
dividend = 0
vol = .1
noOfSim = 10000
# region Delta of a call a function of spot
delta = B4Greeks.delta_call_BSM(spot, strike, maturity, rate, vol)
delta_fd = B4Greeks.delta_call_finite_difference(spot, strike, maturity, rate, vol)
print("Formula Delta: {:.5f} \nFinite Diff Delta: {:.5f}".format(delta, delta_fd))
print("Diff %: {:.4f} %".format(abs(delta - delta_fd)*100/abs(delta)))

spots = [spot + i for i in range(-25, 26, 1)]
deltas = [B4Greeks.delta_call_BSM(spot, strike, maturity, rate, vol) for spot in spots]

Utils.plot_curve(spots,deltas,"Call Delta","Stock Price","Delta","Delta of Call")

print("="*50)
# endregion


delta = B4Greeks.delta_call_BSM(spot, strike, maturity, rate, vol)
delta_mc, delta2_mc = B4Greeks.delta_call_MonteCarlo(spot,strike,rate,maturity,vol,noOfSim,dividend)
print("BS Delta: {:.4f} \t MonteCarlo Delta: {:.4f}".format(delta,delta_mc))
'''
Calculating Bias and MSE 
https://quant.stackexchange.com/questions/33695/pathwise-derivative-to-estimate-delta
'''

Bias = delta - delta_mc
var = delta2_mc - delta_mc
MSE = Bias**2 + var

print("MSE: \t{:.4f}".format(MSE))





gamma = B4Greeks.gamma_call_BSM(spot, strike, maturity, rate, vol)
gamma_fd = B4Greeks.gamma_call_finite_difference(spot, strike, maturity, rate, vol)

e = 0.0001
delta_up = B4Greeks.delta_call_BSM(spot + e, strike, maturity, rate, vol)

delta_fd = (delta_up-delta)/e

print(gamma, gamma_fd)
print("Diff %: {:.4f} %".format(abs(gamma - gamma_fd)*100/abs(gamma)))

print(gamma, gamma_fd, delta_fd)
