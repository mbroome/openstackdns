#!/usr/bin/python
import sys
from qpid.messaging import *
import json

import pprint

pp = pprint.PrettyPrinter(indent=4)

class novaQueue:
   def __init__(self):
      self.broker = "192.168.95.20:5672"

      self.connection = Connection(self.broker)

      # setup the options to browse the exchange
      self.addr_opts = {
            "create": "always",
            "mode": "browse",
            "node": {
                "type": "topic",
                "x-declare": {
                    "durable": True,
                    "auto-delete": False,
                },
            },
         }
      # attache to the 'nova' exchange with the options
      self.address = "%s ; %s" % ('nova', json.dumps(self.addr_opts))


   def get(self):
      try:
         # open the connection and create a session
         self.connection.open()
         session = self.connection.session()

         # attach a receiver to the session
         receiver = session.receiver(self.address)

         # loop waiting for new messages
         while True:
            message = receiver.fetch(timeout=120)
            pp.pprint(message.content)
            print "\n"
            #try:
            #   # pull out the messages that we care about
            #   if message.content['event_type'] == 'compute.instance.create.end':
            #      instance = message.content['payload']
            #      pp.pprint(instance)
            #except:
            #   pass

         session.acknowledge()

      except MessagingError,m:
         print m
      finally:
         self.connection.close()

q = novaQueue()
q.get()

