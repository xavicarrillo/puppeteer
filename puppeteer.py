#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Simple puppetdb client
It uses the pypuppetdb library: https://github.com/nedap/pypuppetdb
"""

__title__   = "puppeteer.py"
__version__ = "0.1"
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

from pypuppetdb import connect
from optparse import OptionParser
import sys

def main():

  parser = OptionParser(usage, version=__version__)
  #parser.add_option("-l", "--list", help="Get the list of all nodes")
  parser.add_option("-f", "--facts", type="string", action="store", dest="facts",
  help="Get fact from given node")
  (options, args) = parser.parse_args()
  
  factsout = ""
  db = connect()
  #if options.list:
  nodes = db.nodes()

  if options.facts:
    facts = options.facts.split(',')
    for node in nodes:
      for fact in facts:
        factsout = factsout + " " + node.fact(fact).value
      print '%s: %s' %(node,factsout)
      factsout = ""

  sys.exit(0)

if __name__ == "__main__":
  main()

