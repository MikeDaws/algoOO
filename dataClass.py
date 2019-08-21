# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 12:23:30 2019

@author: Mike
"""
import pandas as pd
import h5py    
import datetime
import tables


class dataClass(object):
    
    def __init__(self, config, instrument):
        self.config=config
        self.instrument=instrument
        self.timestamp=datetime.date.today()
        self.timestampstr =datetime.datetime.now().strftime("%d-%m-%Y")
        
        
        if config.is_backTest==False:
            try:
                path=self.instrument+"_"+'_'+self.timestampstr+'.h5'
                self.df=pd.read_hdf(path)
                timeIndex=self.df.index
                self.dtime=timeIndex.to_frame(index=False)
                
        
            except:        
                self.df = pd.DataFrame(columns=['Instrument','Ask', 'Bid', 'Spread'])
                self.dtime=pd.DataFrame(columns=['Time'])


        if config.is_backTest==True:
                self.df = pd.DataFrame(columns=['Instrument','Ask', 'Bid', 'Spread'])
                self.dtime=pd.DataFrame(columns=['Time'])
            
            
        self.savecount=100




    def storeData(self,event):
        if event.type=='TICK':
            self.ask=(event.ask)
            self.bid=(event.bid)
            self.time=event.time
            self.instrument=event.instrument
            self.spread=(self.ask)-(self.bid)
            dict_time={'Time':self.time}
            dict={'Instrument':self.instrument, 'Ask':self.ask, 'Bid':self.bid, 'Spread':self.spread}
            self.df=self.df.append(dict,ignore_index=True)
            self.dtime=self.dtime.append(dict_time,ignore_index=True)
            self.dtime['Time']=pd.to_datetime(self.dtime['Time'], utc=True)
            self.df.index=self.dtime['Time']
            


            count=len(self.df.index)            



            #Stores tick data to file every specified (savecount) number of ticks
            if count % self.savecount == 0 and self.config.is_backTest==False:                
                path=self.instrument+"_"+'_'+self.timestampstr+'.h5'
                self.df.to_hdf(path,'df',mode='w',table=True)
                print('done')
                
                #This section checks the current date against that of when the Data object was created
                    #if the object is found to enter a new day, a new object + file will be created
                if  self.timestamp < datetime.date.today():
                    self.__init__(self.config,self.instrument)
            
            
            

        
        
        
        
        
        
    def loadHistoricData(self):
        
        print()
        
        
    def getPartialhistory(self,config, n):
        a=self.currency
        b="S5"
        #n=1
#        t=time.time()s
        
        api = config.create_context()
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
            
            
            