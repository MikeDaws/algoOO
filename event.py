# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 12:34:12 2018

@author: Mike
"""

class Event(object):
    pass


class TickEvent(Event):
    def __init__(self, instrument, time, bid, ask):
        self.type = 'TICK'
        self.instrument = instrument
        self.time = time
        self.bid = bid
        self.ask = ask


class OrderEvent(Event):
    def __init__(self, instrument, units, order_type, side, bid, ask, time, stopLoss, takeProfit):
        self.type = 'ORDER'
        self.instrument = instrument
        self.units = units
        self.order_type = order_type
        self.side = side
        self.bid = bid
        self.ask = ask
        self.time = time
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
#        print('new order')
        
        
        
class EndBT(Event):
    def __init__(self, instrument, time):
        self.type = 'EndBT'
        self.instrument = instrument
        self.time = time
