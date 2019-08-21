
'''
TODO 

1) sometimes the poll/stream function times out and stops recording data - need to create an exception/catch
   to retry the poll after a given wait



'''


from priceClass import priceClass
from dataClass import dataClass
import time
import os  
import common.config
import common.args
import datetime
import queue
import numpy as np
import threading
from bookKeeping import bookKeeping
import time
#import v20
from execution import Execution
from strategy import TestStrategy
from streaming import StreamingForexPrices


def trade(events, strategy, execution, instruments, data, bookKeep):
    """
    Carries out an infinite while loop that polls the
    events queue and directs each event to either the
    strategy component of the execution handler. The
    loop will then pause for "heartbeat" seconds and
    continue.
    """
    instrumentMarker=instruments
    while True:
        try:
            eventT = events.get(block=False)
            event=eventT[2]
#            print(event.instrument)
        except queue.Empty:
            pass
        else:
            if event is not None:
                if config.recordOnly == True:
                    if event.type == 'TICK':
                        index=instruments.index(event.instrument)
                        dataObject=data[index]
                        dataObject.storeData(event)                        
                if config.recordOnly == False:
                    if event.type == 'TICK':
    #                    print(intrument.index(event.instrument)
                        index=instruments.index(event.instrument)
                        dataObject=data[index]
                        dataObject.storeData(event)
    #                    print('tick')
                        strategy.calculate_signals(event,dataObject)
                        bookKeep.checkOpen(event)
                    elif event.type == 'ORDER':
    
                        bookKeep.record(event)
    #                    bookKeep.checkOpen(event)
                    elif event.type == 'EndBT':
                        instrumentMarker.remove(event.instrument)
            if len(instrumentMarker)==0 and events.empty():
                print('done')
                break
    #        if events.empty():
    #            print('done!')
    #            break
    #        time.sleep(heartbeat)



if __name__ == "__main__":
    heartbeat = 0.00001  # Half a second between polling
    events = queue.PriorityQueue()

    # Trade 10000 units of EUR/USD
    instruments = ["EUR_USD", "GBP_USD", "EUR_GBP", "UK100_GBP","NAS100_USD"]
#    instruments = ["EUR_USD"]
#
    path=common.config.default_config_path()
    config=common.config.make_config_instance(path) # this makes an instance of the config class and points it to the config file
    config.is_backTest=False
    backTestEndDate=datetime.datetime(2019,7,17)
    backTestDuration=datetime.timedelta(days=0)
    

    config.recordOnly= True
    
#     Create the OANDA market price streaming class
#     making sure to provide authentication commands
    prices = [None]*len(instruments)
    price_thread = [None]*len(instruments)
    data = [None]*len(instruments)
#    is_backTest=True
    for index,instrument in enumerate(instruments):
#        print(instrument)
        prices[index] = StreamingForexPrices(config,instrument, events)
        time.sleep(2)
        if config.is_backTest==False:
            price_thread[index] = threading.Thread(target=prices[index].stream_to_queue, args=[])
            data[index] = dataClass(config, instrument)
            price_thread[index].start()
        if config.is_backTest==True:
            data[index] = dataClass(config, instrument)            


    if config.is_backTest==True:
        price_thread[0] = threading.Thread(target=prices[index].historic_stream_to_queue, args=[backTestEndDate,backTestDuration,instruments])
        price_thread[0].start()



#        prices[index].stream_to_queue()
#
   

     
    # Handle errors while calling os.remove()
    if config.is_backTest==True:
        try:
            os.remove('bookKeepingstore.h5')
        except:
            pass

#
#    # Create the strategy/signal generator, passing the
#    # instrument, quantity of units and the events queue
    strategy = TestStrategy(events)

    bookKeep = bookKeeping(events, config)


#    # Create the execution handler making sure to
#    # provide authentication commands
    execution = Execution(config)
# 
##    # Create two separate threads: One for the trading loop
##    # and another for the market price streaming class
##    trade_thread = threading.Thread(target=trade, args=(events, strategy, execution))
    trade_thread = threading.Thread(target=trade, args=(events, strategy, execution, instruments,data,bookKeep))
#    price_thread = threading.Thread(target=prices[0].stream_to_queue, args=[])

    # Start both threads
    trade_thread.start()
#    price_thread.start()









#kwargs={}
#x=None
#kwargs["currency"]="EUR_GBP"
#x=priceClass(**kwargs)
#x.getPartialhistory(10)
#x.saveData()
#
#time.sleep(20)
#
#x.loadData()
#x.updateData()


#wait(1)
#kwargs["timeframe"]="15 min"
#x.changeTimeframe(**kwargs)
#time.sleep(11)
##x.updateData()

#trainingInput=dataClass()
#trainingInput.defaultSpec()