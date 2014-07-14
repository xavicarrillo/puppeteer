#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
Simple puppetdb wrapper
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

def main():
  db = connect()
  nodes = db.nodes()
  for node in nodes:
    print(node)

if __name__ == "__main__":
  main()

