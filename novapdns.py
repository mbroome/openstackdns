#!/usr/bin/python

import MySQLdb
import sys

import logging

# attach to our global logger
logger = logging.getLogger("novadns")

# lets talk to the powerdns database...
class pdnsDatabase:
   def __init__(self, config):
      self.config = config
      self.connection = None
      self.reconnectTries = 2

      self.forwardName = self.config.get('DNSZONE', 'forwardzone')
      self.reverseName = self.config.get('DNSZONE', 'reversezone')
      self.dbHost = self.config.get('MYSQL', 'mysqlhost')
      self.dbUser = self.config.get('MYSQL', 'mysqluser')
      self.dbPass = self.config.get('MYSQL', 'mysqlpass')
      self.dbName = self.config.get('MYSQL', 'mysqldatabase')

      logger.info("ZONES: forward: %s reverse: %s" % (self.forwardName, self.reverseName))
      logger.info("DB: host: %s user: %s pass: %s db: %s" % (self.dbHost, self.dbUser, self.dbPass, self.dbName))

      # connect to mysql
      self.connect()

      self.forwardID = self.getDomainID(self.forwardName)
      self.reverseID = self.getDomainID(self.reverseName)

   def connect(self):
      # close down an existing connection
      try:
         self.connection.close()
         self.connection = None
      except:
         pass

      # and now make a new connection
      try:
         self.connection = MySQLdb.connect(self.dbHost, self.dbUser, self.dbPass, self.dbName);
         self.connection.autocommit(True)
      except MySQLdb.Error, e:
         logger.info("MySQL error: %s" % (str(e)))
         sys.exit()

   def getDomainID(self, domain):
      try:
         cursor = self.connection.cursor()
         cursor.execute("SELECT id FROM domains WHERE name=%s", (domain))

         rows = cursor.fetchall()
         try:
            return(rows[0][0])
         except:
            pass
      except:
         pass

   def putRecord(self, name, content, type, domainID, instance):
      tryCounter = 0
      while tryCounter <= self.reconnectTries:      
         try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT count(*) from records where domain_id=%s and name=%s", (domainID, name))
            row = cursor.fetchone()
            if row[0] > 0:
               sql = "UPDATE records set content = %s, instance=%s, change_date=UNIX_TIMESTAMP() where domain_id=%s and name=%s;"
               r = cursor.execute(sql, (content, domainID, name, instance))
            else:
               sql = "INSERT INTO records (domain_id,name,content,type,ttl,prio,change_date,instance) VALUES (%s,%s,%s,%s,120,NULL,UNIX_TIMESTAMP(),%s);"
               r = cursor.execute(sql, (domainID, name, content, type, instance))
            break
         except:
            logger.info("Lost mysql connection, reconnecting")
            self.connect()

         tryCounter += 1

   def parsePTR(self, ip):
      fields = ip.split('.')
      fields.reverse()
      ptr = ".".join(fields) + '.in-addr.arpa'
      return(ptr)

   def update(self, hostname, ip, instance):
      name = ''
      ptr = self.parsePTR(ip)

      try:
         if hostname.endswith(self.forwardName):
            name = hostname
         else:
            name = hostname + '.' + self.forwardName
      except:
         name = hostname + '.' + self.forwardName

      logger.info("DNS Change: %s %s" % (name, ip))
      try:
         if self.forwardID != None:
            self.putRecord(name, ip, 'A', self.forwardID, instance)
         if self.reverseID != None:
            self.putRecord(ptr, name, 'PTR', self.reverseID, instance)
      except MySQLdb.Error, e:
         logger.info("MySQL Error %d: %s" % (e.args[0], e.args[1]))


   def remove(self, instance):
      tryCounter = 0
      while tryCounter <= self.reconnectTries:
         try:
            sql = "DELETE from records where instance=%s;"
            cursor = self.connection.cursor()
            r = cursor.execute(sql, (instance))
         except:
            logger.info("Lost mysql connection, reconnecting")
            self.connect()

         tryCounter += 1
