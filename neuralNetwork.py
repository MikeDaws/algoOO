

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import os as os
#class NeuralNet():

import h5py




#def output(inputData,profitThreshold,stopLossThreshold):
#    output=[]
#
#    for ii in range(0,len(inputData)):
#        
#        '''assumes user buys - must clear a given profit amount and remain above a certain stopLossThreshold'''
#        spread = inputData['Spread'].iloc[ii]
#        profitValueBuy = profitThreshold*spread+inputData['Ask'].iloc[ii]
#        profitValueSell = inputData['Bid'].iloc[ii] - profitThreshold*spread
#        stopValueBuy = inputData['Ask'].iloc[ii] - stopLossThreshold*spread
#        stopValueSell = stopLossThreshold*spread + inputData['Bid'].iloc[ii]
#        buyLog=0
#        sellLog=0
#        outputBuy=0
#        outputSell=0
#        for jj in range(ii+1,len(inputData)):    #checks future values#
#            if inputData['Bid'].iloc[jj]>profitValueBuy:
#                outputBuy = 1
#                buyLog=ii
#                break
#            if inputData['Bid'].iloc[jj]<stopValueBuy:
#                outputBuy=0
#                buyLog=0
#                break
#        for jj in range(ii+1,len(inputData)):
#            if inputData['Ask'].iloc[jj]<profitValueSell:
#                outputSell = -1
#                sellLog=ii
#                break
#            if inputData['Ask'].iloc[jj]>stopValueSell:
#                outputSell=0
#                sellLog=0
#                break                
#        if outputBuy == 1 and outputSell == -1:
#            if buyLog<sellLog:
#                output.append(outputBuy)
#            elif buyLog>=sellLog:
#                output.append(outputSell)
#        else:
#            if abs(outputBuy)>abs(outputSell):
#                output.append(outputBuy)
#            else:
#                output.append(outputSell)
##        print(ii)
#    return output

def output(inputData,profitThreshold,stopLossThreshold):
    output=[]

    for ii in range(0,len(inputData)):
        
        '''assumes user buys - must clear a given profit amount and remain above a certain stopLossThreshold'''
        spread = inputData['Spread'].iloc[ii]
        profitValueBuy = profitThreshold*spread+inputData['Ask'].iloc[ii]
        profitValueSell = inputData['Bid'].iloc[ii] - profitThreshold*spread
        stopValueBuy = inputData['Ask'].iloc[ii] - stopLossThreshold*spread
        stopValueSell = stopLossThreshold*spread + inputData['Bid'].iloc[ii]
        buyLog=0
        sellLog=0
        outputBuy=0
        outputSell=0
        for jj in range(ii+1,len(inputData)):    #checks future values#
            if inputData['Bid'].iloc[jj]>profitValueBuy:
                outputBuy = [1,0,0]
                buyLog=ii
                break
            if inputData['Bid'].iloc[jj]<stopValueBuy:
                outputBuy=[0,0,1]
                buyLog=0
                break
        for jj in range(ii+1,len(inputData)):
            if inputData['Ask'].iloc[jj]<profitValueSell:
                outputSell = [0,1,0]
                sellLog=ii
                break
            if inputData['Ask'].iloc[jj]>stopValueSell:
                outputSell=[0,0,1]
                sellLog=0
                break                
        if outputBuy == [1,0,0] and outputSell == [0,1,0]:
            if buyLog<sellLog:
                output.append(outputBuy)
            elif buyLog>=sellLog:
                output.append(outputSell)
        else:
            if outputBuy==[1,0,0]:
                output.append(outputBuy)
            elif outputSell == [0,1,0]:
                output.append(outputSell)
            else:
                output.append([0,0,1])
                
#        print(ii)
    output=np.asarray(output)
    output = np.stack(output)
    return output


    
#def main():
X=pd.read_hdf('EUR_USD__17-07-2019.h5')
X=X.drop('Instrument', axis=1)
X['Time_cos']=np.cos((X.index.hour*60*60*1e06 + X.index.minute*60*1e06+X.index.second*1e-6+X.index.microsecond)*2*np.pi/8.64e+10)
X['Time_sin']=np.sin((X.index.hour*60*60*1e06 + X.index.minute*60*1e06+X.index.second*1e-6+X.index.microsecond)*2*np.pi/8.64e+10)


#pyplot.plot(X['Bid'])#


'''Set parameters for batching of data'''
batchSize=256
trainPercentage=0.95
spreadmultiplierWin=3.5
spreadmultiplierStop=2
numFeatures=5
nodes=512
manyToMany=0
testPercentage=1-trainPercentage#        
pad_length=batchSize-(len(X)%batchSize)





'''pad the data - needed for non-sliding window approaches'''
paddingFrame_x=[]
paddingFrame_y=[]
for ii in range(0,pad_length):
    paddingFrame_x.insert(0,{'Ask':0, 'Bid':0, 'Spread':0, 'Time_cos':0, 'Time_sin':0})
    paddingFrame_y.append(0)

X = pd.concat([pd.DataFrame(paddingFrame_x),X])
pad_check=len(X)%batchSize
divisionCount = len(X)/batchSize
trainSize = np.ceil(divisionCount*trainPercentage)
testSize = divisionCount-trainSize
Xpd=X


X=X.values





''' define output data'''
Y = output(Xpd,spreadmultiplierWin, spreadmultiplierStop)

\



'''structure the data in an appropriate manner to the problem being solved'''
if manyToMany == 1:
    x_batch=np.reshape(X,(-1,batchSize,numFeatures))
    y_batch = [*paddingFrame_y,*Y] #pad data
    y_batch = np.reshape(y_batch,(-1,batchSize))


''' OR implement a sliding window approach'''
if manyToMany == 0:
    x_batch=[] #use standard python list as can't be bothered working out size of a numpy array
    y_batch=[]
    for ii in range(0,len(X)-batchSize):
        x_batch.append(X[ii:batchSize+ii,:])
        y_batch.append(Y[ii+batchSize])
    x_batch=np.asarray(x_batch)
    x_batch=np.stack(x_batch)
    y_batch=np.asarray(y_batch)
    y_batch=np.stack(y_batch)
    
    '''split into training and test sets - leave validation here'''
    divisionCount = len(x_batch)
    trainSize = int(np.ceil(divisionCount*trainPercentage))
#    testSize = divisionCount-trainSize    
    x_batch_train=x_batch[0:trainSize,:,:]/np.max(np.max(x_batch[:,:,:],axis=0),axis=0)
    x_batch_test=x_batch[trainSize:,:,:]/np.max(np.max(x_batch[:,:,:],axis=0),axis=0)
    y_batch_train=y_batch[0:trainSize]
    y_batch_test=y_batch[trainSize:]
    


#model = tf.keras.Sequential([
#    tf.keras.layers.LSTM(nodes),
##    tf.keras.layers.LSTM(nodes, activation='relu'), 
##    tf.keras.layers.Dense(nodes, activation='tanh'), 
#    tf.keras.layers.Dense(1, activation='tanh')
#])
#    
checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create checkpoint callback
cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1, period=20)

model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(nodes,return_sequences=True, input_shape=( batchSize,5)))
model.add(tf.keras.layers.LSTM(nodes,return_sequences=True, input_shape=( batchSize,5)))
model.add(tf.keras.layers.LSTM(nodes,return_sequences=True, input_shape=( batchSize,5)))

#model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.LSTM(nodes))
#model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dense(nodes, activation='tanh'))
#model.add(tf.keras.layers.BatchNormalization())

#model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dense(int(np.ceil(nodes/2)), activation='tanh'))
model.add(tf.keras.layers.Dense(int(np.ceil(nodes/4)), activation='tanh'))

model.add(tf.keras.layers.Dense(3, activation='softmax'))
print(model.summary())

model.compile(optimizer=tf.keras.optimizers.Adam(0.000001),
              loss=tf.keras.backend.categorical_crossentropy,
              metrics=['categorical_accuracy', 'Precision', 'Recall'])

norm_para = np.max(np.max(x_batch[:,:,:],axis=0),axis=0)
h5f = h5py.File('EUR_USD__17-07-2019_normpara.h5','w')
h5f.create_dataset('EUR_USD__17-07-2019', data =norm_para)
h5f.close()


loss_rec=[]
acc_rec=[]
validation_rec=[]



for ii in range(0,100):
    history_fit=model.fit(x_batch_train, y_batch_train, epochs=50, validation_data=(x_batch_test,y_batch_test))
    
    loss_rec+=history_fit.history['loss']
    acc_rec+=history_fit.history['categorical_accuracy']
    validation_rec+= history_fit.history['val_categorical_accuracy']
    
    plt.plot(loss_rec)
    plt.plot(acc_rec)
    plt.plot(validation_rec)
    plt.show()




result=model.predict(x_batch_train)
#
#result_test=model.predict(x_batch_test)
##
##
#
model.save('test')
##
#h5f = h5py.File('EUR_USD__17-07-2019_normpara.h5','r')
#norm_para = h5f['EUR_USD__17-07-2019'][:]
##
##
#h5f.close()
##
##
##
##
##
##endtraining=len(inputs)-(predicted+1)
##
##endtest=len(inputs)-1
##
##cut =(endtraining-starttraining) % seqLength
##adjustedStart=starttraining+cut
##starttest=endtest-(endtraining-adjustedStart)    
##
##normIn, normOut = inOut(inputs, adjustedStart, endtraining, len(history),targetHistory,spread, predIn)    
##indicatorVal=len(inputs)-(endtraining-adjustedStart)
##normindVal = inOnly(inputs, indicatorVal, len(inputs), len(history))    
##x_batches_nonnorm = inputs[adjustedStart:endtraining,:].reshape(-1, seqLength, len(inputs[1]))
##x_ind = normindVal.reshape(-1, seqLength, len(normIn[1]))
#
#normIn=normIn[-dataAmount:,:]
#normOut=normOut[-dataAmount:,:]
#historyUsed=history1[-dataAmount:,:]
#
#x_batches = normIn.reshape(-1, seqLength, len(normIn[1]))
#y_batches = normOut.reshape(-1, seqLength, num_classes)
#
#
#
##x_batches_test = normInTest.reshape(-1, seqLength, len(normIn[1]))
##y_batches_test = normOutTest.reshape(-1, seqLength, 1)
#testData=normOut[-100:,:]
#output=y_batches.shape[2]
#num_periods=y_batches.shape[1]
#tf.reset_default_graph()   #We didn't have any previous graph objects running, but this would reset the graphs
