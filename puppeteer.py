#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Simple puppetdb client
"""

__title__   = "puppeteer.py"
__version__ = "0.3"
__author__  = "Xavi Carrillo"
__email__   = "xcarrillo at gmail dot com"
__licence__ ="""
  Copyright (c) 2014 Xavi Carrillo
  License: MIT
"""

usage = """
%prog [options]
Use --help to view options
"""

from pypuppetdb import connect # https://github.com/nedap/pypuppetdb
from optparse import OptionParser
from datetime import timedelta
import sys, datetime

def main():

  parser = OptionParser(usage, version=__version__)
  parser.add_option("-l", "--list", action='store_true', dest='list', help="Get the list of all nodes")
  parser.add_option("-f", "--facts", type="string", action="store", dest="facts",
  help="Get fact from given node")
  parser.add_option("-o", "--outofsync", action="store", dest="outofsync", default="30",
  help="Get the list of out of sync nodes (30 min without sending a report). Minutes can be passed as a parameter ")
  (options, args) = parser.parse_args()
  
  factsout  = ""
  db        = connect()
  nodes     = db.nodes()

  if options.list:
    for node in nodes:
      print node
    sys.exit(0)

  if options.facts:
    facts = options.facts.split(',')
    for node in nodes:
      for fact in facts:
        try:
          if '=' in fact:
            factarray= fact.split('=')
            fact=factarray[0]
            #print type(fact)
            if node.fact(fact).value == factarray[1]:
              print node
          else:
            factsout = factsout + " " + node.fact(fact).value
        except:
          print "Unexpected error:", sys.exc_info()[0]
          raise

      if factsout != "": # If there is an array of facts, print out all nodes, and the value of the facts
        try:
          print '%s: %s' %(node,factsout)
          factsout = ""
        except:
          print "Unexpected error:", sys.exc_info()[0]
          raise


  if options.outofsync:
    # there are 2 hours difference because of the timezone. So instead of dealing with pytz we use this workaround
    deltaminutes = 120
    now = datetime.datetime.now()
    delta = timedelta(minutes=int(deltaminutes))
    for node in nodes:
      try:
        lastcatalog = now - node.catalog_timestamp.replace(tzinfo=None) - delta
        minutes = lastcatalog.seconds / 60
      except:
        minutes = None
      if minutes > int(options.outofsync):
        print '%s has not sent a report within the last %s minutes' %(node.name,minutes)

  sys.exit(0)

if __name__ == "__main__":
  main()

