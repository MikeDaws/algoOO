# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:36:44 2019

@author: Geoff
"""


from priceClass import priceClass
import pandas as pd
from dataClass import dataClass
import time
import argparse
import common.config
import common.args
import datetime
import queue
import threading
from bookKeeping import bookKeeping
import time
import event
from execution import Execution
#from settings import STREAM_DOMAIN, API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID
from strategy import TestStrategy
from streaming import StreamingForexPrices




events = queue.Queue()


path=common.config.default_config_path()
config=common.config.make_config_instance(path) # this makes an instance of the config class and points it to the config file
config.is_backTest=True

bookKeep = bookKeeping(events, config)



instrument='EUR_USD'
units=10
side='buy'
bid=1.1
ask=1.2
time=datetime.date.today()
stopLoss=1.0
takeProfit=1.4

#eventOrder = event.OrderEvent(instrument, units, "market", side, bid, ask, time,stopLoss,takeProfit)
#
#
#bookKeep.record(eventOrder)
#
books=pd.read_hdf('bookKeepingstore.h5')
#
#ask=1
#bid=0.9
#eventTick = event.TickEvent(instrument, time, bid, ask)
#
#bookKeep.checkOpen(eventTick)
#book1=pd.read_hdf('bookKeepingstore.h5')
#store1=pd.read_hdf('EUR_USD__12-07-2019.h5')



#data = dataClass(config, instrument)