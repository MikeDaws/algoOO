# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:51:41 2019

@author: Mike
"""


import pandas as pd


#path='D:\Coding\Finance\algoOO\GBP_USD__08-08-2019.h5'
path='GBP_USD__08-08-2019.h5'

a=pd.read_hdf(path, 'df')