#!/usr/bin/python

from configobj import ConfigObj


class novaConfig:
   def __init__(self, configFile=''):
      self.configFile = '/etc/config/openstack/dns.conf'
      try:
         if configFile:
            self.configFile = configFIle 
      except:
         pass

      self.config = ConfigObj(self.configFile)

   def get(self, key, value):
      try:
         if self.config[key][value]:
            return(self.config[key][value])
      except:
         pass
