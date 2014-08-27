#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
PuppetDB client, that uses the PyPuppetDB library (https://github.com/nedap/pypuppetdb)
"""

__title__   = "puppeteer.py"
__version__ = "0.5"
__author__  = "Xavi Carrillo"
__email__   = "xcarrillo at gmail dot com"
__licence__ = "Copyright (c) 2014 Xavi Carrillo. License: MIT"
__usage__   = """
%prog [options]
Use --help to view options
Example:  python puppeteer.py -f operatingsystem=CentOS,operatingsystemrelease=6.5,puppetversion=3.6.2
"""
from pypuppetdb import connect
from optparse import OptionParser
from datetime import timedelta
import sys, datetime

def main():

  parser = OptionParser(usage=__usage__, version=__version__)
  parser.add_option("-l", "--list", action='store_true', dest='list', help="Get the list of all nodes")
  parser.add_option("-f", type="string", action="store", dest="facts",
  help="Get fact value from all nodes. Can be as many as you want, comma separated")
  parser.add_option("-o", action="store", dest="outofsync", default="30",
  help="Get list of out of sync nodes (30 min without sending a report). Number of mins can be passed as a parameter")
  (options, args) = parser.parse_args()
  if len(sys.argv)==1:
    print __usage__
    sys.exit(1)

  db    = connect()
  nodes = db.nodes()

  if options.list:
    for node in nodes:
      print node
    sys.exit(0)

  if options.facts:
    facts     = options.facts.split(',')
    factsout  = ""
    for node in nodes:
      matchfacts    = 0
      factlistindex = -1 
      for fact in facts:
        factlistindex += 1
        try:
          # If the user gives a value to the fact...
          if '=' in fact:
            factarray= fact.split('=')
            fact=factarray[0]
            if node.fact(fact).value == factarray[1]:
              matchfacts +=1
          else:
            factsout = factsout + " " + node.fact(fact).value
        except:
          print "Unexpected error:", sys.exc_info()[0]
          raise
      if matchfacts == len(facts):
        # Good! all the given facts have the desired value on this node
        print node

      if factsout != "": # If there is an array of facts, it means that the user didn't pass a value for the fact,
                         # so we print out all nodes, and the value of the facts
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

