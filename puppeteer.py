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
  parser.add_option("-L", "--licence", action="store_true", default=False, help="Display license information and exit")
  parser.add_option("-l", "--list", action="store_true", default=False, help="Get the list of all nodes")
  (options, args) = parser.parse_args()

  if options.licence:
    print '\n'
    print __title__, __version__
    print __licence__
    sys.exit(0)
  if options.list:
    db = connect()
    nodes = db.nodes()
    for node in nodes:
      print(node)

if __name__ == "__main__":
  main()

