# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 06:51:53 2024

@author: rodney.viereck
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from PIL import Image
import datetime as dt
from datetime import timedelta as tdelta

# from scipy.ndimage.filters import uniform_filter1d

# def untuple(x):
#     return x

# ipath_see = "C:/Users/rodney.viereck/Documents/Python/EUV_2/stan_bands/"
ipath_goes = "C:/Users/rodney.viereck/Documents/Python/EUV_2/combined/"
# ipath = "C:/Users/rodney.viereck/Documents/Python/EUV_2/combined/"

ifile = 'GOES_lines_2018-2024.dat'
# ifile = "NRL_Spec.csv"



scatter_plot = False
# scatter_plot = True

#Load GOES_Lines

goes_lines_df = pd.read_csv(ipath_goes+ifile)
goes_lines_df['Datetime'] = pd.to_datetime(goes_lines_df['Datetime'])
goes_lines_df.set_index('Datetime', inplace = True)
goes_columns = goes_lines_df.columns

goes_lines_df['G_280.0_goes'] =  .8 * goes_lines_df['G_280.0_goes']  - .059

#Create Daily Averages
goes_lines_da_df = goes_lines_df.groupby(goes_lines_df.index.strftime("%Y-%m-%d")).mean()
goes_lines_da_df.index = pd.to_datetime(goes_lines_da_df.index)


fig, ax1 = plt.subplots()

c1 = goes_lines_df.columns

col = 1

pmin = 0.9 * goes_lines_da_df[c1[col]].min()
pmax = 1.1 * goes_lines_da_df[c1[col]].max()


if scatter_plot:
    ax1.scatter(goes_lines_da_df[c1[col]],goes_lines_da_df[c1[col + 8]]
                ,color = 'red',s=.2, label = 'GOES vs SEE')
    
    ax1.plot()
    
    # Plot line on diagonal
    
    p1 = [pmin, pmax]
    p2 = p1
    
    ax1.plot(p1,p2, color = 'black', linewidth = .5, label = "1-1 line")
    
    
    
    lim1 = [pmin,pmax]
    lim2 = [pmin,pmax]
    ax1.set_ylim(lim1)
    ax1.set_xlim(lim2)
    
    ax1.set_xlabel(c1[col])
    ax1.set_ylabel(c1[col+8])
    # ax1.set_xlabel("SCIAMACHI")

else:
    ax1.plot(goes_lines_da_df[c1[col]],label = c1[col], color = 'blue')
    ax1.plot(goes_lines_da_df[c1[col+8]],label = c1[col+8], color = 'red')
    
    ax1.legend(loc = 'lower right')

plt.plot()



