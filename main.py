# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 13:16:59 2018

@author: Mikw
5"""

from priceClass import priceClass
from dataClass import dataClass
import os
import time
import argparse
import common.config
import common.args

import queue
import threading
import time

from execution import Execution
from settings import STREAM_DOMAIN, API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID
from strategy import TestRandomStrategy
from streaming import StreamingForexPrices


def trade(events, strategy, execution):
    """
    Carries out an infinite while loop that polls the
    events queue and directs each event to either the
    strategy component of the execution handler. The
    loop will then pause for "heartbeat" seconds and
    continue.
    """
    while True:
        try:
            event = events.get(False)
        except Queue.Empty:
            pass
        else:
            if event is not None:
                if event.type == 'TICK':
                    strategy.calculate_signals(event)
                elif event.type == 'ORDER':
                    print("Executing order!")
                    execution.execute_order(event)
        time.sleep(heartbeat)



if __name__ == "__main__":
    heartbeat = 0.5  # Half a second between polling
#    events = Queue.Queue()

    # Trade 10000 units of EUR/USD
    instrument = "EUR_USD"
    units = 10000
    

#    parser = argparse.ArgumentParser()
#    common.config.add_argument(parser)
#    args = parser.parse_args()
#    api = args.config.create_context()
#    common.config.

#    configClass=common.config.Config()
    path=common.config.default_config_path()
    config=common.config.make_config_instance(path) # this makes an instance of the config class and points it to the config file
    api=config.create_context()
    streaming_api=config.create_streaming_context()
    
    # Create the OANDA market price streaming class
    # making sure to provide authentication commands
    prices = StreamingForexPrices(
        STREAM_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID,
        instrument, events
    )

    # Create the execution handler making sure to
    # provide authentication commands
    execution = Execution(API_DOMAIN, ACCESS_TOKEN, ACCOUNT_ID)

    # Create the strategy/signal generator, passing the
    # instrument, quantity of units and the events queue
    strategy = TestRandomStrategy(instrument, units, events)

    # Create two separate threads: One for the trading loop
    # and another for the market price streaming class
    trade_thread = threading.Thread(target=trade, args=(events, strategy, execution))
    price_thread = threading.Thread(target=prices.stream_to_queue, args=[])

    # Start both threads
    trade_thread.start()
    price_thread.start()









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