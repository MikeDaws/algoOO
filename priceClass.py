import argparse
import common.config
import common.args
from datetime import datetime#
import numpy as np
import array
from datetime import datetime, timedelta
import time
import pandas as pd
import h5py    
import tables

class priceClass:
    
    currency="EUR_USD"
    timeFrame="S5"
    
    def __init__(self,**kwargs):
        if "currency" in kwargs:
            self.currency = kwargs["currency"]

    def saveData(self):
        store = pd.HDFStore(self.currency+"_"+'store.h5')
        store['timeseries']=self.timeseries
        store.close
        
        
    def loadData(self):
        store = pd.HDFStore(self.currency+"_"+'store.h5')
        self.timeseries = store['timeseries']
        store.close
        
        
    def changeTimeframe(self,**kwargs):
        if "timeframe" in kwargs:
            timeframe=kwargs["timeframe"]
            try:
                ohlc_dict = {'o':'first', 'h':'max', 'l':'min', 'c': 'last', 'volume':'sum'}
                self.newTimeseries=self.timeseries.resample(timeframe).agg(ohlc_dict)
                cols=['o', 'h', 'l', 'c', 'volume']  
                self.newTimeseries = self.newTimeseries[cols]
            except:
                print("timeframe not recongised/found")
                
    def updateData(self):
        
        
        a=self.currency
        b="S5"
        #n=1
#        t=time.time()s
        
        parser = argparse.ArgumentParser()
        common.config.add_argument(parser)
        args = parser.parse_args()
        api = args.config.create_context()
#        storeCandles=[]
#        A1=datetime.now()
        kwargs={}
        storeDict=[]
        candles=[]
        ii=0
        timeStamp=self.timeseries.index.max()
        fromTime=timeStamp.to_pydatetime()
        fromTimestr=str(fromTime.year)+"-"+str(fromTime.month)+"-"+str(fromTime.day)+"T"+str(fromTime.hour)+":"+str(fromTime.minute)+":"+str(fromTime.second)+".000000000Z"
        kwargs["fromTime"]=fromTimestr
        currentTime=datetime.now()
#        print("%Y-%m-%dT%H:%M:%S.000000000Z",(currentTime.year, currentTime.month, currentTime.day,currentTime.hour, currentTime.minute, currentTime.second))
        
        while fromTime<currentTime-timedelta(seconds=4.9):
#                kwargs = {}
                kwargs["granularity"] = b
                kwargs["count"] = 5000
           
#                if ii>0:
                kwargs["fromTime"]=fromTimestr



                while True:
                    try:
                        response = api.instrument.candles(a, **kwargs)
                        candles = response.get("candles", 200)
                        break
                    except:
                     time.sleep(2)
                     print("error")
            #        time.sleep(0.5)
                if candles != []:
                    for jj in range(0,len(candles)):
                        temp1=vars(candles[jj].mid)
                        temp2={"volume":candles[jj].volume}
                        temp3={"time":datetime.strptime(candles[jj].time,"%Y-%m-%dT%H:%M:%S.000000000Z")}
                        dict1={**temp1, **temp2, **temp3}
                        storeDict.append(dict1)
        
        #            storeCandles.append(candles)
                    print(ii)
                    ii=ii+1
#                timeStamp=self.timeseries.index.max()
#                fromTime=timeStamp.to_pydatetime()
                fromTime=datetime.strptime(candles[-1].time,"%Y-%m-%dT%H:%M:%S.000000000Z")
                fromTimestr=str(fromTime.year)+"-"+str(fromTime.month)+"-"+str(fromTime.day)+"T"+str(fromTime.hour)+":"+str(fromTime.minute)+":"+str(fromTime.second)+".000000000Z"
                kwargs["fromTime"]=fromTimestr
#                currentTime=datetime.now()
        candles=None
        tempseries=pd.DataFrame(storeDict)
        storeDict=None
        tempseries=tempseries.astype({"time":datetime})
        tempseries=tempseries.set_index('time')
#        elapsed = time.time() - t
        tempseries=tempseries.sort_index()
        self.timeseries=tempseries
        
        
        
    def getPartialhistory(self,n):
        a=self.currency
        b="S5"
        #n=1
#        t=time.time()s
        
        parser = argparse.ArgumentParser()
        common.config.add_argument(parser)
        args = parser.parse_args()
        api = args.config.create_context()
#        storeCandles=[]
#        A1=datetime.now()
        storeDict=[]
        candles=[]
        ii=0
        while ii<n:
                kwargs = {}
                kwargs["granularity"] = b
                kwargs["count"] = 5000
           
                if ii>0:
                    kwargs["toTime"] = candles[0].time
                while True:
                    try:
                        response = api.instrument.candles(a, **kwargs)
                        candles = response.get("candles", 200)
                        break
                    except:
                     time.sleep(2)
                     print("error")
            #        time.sleep(0.5)
                if candles != []:
                    for jj in range(0,len(candles)):
                        temp1=vars(candles[jj].mid)
                        temp2={"volume":candles[jj].volume}
                        temp3={"time":datetime.strptime(candles[jj].time,"%Y-%m-%dT%H:%M:%S.000000000Z")}
                        dict1={**temp1, **temp2, **temp3}
                        storeDict.append(dict1)
        
        #            storeCandles.append(candles)
                    print(ii)
                    ii=ii+1

        
        candles=None
        tempseries=pd.DataFrame(storeDict)
        storeDict=None
        tempseries=tempseries.astype({"time":datetime})
        tempseries=tempseries.set_index('time')
#        elapsed = time.time() - t
        tempseries=tempseries.sort_index()
        self.timeseries=tempseries
        
        
    def getFullhistory(self):
        a=self.currency
        b="S5"
        #n=1
#        t=time.time()s
        
        parser = argparse.ArgumentParser()
        common.config.add_argument(parser)
        args = parser.parse_args()
        api = args.config.create_context()
#        storeCandles=[]
#        A1=datetime.now()
        storeDict=[]
        candles=[]
        for ii in range(0,10000):
                kwargs = {}
                kwargs["granularity"] = b
                kwargs["count"] = 5000
           
                if ii>0:
                    kwargs["toTime"] = candles[0].time
        #        time.sleep(0.5)    
                while True:
                    try:
                        response = api.instrument.candles(a, **kwargs)
                        candles = response.get("candles", 200)
                        break
                    except:
                     time.sleep(2)
                     print("error")
            #        time.sleep(0.5)
                if candles != []:
                    for jj in range(0,len(candles)):
                        temp1=vars(candles[jj].mid)
                        temp2={"volume":candles[jj].volume}
                        temp3={"time":datetime.strptime(candles[jj].time,"%Y-%m-%dT%H:%M:%S.000000000Z")}
                        dict1={**temp1, **temp2, **temp3}
                        storeDict.append(dict1)
        
        #            storeCandles.append(candles)
                    print(ii)
        
        candles=None
        tempseries=pd.DataFrame(storeDict)
        storeDict=None
        tempseries=tempseries.astype({"time":datetime})
        tempseries=tempseries.set_index('time')
#        elapsed = time.time() - t
        tempseries=tempseries.sort_index()
        self.timeseries=tempseries