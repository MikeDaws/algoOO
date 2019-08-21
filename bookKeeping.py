# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 18:22:13 2019

@author: Mike
"""

import numpy as np
from event import OrderEvent
import pandas as pd
import datetime


class bookKeeping(object):
    def __init__(self, events,config):
        self.events = events
        self.ticks = 0

        
        try:
            self.books=pd.read_hdf('bookKeepingstore.h5')
        
        except:
            self.books = pd.DataFrame(columns=['Instrument','Ask', 'Bid', 'Spread', 'Units', 'Side', 'StopLoss', 'TakeProfit', 'FillTime', 'NetProfit', 'IsOpen'])
#            self.dtime=pd.DataFrame(columns=['Time'])

        self.config=config
       



    def record(self, event):
        instrument = event.instrument
        
        isOpen=self.books['IsOpen']==True
        openOrders=self.books[isOpen]
#        print(len(openOrders.index))
        openOrdersInstr=openOrders['Instrument']==instrument     
        openOrdersCheck=openOrders[openOrdersInstr]
#        print('wut wut')
#        print(len(openOrdersCheck.index))
        if len(openOrdersCheck) == 0 or len(self.books.index)==0 :
            units = event.units
            side = event.side 
            isOpen=True
            stopLoss=event.stopLoss
            takeProfit=event.takeProfit
            netProfit=0
            ask=(event.ask)
            bid=(event.bid)
            time=event.time
            fillTime=datetime.date.today()
            netProfit=0
            spread=(ask)-(bid)
            dict_time={'Time':time}
            dict={'Instrument':instrument, 'Ask':ask, 'Bid':bid, 'Spread':spread, 'Units':units, 'Side':side,
                  'StopLoss':stopLoss, 'TakeProfit':takeProfit, 'FillTime':fillTime, 'NetProfit':netProfit,'IsOpen':isOpen}
            self.books=self.books.append(dict,ignore_index=True)
            
            
#            if side == 'buy':
#                print('buy')
#                
#            if side == 'sell':
#                print('sell')
            
    #        self.dtime=self.dtime.append(dict_time,ignore_index=True)
    #        self.dtime['Time']=pd.to_datetime(self.dtime['Time'])
    #        self.books.index=self.dtime['Time']
            self.books.dtypes
            self.books.to_hdf('bookKeepingstore.h5', 'books')
    #        checkOpen(event)
        
        
        
    def checkOpen(self, event):
        
        #first filter all the closed orders
        isOpen=self.books['IsOpen']==True
        openOrders=self.books[isOpen]
        
        for row in openOrders.itertuples(index=True, name='orders'):
            if row.Side == 'buy':
                #check if current bid price exceeds take profit (ask price is the higher price    buy at ask price, sell at bid)
                if event.bid >= row.TakeProfit:
#                    self.books['IsOpen'][row.Index]=0;
                    self.books.at[row.Index,'IsOpen']=0;
                    self.books.at[row.Index,'NetProfit']=row.TakeProfit-row.Ask
                    print('buy -Profit - Position closed', row.TakeProfit, row.Ask, event.bid, row.TakeProfit-row.Ask)
                if event.bid <= row.StopLoss:
                    self.books.at[row.Index,'IsOpen']=0;
                    self.books.at[row.Index,'NetProfit']=row.StopLoss-row.Ask                
                    print('buy -Stop loss - Position closed', row.StopLoss, row.Ask, event.bid, row.StopLoss-row.Ask)
                #check if current bid price is lower than stoploss
                
            if row.Side == 'sell':
                if event.ask <= row.TakeProfit:
                    self.books.at[row.Index,'IsOpen']=0;
                    self.books.at[row.Index,'NetProfit']=-row.TakeProfit+row.Bid
                    print('short -profit - Position closed',row.TakeProfit, row.Bid, event.ask, -row.TakeProfit+row.Bid)
                    
                if event.ask >= row.StopLoss:
                    self.books.at[row.Index,'IsOpen']=0;
                    self.books.at[row.Index,'NetProfit']=-row.StopLoss+row.Bid                
                    print('short -stop loss -Position closed', row.StopLoss, row.Bid, event.ask, -row.StopLoss+row.Bid )
                
                
                
#        print('chc')
                
        self.books.to_hdf('bookKeepingstore.h5', 'books')

        
        