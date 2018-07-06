import pandas as pd

class dataClass:
    
    
    def __init__(self):
        print("New inputdata container initialised")
        cols=['On_Off', 'Pair', 'Timeframe', 'Property', 'Normalisation']  
        self.inputArray=pd.DataFrame(columns=cols)
#        self.inputArray = self.inputArray()

    def setSpec(self, **kwargs):
#        tempSeries=pd.DataFrame(kwargs)
#        new_df = pd.DataFrame.from_dict(kwargs)

        self.inputArray=self.inputArray.append(kwargs, ignore_index=True)

#        print(self.inputArray)
        
        
    def setNewSpec(self, inputList):
#        tempSeries=pd.DataFrame(kwargs)
#        new_df = pd.DataFrame.from_dict(kwargs)
        cols=['On_Off', 'Pair', 'Timeframe', 'Property', 'Normalisation']  
        self.inputArray=pd.DataFrame(inputList)
        self.inputArray=self.inputArray[cols]
#        print(self.inputArray)
        
    def defaultInputSpec(self):
        
        inputDictList=[]
        inputDict={"On_Off": "1", "Pair": "EUR_USD", "Timeframe":"15M", "Property": "close", "Normalisation": "tanh"}
        inputDictList.append(inputDict)
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"15M", "Property": "open", "Normalisation": "tanh"}
        inputDictList.append(inputDict)
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"15M", "Property": "high", "Normalisation": "tanh"}
        inputDictList.append(inputDict)
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"15M", "Property": "low", "Normalisation": "tanh"}
        inputDictList.append(inputDict)
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"5M", "Property": "close", "Normalisation": "tanh"}
        inputDictList.append(inputDict)
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"5M", "Property": "open", "Normalisation": "tanh"}
        inputDictList.append(inputDict)
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"5M", "Property": "high", "Normalisation": "tanh"}
        inputDictList.append(inputDict)
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"5M", "Property": "low", "Normalisation": "tanh"}
        inputDictList.append(inputDict)    
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"1H", "Property": "close", "Normalisation": "tanh"}
        inputDictList.append(inputDict)
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"1H", "Property": "open", "Normalisation": "tanh"}
        inputDictList.append(inputDict)
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"1H", "Property": "high", "Normalisation": "tanh"}
        inputDictList.append(inputDict)
        inputDict={"On_Off": "1", "Pair": "EUR_USD","Timeframe":"1H", "Property": "low", "Normalisation": "tanh"}
        inputDictList.append(inputDict)

        #neural networks will be needed for each timeframe
        self.unique_values = set(e['Timeframe'] for e in inputDictList)
        print(unique_values)
        self.numUnique=len(unique_values)
        print(numUnique)
        self.setNewSpec(inputDictList)


    def getInputdata(self):
    #need someway of finding what pairs are currency in the input dict 
    #and generating priceClass object for each of these, this object should also be used in
    #the target data so the times match (can use through harddrive)
    
    #save the inputdata as a object which can be passed to the output class constructer
    #Based on unique values obtained previously
        self.inputData[0]=priceClass("EUR_GBP")
    
        pass
    
    def clearInputdata(self):
        self.inputData[0]=None
        pass

    def calcIndicators(self):
    #This method calculates the indicators
        pass
    
    def constructInputArray(self):
    #piece together all the bits to tick off inputDictList
        pass
    
    def outputArray(self):
        pass
    
