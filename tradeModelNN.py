# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 22:21:46 2018

@author: Mikw
"""

class tradeModelNN:
    
    def __init__(self,inputdata,outputdata):
        self.optimiseMode=0
        self.trainMode=1
        self.batchsize =100
        self.createTime
        pass
    
    
    def runModel(self):
        
        #define parameters
        
        #call split data if training
        
        #feed into neural network class
        
        #do nothing if just trainging
        
        #feed into backtest model if optimise
        
        #feed into returnSignal if not optimise or trains
        
        pass
    
    
    #parameters incude, nodes,layers, buy/sell threshold - any others?
    def optimiseParameters(self):
        self.optimiseMode=0
        
        #defineparmeter kwarg
        
        #call sklearn which calls self.runModel
        
        pass
    
    
    def partitionData(self):
        pass
    
    
    #return buy/sell/none back to mainframework
    def returnSignal(self): 
        
        pass
    
    
    
    def backTest(self):
        profit=0
        for ii in reversed(range(2,100)):        
            if predictions[-ii,0]>threshold and predictions[-ii,1]<predictions[-ii,0]:
                if Data[-ii+1,1]-Data[-ii,3]>n*spread and Data[-ii,3]-Data[-ii+1,2]<stoploss*spread :
                    profit=profit+(n/stoploss)
                else:
                    profit=profit-1
                
            elif predictions[-ii,1]>threshold and predictions[-ii,0]<predictions[-ii,1]:   
                if Data[-ii,3]-Data[-ii+1,2]>n*spread and Data[-ii+1,1]-Data[-ii,3]<stoploss*spread :
                    profit=profit+(n/stoploss)
                else:
                    profit=profit-1
                    
        return profit
        pass
        