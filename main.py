#!/usr/bin/python2
'''
@author: tomusdrw
'''
from proxy import ProxyFactory
from twisted.internet import reactor
from twisted.python import log
import sys


if __name__ == '__main__':
    log.startLogging(open('logs/twisted.logs', 'a+'))
    
    reactor.listenTCP(8080, ProxyFactory.ProxyFactory())
    reactor.run()
