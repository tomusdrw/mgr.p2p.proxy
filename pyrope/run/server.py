# -*- coding:utf-8 -*-
__author__    = "Nicolas Dumazet"
__copyright__ = "Copyright 2009, Nicolas Dumazet"
__license__   = "MIT"
__version__   = "0.1.0dev"
__email__     = "nicdumz@gmail.com"
__status__    = "Prototype"

import node, sys

if len(sys.argv) != 2:
    print """Usage:
    python testcli.py localport"""
    sys.exit(-1)

id = int(sys.argv[1])
serv = node.Node(id, id)
