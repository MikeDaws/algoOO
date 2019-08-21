# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:07:46 2018

@author: Mike
"""

import http.client as httplib
import urllib


class Execution(object):
    def __init__(self, config):
        self.domain = config.streaming_hostname
        self.access_token = config.token
        self.account_id = config.username
        self.conn = self.obtain_connection()

    def obtain_connection(self):
        return httplib.HTTPSConnection(self.domain)

    def execute_order(self, event):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + self.access_token
        }
        params = urllib.urlencode({
            "instrument" : event.instrument,
            "units" : event.units,
            "type" : event.order_type,
            "side" : event.side
        })
        self.conn.request(
            "POST",
            "/v1/accounts/%s/orders" % str(self.account_id),
            params, headers
        )
        response = self.conn.getresponse().read()
        print(response)
        
        
        