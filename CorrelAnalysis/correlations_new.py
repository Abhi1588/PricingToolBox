# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from functools import reduce

rateSwap_Directory = r'rates'
Cashrate_Directory = r'cashRates'
TreasurySpread_Directory = r'treasurySpread'
xCCYSpread_Directory = r'xccy'
EURUSD_FX_Directory = r'FX/EURUSD'

def plot_curves(df,matu,title = "Title", save=False):

    indx = [dex.date() for dex in df.index]
    val = df['correl'].values

    fig = plt.figure()
    fig, ax = plt.subplots()

    ax.plot(indx, val, label = 'Correl', color = 'blue')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Correlation')

    ax.set_title('{}_Maturity_{}'.format(title,matu))
    fig.legend()
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    if save:
        fig.savefig(r'graph\{}_Correls_for_Matu_{}.jpg'.format(title,matu))
    plt.close(fig)    


def read_files(folder):
    path = os.getcwd()
    folder = os.path.join(path,folder)
    files = os.listdir(folder)
    files_xlsx = [f for f in files if f[-4:] == 'xlsx']
    df = pd.DataFrame()
    for f in files_xlsx:
        print(f)
        data = pd.read_excel(os.path.join(folder,f),engine = 'openpyxl')
        data['file'] = f
        df = df.append(data)
    subset = df.columns.to_list()
    subset.remove('file')
    df = df.drop_duplicates(subset = subset)
    df = df.reset_index(drop = True)
    return df

##Read Data and create dataframes

df_Swap = read_files(rateSwap_Directory)
df_xccy = read_files(xCCYSpread_Directory)
df_FX = read_files(EURUSD_FX_Directory)


##Organise swap data by curve

df_EURIBOR = df_Swap[df_Swap.Curve == 'EURIBOR EUR']
df_EONIA = df_Swap[df_Swap.Curve == 'EONIA OIS EUR']
df_LIBUSD = df_Swap[df_Swap.Curve == 'LIBOR USD']
df_OISUSD = df_Swap[df_Swap.Curve == 'OIS USD']
df_SOFRUSD = df_Swap[df_Swap.Curve == 'SOFR USD']

##Compute Spreads Ref-Ovn

##EURIBOR - EONIA
df_Spreads_EIBEON = pd.merge(df_EURIBOR[['Date','Curve','Maturity','Mid']],
                             df_EONIA[['Date','Curve','Maturity','Mid']],
                             how ="inner", on=["Date", "Maturity"])

df_Spreads_EIBEON['Spread'] = df_Spreads_EIBEON.Mid_x - df_Spreads_EIBEON.Mid_y

##LIBUSD - USDOIS

df_Spreads_LIBOIS = pd.merge(df_LIBUSD[['Date','Curve','Maturity','Mid']],
                             df_OISUSD[['Date','Curve','Maturity','Mid']],
                             how ="inner", on=["Date", "Maturity"])

df_Spreads_LIBOIS['Spread'] = df_Spreads_LIBOIS.Mid_x - df_Spreads_LIBOIS.Mid_y

##LIBUSD - USDSOFR
df_Spreads_LIBSOF = pd.merge(df_LIBUSD[['Date','Curve','Maturity','Mid']],
                             df_SOFRUSD[['Date','Curve','Maturity','Mid']],
                             how ="inner", on=["Date", "Maturity"])

df_Spreads_LIBSOF['Spread'] = df_Spreads_LIBSOF.Mid_x - df_Spreads_LIBSOF.Mid_y


def computeCorrel(borDf,SpreadDf, matu = "All",plot_curve = True):
    window = 7*52
    if matu == 'All':
        matu = set(SpreadDf.Maturity)
        
    df_Spreads = SpreadDf[SpreadDf.Date.notna()].copy()
    df_BOR = borDf[borDf.Date.notna()].copy()
    mean_correl = {}
    
    for mat in matu:
        _df_spreads = df_Spreads[df_Spreads.Maturity == mat]
        _df_bor = df_BOR[df_BOR.Maturity == mat]
        
        _df_spreads.set_index('Date',inplace=True)
        _df_spreads = _df_spreads.sort_index(ascending=True)
        #_df2 = _df2.reset_index(drop = True)
        _df_bor.set_index('Date',inplace=True)
        _df_bor = _df_bor.sort_index(ascending=True)
        _df_spreads['returns'] = (_df_spreads.Spread - _df_spreads.Spread.shift(1))
        _df_bor['returns'] = (_df_bor.Mid - _df_bor.Mid.shift(1))
        returns_df = pd.merge(_df_spreads.returns, _df_bor.returns, left_index=True, right_index=True)
        returns_df['correl'] = returns_df['returns_x'].rolling(window).corr(returns_df['returns_y'])
        mean_correl.update({mat:returns_df.correl.mean()})
        if plot_curve:
            curve = [str(_) for _ in set(borDf.Curve)][0]
            spread = [str(_) for _ in set(SpreadDf.Curve_x)][0] +' ' +[str(_) for _ in set(SpreadDf.Curve_y)][0]
            plot_curves(returns_df,mat,"{} vs {} Spread".format(curve,spread),True)
    
    return pd.DataFrame(mean_correl.items(), columns=["Tenor","Correl"])


## Mono Currency Correlations 
#Euribor swap against ois-Bor spread
EIBvsEIBEON = computeCorrel(df_EURIBOR,df_Spreads_EIBEON)
#LIBUSD swap against ois-Bor spread
LIBUSDvsLIBOIS = computeCorrel(df_LIBUSD,df_Spreads_LIBOIS)
#LIBUSD swap against SOF-bor spread
LIBUSDvsLIBOIS = computeCorrel(df_LIBUSD,df_Spreads_LIBSOF)

#TODO: FX vs Spreads


##Multi Currency Correlations

df_EUR_Spread = df_Spreads_EIBEON[['Date','Maturity','Spread']].rename({'Spread': 'EUR_Spread'}, axis=1)
df_EUR_Spread['Curve_y'] = 'Currency'
df_USD_Spread = df_Spreads_LIBOIS[['Date','Maturity','Spread']].rename({'Spread': 'USD_Spread'}, axis=1)
df_USD_Spread['Curve_x'] = 'Multi'

dfs = [df_EUR_Spread, df_USD_Spread, df_xccy[['Date','Maturity','Mid']]]

df_Multi_Spread = reduce(lambda left,right: pd.merge(left,right,on=["Date", "Maturity"],how='inner'), dfs)
df_Multi_Spread['Spread'] = df_Multi_Spread.USD_Spread - df_Multi_Spread.EUR_Spread - df_Multi_Spread.Mid

EIBEURvsMulti = computeCorrel(df_EURIBOR,df_Multi_Spread)
LIBUSDvsMulti = computeCorrel(df_LIBUSD,df_Multi_Spread)


matu = ['5Y']


for mat in matu:
    _df_spreads = df_Spreads[df_Spreads.Maturity == mat]
    _df_euribor = df_EURIBOR[df_EURIBOR.Maturity == mat]
    
    _df_spreads.set_index('Date',inplace=True)
    _df_spreads = _df_spreads.sort_index(ascending=True)
    #_df2 = _df2.reset_index(drop = True)
    _df_euribor.set_index('Date',inplace=True)
    _df_euribor = _df_euribor.sort_index(ascending=True)
    _df_spreads['returns'] = (_df_spreads.Spread - _df_spreads.Spread.shift(1))
    _df_euribor['returns'] = (_df_euribor.Mid - _df_euribor.Mid.shift(1))
    returns_df = pd.merge(_df_spreads.returns, _df_euribor.returns, left_index=True, right_index=True)
    returns_df['correl'] = returns_df['returns_x'].rolling(window).corr(returns_df['returns_y'])
    
    plot_curves(returns_df,mat,"EURIBOR vs EIB/EON Spread",True)


df_new  = pd.merge(_df_spreads, returns_df, left_index=True, right_index=True)

indx = [dex.date() for dex in df_new.index]
val = df_new['correl'].values
spreads = df_new.Spread * 10000

fig = plt.figure()
fig, ax = plt.subplots()
ax2 = ax.twinx()
ax.plot(indx, val, label = 'Correl', color = 'blue')
ax2.plot(indx,spreads,label = 'Spreads',color = 'grey')
ax2.set_ylabel('Spreads')
ax.set_xlabel('Date')
ax.set_ylabel('Correlation')

ax.set_title('{}_Maturity_{}'.format("EURIBOR vs EIB/EON Spread","5Y"))
fig.legend()
plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
fig.savefig(r'graph\{}_Correls_for_Matu_{}.jpg'.format("EURIBOR vs EIB-EON Spread and Spread","5Y"))
plt.close()



'''
returns_df.correl.rolling(250).mean().plot(title = "Moving Average 250 days", y = "Correlation", x = "Date")
'''

