import sys
from qpid.messaging import *
import json
import logging

# attach to our global logger
logger = logging.getLogger("novadns")


class novaQueue:
   def __init__(self, config):
      self.config = config
      self.broker = self.config.get('QPID', 'qpidhost') + ':' + self.config.get('QPID', 'qpidport')

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


   def get(self, pdns):
      try:
         # open the connection and create a session
         self.connection.open()
         session = self.connection.session()

         # attach a receiver to the session
         receiver = session.receiver(self.address)

         # loop waiting for new messages
         while True:
            try:
               message = receiver.fetch(timeout=120)
               try:
                  # pull out the messages that we care about 
                  if message.content['event_type']:
                     if message.content['event_type'] == 'compute.instance.create.end':
                        instance = message.content['payload']
                        name = instance['display_name']
                        name = name.replace(' ', '-')
                        logger.info("Queue Add Message: %s %s %s" % (instance['instance_id'], name.lower(), instance['fixed_ips'][0]['address']))
                        pdns.update(name.lower(), instance['fixed_ips'][0]['address'], instance['instance_id'])
                     elif message.content['event_type'] == 'compute.instance.delete.end':
                        instance = message.content['payload']
                        logger.info("Queue Remove Message: %s" % (instance['instance_id']))
                        pdns.remove(instance['instance_id'])
               except:
                  pass
            except:
               pass
               #logger.exception("Timeout watching queue")

         # ack the message
         session.acknowledge()

      except MessagingError, e:
         logger.exception("Message Error")
      finally:
         self.connection.close()

