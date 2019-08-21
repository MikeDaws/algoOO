# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:08:20 2018

@author: Mike
"""

import random
import numpy as np
from event import OrderEvent
from simplePriceaction import simplePriceaction
from LSTM_NN import LSTM_NN


class TestStrategy(object):
    def __init__(self, events):
        self.events = events
        self.ticks = 0
        modelName = 'EUR_USD__17-07-2019_model2'
        normName ='EUR_USD__17-07-2019_normpara.h5'
#            print('executing strat')
        self.LSTMobject=LSTM_NN(modelName, normName, self.events)

    def calculate_signals(self, eventTick, data):
        if eventTick.type == 'TICK':
#            instrument = event.instrument
            self.ticks += 1
    #            print(data.df.index[-1], data.df['Instrument'][-1])
    #            print(event.time)
            
            self.ask=(eventTick.ask)
            self.bid=(eventTick.bid)
            self.time=eventTick.time
            self.instrument=eventTick.instrument
            self.spread=(self.ask)-(self.bid)
    #        
    #            
    #        if self.ticks % 101 == 0:
    #            side = random.choice(["buy", "sell"])
    #        print('asdsad')
#            SPriceaction=simplePriceaction(self.events)
#            SPriceaction.calc(self.instrument, data,self.spread)
#            del SPriceaction
#            

            self.LSTMobject.calc(self.instrument, data,self.spread)
#            del LSTMobject
#        print('printed')
            