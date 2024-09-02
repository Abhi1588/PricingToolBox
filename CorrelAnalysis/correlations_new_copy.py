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

rateSwap_Directory = r'rates'
Cashrate_Directory = r'cashRates'
TreasurySpread_Directory = r'treasurySpread'
xCCYSpread_Directory = r'xccy'


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


df_Swap = read_files(rateSwap_Directory)
df_xccy = read_files(xCCYSpread_Directory)

df_EURIBOR = df_Swap[ df_Swap.Curve != 'EONIA OIS EUR']
df_EONIA = df_Swap[ df_Swap.Curve == 'EONIA OIS EUR']

df_Spreads = pd.merge(df_EURIBOR[['Date','Curve','Maturity','Mid']],
                      df_EONIA[['Date','Curve','Maturity','Mid']],
                      how ="inner", on=["Date", "Maturity"])

df_Spreads['Spread'] = df_Spreads.Mid_x - df_Spreads.Mid_y

matu = ['5Y']
window = 7*52

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




#swap_treasury_matus = [matu for matu in set(df_Swap.Maturity).intersection(set(df_Treasury.Maturity))]
swap_xccy_matus = [matu for matu in set(df_Swap.Maturity).intersection(set(df_xccy.Maturity))]
#cash_treasury_matus = [matu for matu in set(df_Cash.Maturity).intersection(set(df_Treasury.Maturity))]



def get_correls(df1, df2, matu, window = None, returns = 'Simple'):
    
    _df1 = df1.copy()
    _df2 = df2.copy()
    
    _df1 = _df1[_df1['Maturity']==matu]
    _df2 = _df2[_df2['Maturity']==matu]
    
    _df1['Date'] = pd.to_datetime(_df1['Date'])
    _df2['Date'] = pd.to_datetime(_df2['Date'])
    
    #_df1 = _df1.reset_index(drop = True)
    _df1.set_index('Date',inplace=True)
    _df1 = _df1.sort_index(ascending=True)
    #_df2 = _df2.reset_index(drop = True)
    _df2.set_index('Date',inplace=True)
    _df2 = _df2.sort_index(ascending=True)
    
    if returns == 'Simple':
        _df1['returns'] = (_df1.Mid - _df1.Mid.shift(1))
        _df2['returns'] = (_df2.Mid - _df2.Mid.shift(1))
    elif returns == 'Log':
         _df1['returns'] = np.log(_df1['Mid'] / _df1['Mid'].shift(1))
         _df2['returns'] = np.log(_df2['Mid'] / _df2['Mid'].shift(1))
     
    returns_df = pd.merge(_df1.returns, _df2.returns, left_index=True, right_index=True)
    
    if window is not None:
        returns_df['correl'] = returns_df['returns_x'].rolling(window).corr(returns_df['returns_y'])
    else:
        returns_df['correl'] = returns_df['returns_x'].corr(returns_df['returns_y'])
        
    return returns_df

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
        plt.close()
  
    

df_Tresaury_test = df_Treasury[df_Treasury['Maturity']=='5Y']
df_Tresaury_test.set_index('Date',inplace=True)
df_Tresaury_test = df_Tresaury_test.sort_index(ascending=True)
df_Tresaury_test['returns'] = (df_Tresaury_test.Mid - df_Tresaury_test.Mid.shift(1))/df_Tresaury_test.Mid.shift(1)
df_Tresaury_test = df_Tresaury_test[~df_Tresaury_test.isin([np.nan, np.inf, -np.inf]).any(1)]
df_Tresaury_test['indicate'] = df_Tresaury_test.returns != 0
dex = defaultdict(dict)
period = 1
for i in range(0,df_Tresaury_test.shape[0]):
    if df_Tresaury_test.indicate[i]:
#        if period == 0:
#            period += 1
#            continue
        dex[period]['start'] = df_Tresaury_test.index[i+1]
        dex[period-1]['end'] = df_Tresaury_test.index[i]
        period += 1
        
df_Swap_test = df_Swap[df_Swap['Maturity']=='5Y']
df_Swap_test.set_index('Date',inplace=True)
df_Swap_test = df_Swap_test.sort_index(ascending=True)
df_Swap_test['returns_new'] = 0
err = {}
for i in range(1,len(dex)-1):
    print(i)
    try:
        df_Swap_test['returns_new'][df_Swap_test.index == dex[i]['end']] = \
            df_Swap_test.Mid[df_Swap_test.index == dex[i]['end']].values - \
                df_Swap_test.Mid[df_Swap_test.index == dex[i]['start']].values
                
    except Exception as e:
        err[i] = str(e)

new_df = pd.merge(df_Swap_test.returns_new, df_Tresaury_test.returns, left_index=True, right_index=True)

new_df = new_df[(new_df.T != 0).any()]
new_df.returns.corr(new_df.returns_new)

for matu in swap_xccy_matus:
    print(matu)
    correl_df = get_correls(df_Swap, df_xccy, matu, window = 250)
    plot_curves(correl_df,matu,"RateSwap vs xCCY B Swap",True)


for matu in swap_treasury_matus:
    print(matu)
    correl_df = get_correls(df_Swap, df_Treasury, matu, window = 250)
    plot_curves(correl_df,matu,"RateSwap vs Treasury",True)

for matu in cash_treasury_matus:
    print(matu)
    correl_df = get_correls(df_Cash, df_Treasury, matu, window = 250)
    plot_curves(correl_df,matu,"Cash vs Treasury",True)


