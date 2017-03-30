# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:46:02 2017

@author: GY
"""

from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import scipy.stats as stats

# Read and clean data.
MA = pd.read_csv('C:/Users/GY/WeatherPlot/MA_PM_2016.csv').groupby('Date')['Daily Mean PM2.5 Concentration'].mean()
MA = MA.reset_index()
MA.columns = ['Date', 'PM2.5']
#MA = MA[['PM2.5', 'Date']]
MA['Date'] = MA['Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
MA = MA.set_index(pd.DatetimeIndex(MA['Date']))
del MA['Date']

MI = pd.read_csv('C:/Users/GY/WeatherPlot/MI_PM_2016.csv').groupby('Date')['Daily Mean PM2.5 Concentration'].mean()
MI = MI.reset_index()
MI.columns = ['Date', 'PM2.5']
MI['Date'] = MI['Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
MI = MI.set_index(pd.DatetimeIndex(MI['Date']))
del MI['Date']

FL = pd.read_csv('C:/Users/GY/WeatherPlot/FL_PM_2016.csv').groupby('Date')['Daily Mean PM2.5 Concentration'].mean()
FL = FL.reset_index()
FL.columns = ['Date', 'PM2.5']
FL['Date'] = FL['Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
FL = FL.set_index(pd.DatetimeIndex(FL['Date']))
del FL['Date']

CA = pd.read_csv('C:/Users/GY/WeatherPlot/CA_PM_2016.csv').groupby('Date')['Daily Mean PM2.5 Concentration'].mean()
CA = CA.reset_index()
CA.columns = ['Date', 'PM2.5']
CA['Date'] = CA['Date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y'))
CA = CA.set_index(pd.DatetimeIndex(CA['Date']))
del CA['Date']

# Make daily line plot.
fig = plt.figure(figsize = (16, 12));
fig.subplots_adjust(hspace = 0.5)
ax1 = plt.subplot2grid((3, 4), (0, 0), colspan = 3);
#fig.subplots_adjust(left = 0.25, bottom = 0.25)
ax1.plot(MA, color = 'green', label = 'Massachusetts')
ax1.plot(MI, color = 'blue', label = 'Michigan')
ax1.plot(CA, color = 'orange', label = 'California')
ax1.plot(FL, color = 'red', label = 'Florida')
DateFormat = mdates.DateFormatter('%b-%d')
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(DateFormat)
ax1.set_xlabel('Date', size = 13)
ax1.set_ylabel('PM2.5 Level ($ug/m^3 LC$)', size = 13)
ax1.set_title('Daily PM2.5 Pollution in 4 States (MA, MI, CA, FL) as of 2016', size = 15)
ax1.legend(loc = (1,0.2), frameon = False, prop = {'size':20})

# Make violinplot.
ax2 = plt.subplot2grid((3, 4), (1, 0), colspan = 2, rowspan =2)
ax2.violinplot((MI, MA, CA, FL), showmeans = True)
ax2.set_xticks((1, 2, 3, 4))
ax2.set_xticklabels(('Michigan', 'Massachusetts', 'California', 'Florida'), size = 13)
ax2.set_ylabel('PM2.5 Level ($ug/m^3 LC$)', size = 13)
ax2.set_title('Daily PM2.5 Distributions and Means', size = 15)
ax2.text(1.04, float(MI.mean()) - 0.6, '{0:.3f}'.format(float(MI.mean())), color = 'blue')
ax2.text(2.04, float(MA.mean()) - 0.6, '{0:.3f}'.format(float(MA.mean())), color = 'green')
ax2.text(3.04, float(CA.mean()) - 0.6, '{0:.3f}'.format(float(CA.mean())), color = 'orange')
ax2.text(4.04, float(FL.mean()) - 0.6, '{0:.3f}'.format(float(FL.mean())), color = 'red')

# Make overlayed histogram.
ax3 = plt.subplot2grid((3, 4), (1, 2), colspan = 2, rowspan = 2)
lo = round(min(float(MA.min()), float(MI.min()), float(CA.min()), float(FL.min())))
hi = round(max(float(MA.max()), float(MI.max()), float(CA.max()), float(FL.max())))
#ax3.plot.kde(MA['PM2.5'].tolist(), np.arange(lo, hi, 0.1), alpha = 0.3, label = 'Massachusetts', color = 'green')
#ax3.plot.kde(FL['PM2.5'].tolist(), np.arange(lo, hi, 0.1), alpha = 0.3, label = 'Florida', color = 'red')
#ax3.plot.kde(CA['PM2.5'].tolist(), np.arange(lo, hi, 0.1), alpha = 0.3, label = 'California', color = 'orange')
#ax3.plot.kde(MI['PM2.5'].tolist(), np.arange(lo, hi, 0.1), alpha = 0.3, label = 'Michigan', color = 'blue')
dMA = stats.gaussian_kde(MA['PM2.5'].tolist())
n, x, _ = ax3.hist(MA['PM2.5'].tolist(), np.arange(lo, hi, 0.1), histtype = 'step', alpha = 0, normed = True);
ax3.plot(x, dMA(x), label = 'Massachusetts', color = 'green')

dMI = stats.gaussian_kde(MI['PM2.5'].tolist())
n, x, _ = ax3.hist(MI['PM2.5'].tolist(), np.arange(lo, hi, 0.1), histtype = 'step', alpha = 0, normed = True);
ax3.plot(x, dMI(x), label = 'Michigan', color = 'blue')

dCA = stats.gaussian_kde(CA['PM2.5'].tolist())
n, x, _ = ax3.hist(MA['PM2.5'].tolist(), np.arange(lo, hi, 0.1), histtype = 'step', alpha = 0, normed = True);
ax3.plot(x, dCA(x), label = 'California', color = 'orange')

dFL = stats.gaussian_kde(FL['PM2.5'].tolist())
n, x, _ = ax3.hist(FL['PM2.5'].tolist(), np.arange(lo, hi, 0.1), histtype = 'step', alpha = 0, normed = True);
ax3.plot(x, dFL(x), label = 'Florida', color = 'red')

ax3.set_title('Probability distribution of PM2.5', size = 15)
ax3.set_xlabel('PM2.5 Level ($ug/m^3 LC$)', size = 13)
ax3.set_ylabel('Distribution Probability', size = 13)
ax3.yaxis.tick_right()
ax3.yaxis.set_label_position('right')
plt.show()