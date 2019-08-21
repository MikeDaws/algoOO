# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 12:45:49 2019

@author: Mike
"""
import pandas as pd
import matplotlib.pyplot as plt
import common.config
import common.args
import numpy as np
import datetime
from event import OrderEvent

#store = pd.read_hdf('testset.h5', 'df')

def simplePriceaction(events, store):
    #store
    bid=store['Bid'][-100:]
    upTick=0
    downTick=0
    upstreak=0
    downstreak=0
    upstreakCount=0
    maxUpstreak=0
    maxDownstreak=0
    logUpstreak=[]
    logDownstreak=[]
    downstreakCount=0
    upTickStore=[]
    downTickStore=[]
    
    bidDiff=np.zeros(len(bid))
    for ii in range(1,len(bid)):
        bidDiff[ii]=bid[ii]-bid[ii-1]
        if bidDiff[ii]>0:
            upTick+=1
            upTickStore.append(bidDiff[ii])
            if bidDiff[ii-1]>0:
                logDownstreak.append(downstreak)
                upstreak+=1
                upstreakCount+=1
                maxDownstreak=max(maxDownstreak,upstreak)
                downstreak=0
                
                if upstreakcount > 1 and ii>=len(bid)-1 and devUp>devDown and upTick>downTick:
                   # Buy
                    time = datetime.date.today()
                    order = OrderEvent(instrument, units, "market", 'buy', bid[-1], ask[-1], time, stopLoss, takeProfit)
                
                    events.put(order)
                   
                   
                   
                
        else:
            downTick+=1
            downTickStore.append(bidDiff[ii])
            if bidDiff[ii-1]<0:
                downstreak+=1
                maxUpstreak=max(maxUpstreak,upstreak)
                logUpstreak.append(upstreak)
                upstreak=0
                downstreakCount+=1
                
    devUp=np.std(upTickStore)
    devDown=np.std(downTickStore)
    
    np.std(bidDiff)
    total=np.sum(bidDiff)
    
    
    #logDownstreak=logDownstreak[logDownstreak!=0]
    np.asarray(logUpstreak)
    
    logUpstreak=np.trim_zeros(np.asarray(logUpstreak))
    logUpstreak=list(filter(lambda a: a != 0, logUpstreak))
    logDownstreak=list(filter(lambda a: a != 0, logDownstreak))
    #diff = store['Bid'][1:].astype(float)-store['Bid'][0:].astype(float)
    
    #store['df']['Bid'].astype(float).plot()
    #store['df']['Spread'].astype(float).plot()
    #plt.show()
    #
    
    
    #
    #
    ##Code to retrieve list of instruments
    #path=common.config.default_config_path()
    #config=common.config.make_config_instance(path) # this makes an instance of the config class and points it to the config file
    #account_id = config.active_account
    #
    #api = config.create_context()
    #
    #response = api.account.instruments(account_id)
    #
    #instruments = response.get("instruments", "200")
