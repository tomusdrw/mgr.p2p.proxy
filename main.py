#!/usr/bin/python2
'''
@author: tomusdrw
'''
from proxy import ProxyFactory
from twisted.internet import reactor
from twisted.python import log
import logging
import sys


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    log.startLogging(open('logs/twisted.logs', 'a+'))
    
    reactor.listenTCP(8080, ProxyFactory.ProxyFactory())
    reactor.run()
