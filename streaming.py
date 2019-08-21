# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 18:51:03 2018

@author: Mike
"""

import requests
import json
import pandas as pd
import datetime
import time as Time
#import common.config

from event import TickEvent
from event import EndBT

class StreamingForexPrices:
    def __init__(self, config, instruments, events_queue):
        
        self.domain = config.streaming_hostname
        self.access_token = config.token
        self.account_id = config.username
        self.instruments = instruments
        self.events_queue = events_queue
        self.config=config

    def connect_to_stream(self):
        try:
            
#            api=config.create_context()
            streaming_api=self.config.create_streaming_context()
            resp = streaming_api.pricing.stream(self.account_id,instruments=self.instruments)

            return resp
        
        
        except Exception as e:
#            s.close()
            print("Caught exception when connecting to stream\n" + str(e))
            Time.sleep(3600)
            self.connect_to_stream()
    def stream_to_queue(self):
       
        try:
            response = self.connect_to_stream()
            a=response.lines
    #        print(response)
            if response.status != 200:
                print("bad request")
                Time.sleep(3600)
                self.stream_to_queue()
                return
            for line in response.lines:
                if line:
                    try:
                        msg = json.loads(line)
    #                    print(msg)
                    except Exception as e:
                        print("Caught exception when converting message into json\n" + str(e))
                        Time.sleep(3600)
                        self.stream_to_queue()
                        return
                    if "instrument" in msg or "tick" in msg:
    #                    print(msg)
                        instrument = msg["instrument"]
                        time = msg["time"]
    #                    bid = msg["bids"]
    #                    ask = msg["asks"]
                        ask = float(msg['asks'][0]["price"])
                        bid=float(msg['bids'][0]["price"])
    
                        tev = TickEvent(instrument, time, bid, ask)
                        self.events_queue.put((2,time,tev))
        except Exception:
            Time.sleep(3600)
            self.stream_to_queue()

                    
    def historic_stream_to_queue(self, dateTo, duration,instrumentList):
        
        dateFrom=dateTo-duration
        
        delta = dateTo - dateFrom
        dataStore=[]
        for index,instrument in enumerate(instrumentList):
            for ii in range(delta.days + 1):
                fileDates=((dateFrom + datetime.timedelta(days=ii))).strftime("%d-%m-%Y")
                path=instrument+"_"+'_'+fileDates+".h5"
                dataStore.append(pd.read_hdf(path, 'df'))
        data=pd.concat(dataStore)
        data=data.sort_index()
        
        for ii in range(len(data)):
            instrument = data['Instrument'][ii]
            time = data.index[ii]
            bid = data['Bid'][ii]
            ask = data['Ask'][ii]
            tev = TickEvent(instrument, time, bid, ask)
            self.events_queue.put((2,time,tev))
#            Time.sleep(0.1)
#            print(time, bid, ask)
        tend=EndBT(instrument, time)
        self.events_queue.put((3,time,tend))
        print('end of stream')