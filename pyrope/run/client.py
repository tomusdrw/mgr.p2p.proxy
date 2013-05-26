# -*- coding:utf-8 -*-
__author__    = "Nicolas Dumazet"
__copyright__ = "Copyright 2009, Nicolas Dumazet"
__license__   = "MIT"
__version__   = "0.1.0dev"
__email__     = "nicdumz@gmail.com"
__status__    = "Prototype"

import node, sys

if len(sys.argv) != 3:
    print """Usage:
    python testcli.py localport remoteport"""
    sys.exit(-1)

l = int(sys.argv[1])
remote = int(sys.argv[2])

cli = node.Node(l,l,('',remote))
