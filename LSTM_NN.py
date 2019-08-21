# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:49:24 2019

@author: Mike
"""

import numpy as np
import h5py
import tensorflow as tf
import pandas as pd
from event import OrderEvent




class LSTM_NN():
    
    def __init__(self,modelName, normName, events):
        self.events = events
        self.modelName = modelName
        self.normName = normName
#        self.model = tf.keras.Sequential()
        self.model = tf.keras.models.load_model(self.modelName)

        
    def calc(self,instrument, X,spread):
#        X=pd.read_hdf('EUR_USD__17-07-2019.h5')
        
        #        self.events = events
        #model = tf.keras.Sequential()
#        model = tf.keras.models.load_model(self.modelName)
        
        X = X.df
        starter=self.model.get_input_shape_at(0)[1]
        print(len(X.index), starter)
        if len(X) >=starter:
            
            
            bid=X['Bid'][-starter:]
            ask=X['Ask'][-starter:]
            time=X.index[-starter:]
#            spreadrec=ask-bid

            X=X.drop('Instrument', axis=1)
            
            '''data has to be preprocessed to get the time in the right format - could also calculate some addition
            financial parameters here, could package it another class'''
            
            X['Time_cos']=np.cos((X.index.hour*60*60*1e06 + X.index.minute*60*1e06+X.index.second*1e-6+X.index.microsecond)*2*np.pi/8.64e+10)
            X['Time_sin']=np.sin((X.index.hour*60*60*1e06 + X.index.minute*60*1e06+X.index.second*1e-6+X.index.microsecond)*2*np.pi/8.64e+10)
            X=np.asarray(X)    
            X=X[-starter:]
            
            h5f=h5py.File(self.normName, 'r')
            datasets=list(h5f.keys())
            h5f=np.array(h5f.get(datasets[0]))
            X=X/h5f    
            X=X.reshape(-1,256,5)
            result=self.model.predict(X)
            units=1
            spreadmultiplierWin=3
            spreadmultiplierStop=2
#            spread=spreadrec[-1

            print(result.argmax())
            if result.argmax() == 0:
                profitValueBuy = spreadmultiplierWin*spread+ask[-1]
                stopValueBuy = ask[-1] - spreadmultiplierStop*spread
                order = OrderEvent(instrument, units, "market", 'buy', bid[-1], ask[-1], time[-1], stopValueBuy, profitValueBuy)
                self.events.put((1,time[-1],order))
        
        
            if result.argmax() == 1:            
                profitValueSell = bid[-1] - spreadmultiplierWin*spread
                stopValueSell = spreadmultiplierStop*spread + bid[-1]
                order = OrderEvent(instrument, units, "market", 'sell', bid[-1], ask[-1], time[-1], stopValueSell, profitValueSell)
                self.events.put((1,time[-1],order))

        