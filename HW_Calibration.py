import numpy as np
import pandas as pd
import math
import seaborn as sns
import datetime as dt
from scipy.optimize import least_squares

class MarketCurves:
    def __init__(self):
        self.term_to_maturity = None
        self.discount_factors = None
        self.dates = None
        self.ois_rate = None

    ## The curve on which the HW rates are based
    def createLibor(self,term_to_maturity,discount_factors):
        self.term_to_maturity = term_to_maturity
        self.discount_factors = discount_factors

    ## The curve used to approximate Market Bond Prices (For dummy data)
    def createOis(self,dates,ois_rate):
        self.dates = dates
        self.ois_rate = ois_rate

    def interpolate(self,t,timeIndex,curve):
        tenor_index = 0
        prev_rate = curve[tenor_index]
        prev_tenor = timeIndex[tenor_index]

        for tenor in curve:
            next_tenor = tenor
            if next_tenor >= t:
                next_rate = curve[tenor_index]
                break
            else:
                prev_tenor = next_tenor
                prev_rate = curve[tenor_index]
                tenor_index = tenor_index + 1

        if next_tenor == prev_tenor and t <= timeIndex[0]:
            """ Check next line of code"""
            inter_rate = next_tenor
        elif next_tenor != prev_tenor and t > timeIndex[-1]:
            inter_rate = prev_rate + ((next_rate - prev_rate) / (next_tenor - prev_tenor)) * (t - prev_tenor)
        else:
            inter_rate = curve[-1]

        return  inter_rate

class ConfigParams:

    def __init__(self, spot_rate, dayCount = 360, NoofSims = 100, generatePlot = False ):

        self.spot_rate = spot_rate
        self.NoofSims = NoofSims
        self.dayCount = dayCount
        self.generatePlot = generatePlot

class TradeObject(ConfigParams):

    def __init__(self):
        super().__init__(self)
        self.t = None
        self.T = None
        self.Freq = None

    def createIRBond(self, startDate, endDate, exposureDate, couponFreq = "Semi"):
        self.startDate = dt.datetime.strptime(startDate, "%d/%m/%Y")
        self.endDate = dt.datetime.strptime(endDate, "%d/%m/%Y")
        self.exposureDate = dt.datetime.strptime(exposureDate, "%d/%m/%Y")

        self.t = ((self.exposureDate - self.startDate).days)/self.dayCount
        self.T = ((self.endDate - self.exposureDate).days)/self.dayCount

        if couponFreq == "Semi":
            self.Freq = 2
        elif couponFreq == "Quaterly":
            self.Freq = 4
        else:
            self.Freq = 1

class Pricer:

    def __init__(self, alpha, sigma, configObject, marketObject):
        self.config = configObject
        self.market = marketObject
        self.avg_rates = None
        self.hw_rates = None
        self.hw_a = alpha
        self.hw_sigma = sigma

    def hw_process(self):

        alpha = self.hw_a
        sigma = self.hw_sigma

        forward_rate = [self.config.spot_rate]
        del_forward_rate = []
        theta = []

        ## Get the forward rate on an yearly basis from LIBOR
        discount_yearly = [1]
        year_count = [0]
        forward_rate_yearly = [self.config.spot_rate]
        for i in range(1, len(self.market.term_to_maturity)):
            k = self.market.term_to_maturity[i]/self.config.dayCount
            #print(k)
            year_count.append(k)
            discount_yearly.append(np.interp(k, [self.market.term_to_maturity[i-1]/self.config.dayCount,
                                                 self.market.term_to_maturity[i]/self.config.dayCount],
                                                [self.market.discount_factors[i-1],
                                                 self.market.discount_factors[i]]))

        ## Getting HW rates
        for i in range(1, len(discount_yearly)):
            forward_rate.append((-(math.log(discount_yearly[i]) - math.log(discount_yearly[i - 1])) / (year_count[i] - year_count[i - 1])))
        for i in range(0, len(discount_yearly)-2):
            del_forward_rate.append((1 / 2) * ((year_count[i+1] + 1) * (np.interp(year_count[i+1] + 1, year_count, forward_rate))
                                               - (year_count[i+1] - 1) * (np.interp(year_count[i+1] - 1, year_count, forward_rate))))
            del_forward_rate.append(forward_rate[len(discount_yearly)-1])

        for i in range(0, len(discount_yearly)-1):
            theta.append(del_forward_rate[i]+(alpha*forward_rate[i+1])+(sigma*sigma)*(1-math.exp(-2*alpha*year_count[i+1]))/(2*alpha))

        hw_rates = np.zeros((self.config.NoofSims, len(year_count)))
        for i in range(1, len(discount_yearly)+1):
            a = np.random.randn(self.config.NoofSims)
            b = a.reshape(self.config.NoofSims, 1)

            if i == 1:
                hw_rates[:, 0:1] = hw_rates[:, 0:1] + self.config.spot_rate
            else:
                hw_rates[:, i-1:i] = (hw_rates[:, (i-2):(i-1)] +(theta[i-2] - alpha*hw_rates[:, (i-2):(i-1)])*((year_count[i-1] - year_count[i-2])/360)
                                      + b*math.sqrt((year_count[i-1] - year_count[i-2])/360)*sigma)
        final_df = pd.DataFrame(hw_rates)
        self.hw_rates =  hw_rates
        avg_hw_rates = final_df.mean(axis = 0)

        ## PLOT
        if self.config.generatePlot:
            ## All Simulations
            for i in range(self.config.NoofSims):
                sns.lineplot(year_count, final_df.iloc[i])
            ## The averages at each time step
            for i in range(len(year_count)):
                sns.lineplot(year_count, avg_hw_rates, linewidth=4)
            ## The Forward Rates
            for i in range(1, len(year_count)):
                forward_rate_yearly.append(-(math.log(discount_yearly[i]) - math.log(discount_yearly[i - 1])) / (year_count[i] - year_count[i - 1]))
            for i in range(len(market.term_to_maturity)):
                sns.lineplot(year_count, forward_rate_yearly).set(ylim = (0.02, 0.04))

        self.avg_rates =  np.array(avg_hw_rates)






if __name__ =="__main__":
    """Create market curve objects"""
    df = pd.read_excel('/Users/abhishek/IdeaProjects/ModelCalibration/3MLOIS123118USD.xlsx')
    marketObject = MarketCurves()
    marketObject.createLibor(df["244 USD"].tolist(), df["LIBOR RR"].tolist())
    marketObject.createOis(df["Dates"].tolist(), df["OIS RR"].tolist())
    """Define Run Configuration"""
    configObject = ConfigParams(0.028)
    """Create Trades"""
    startDate = '01/01/2015'
    endDate = '31/12/2020'
    exposureDate = '01/05/2018'
    TO = TradeObject()
    bond1 = TO.createIRBond(startDate, endDate, exposureDate)
    """Run Pricer"""

    alpha = 0.001
    sigma = 0.002
    priceObject = Pricer(alpha, sigma, configObject,marketObject)
    print("No Process: {}".format(priceObject.avg_rates))
    hwObject = priceObject.hw_process()

    print("HW Object: {}".format(hwObject))
    print("After Process: {}".format(priceObject.avg_rates))

