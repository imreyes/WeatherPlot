# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 14:17:49 2017

@author: GY
"""

from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Read data as directed.
dat = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/6bfe451be8ad7abced396241683a69ba88103e019d15e945a56d0d05.csv')
# Clean data and create new columns as needed.
dat['Years'] = dat['Date'].apply(lambda x: x[:4])
dat['DateOfYear'] = dat['Date'].apply(lambda x: x[5:])
dat = dat[dat['DateOfYear'] != '02-29']
dat['DateOfYear'] = dat['DateOfYear'].apply(lambda x: datetime.strptime(x, '%m-%d'))
dat['Data_Value'] = dat['Data_Value'].apply(lambda x: x/10)
# Separate 'old' and 'new' datasets.
dat_new = dat[dat['Years'] == '2015']
dat = dat[dat['Years'] != '2015']
# Extract high and low records in series.
maxT = dat[dat['Element'] == 'TMAX'].groupby('DateOfYear')['Data_Value'].max()
maxT.sort_index(inplace = True)
minT = dat[dat['Element'] == 'TMIN'].groupby('DateOfYear')['Data_Value'].min()
minT.sort_index(inplace = True)
# Make line plot with shade.
fig, ax = plt.subplots()
ax.plot(minT, color = 'green', label = 'Low Record 2005-2014')
ax.plot(maxT, color = 'orange', label = 'High Record 2005-2014')
DateFormat = mdates.DateFormatter('%b-%d')
ax.xaxis.set_major_formatter(DateFormat)
plt.xlabel('Date of Year')
plt.ylabel('Temperature ($^\circ$C)')
plt.title('Breaking Low/High Temperatures in 2015 Comparing to Records as of 2005-2014')
ax.fill_between(maxT.index, minT, maxT, facecolor='magenta', alpha=0.25)
# Add scatters of breaking records in 2015.
maxT_new = dat_new[dat_new['Element'] == 'TMAX'].groupby('DateOfYear')['Data_Value'].max()
maxT_new.sort_index(inplace = True)
maxT_new = maxT_new[maxT_new > maxT]
minT_new = dat_new[dat_new['Element'] == 'TMIN'].groupby('DateOfYear')['Data_Value'].min()
maxT_new.sort_index(inplace = True)
minT_new = minT_new[minT_new < minT]
ax.scatter(maxT_new.index, maxT_new, color = 'red', s = 10, label = 'Breaking High in 2015')
ax.scatter(minT_new.index, minT_new, color = 'blue', s = 10, label = 'Breaking Low in 2015')
plt.legend(loc = 'best', frameon = False)
plt.show()