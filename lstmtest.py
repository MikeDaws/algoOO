# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:00:55 2019

@author: Mike
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:49:24 2019

@author: Mike
"""

import numpy as np
import h5py
import tensorflow as tf
import pandas as pd


X=pd.read_hdf('EUR_USD__17-07-2019.h5')

#        self.events = events
#model = tf.keras.Sequential()
model = tf.keras.models.load_model('EUR_USD__17-07-2019_model2.h5')

        
starter=model.get_input_shape_at(0)[1]
if len(X) >=starter:
    
    X=X.drop('Instrument', axis=1)
    X['Time_cos']=np.cos((X.index.hour*60*60*1e06 + X.index.minute*60*1e06+X.index.second*1e-6+X.index.microsecond)*2*np.pi/8.64e+10)
    X['Time_sin']=np.sin((X.index.hour*60*60*1e06 + X.index.minute*60*1e06+X.index.second*1e-6+X.index.microsecond)*2*np.pi/8.64e+10)
    X=np.asarray(X)    
    X=X[-starter:]
    
    h5f=h5py.File('EUR_USD__17-07-2019_normpara.h5', 'r')
    datasets=list(h5f.keys())
    h5f=np.array(h5f.get(datasets[0]))
    X=X/h5f    
    X=X.reshape(-1,256,5)
    result=model.predict(X)

    

    if result.argmax() == 1


    if result.argmax() == 2:
        order = OrderEvent(instrument, units, "market", 'sell', bid[-1], ask[-1], time[-1], stopLoss, takeProfit)
        self.events.put((1,time[-1],order))
    
            
        