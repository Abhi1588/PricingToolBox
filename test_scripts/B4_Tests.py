import B3_VanillaOptionsinBlackScholesWorld as B3BS
import B4_VanillaGreeks as B4Greeks
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

spot = 100
strike = 100
maturity = 0.5
rate = 0.02
dividend = 0
vol = .1

delta = B4Greeks.delta_call_BSM(spot, strike, maturity, rate, vol)
delta_fd = B4Greeks.delta_call_finite_difference(spot, strike, maturity, rate, vol)

print(delta, delta_fd)
print("Diff %: {:.4f} %".format(abs(delta - delta_fd)*100/abs(delta)))

gamma = B4Greeks.gamma_call_BSM(spot, strike, maturity, rate, vol)
gamma_fd = B4Greeks.gamma_call_finite_difference(spot, strike, maturity, rate, vol)

e = 0.0001
delta_up = B4Greeks.delta_call_BSM(spot + e, strike, maturity, rate, vol)

delta_fd = (delta_up-delta)/e

print(gamma, gamma_fd)
print("Diff %: {:.4f} %".format(abs(gamma - gamma_fd)*100/abs(gamma)))

print(gamma, gamma_fd, delta_fd)
