#!/usr/bin/python2

from proxy.ProxyFactory import ProxyFactory
from twisted.internet import reactor
from twisted.python import log
import argparse
import logging
import sys
from cache.test import ImageReplaceStorage

PROG_NAME = 'p2p.proxy'
PROG_VERSION = '0.0.1'


def parser():
    p = argparse.ArgumentParser(description='Run and test distributed caching proxy.')
    p.add_argument('--version',
        action='version',
        version=PROG_VERSION)
    p.add_argument('--log',
        help='Change logging mode',
        dest='log',
        default='info',
        choices=['info', 'debug', 'warn'])
    p.add_argument('-P',
        metavar='port',
        dest='proxy_port',
        type=int,
        default=8080,
        action='store',
        help='Proxy port')
    p.add_argument('--no-proxy',
        dest='no_proxy',
        action='store_true',
        help='Create only p2p node without proxy.')
    p.add_argument('--spawn',
        metavar='N',
        dest='spawn',
        type=int,
        action='store',
        help='Spawn some nodes that will be in p2p network')
    return p
def initLogger(logLevel):
    levels = {
     'info' : logging.INFO,
     'debug' : logging.DEBUG,
     'warn' : logging.WARN
    }
    logging.basicConfig(stream=sys.stdout, level=levels[logLevel])


if __name__ == '__main__':
    args = parser().parse_args()
    
    initLogger(args.log)
    log.startLogging(open('logs/twisted.logs', 'w+'))
    
    logging.info("Starting proxy at :{}".format(args.proxy_port))
    
    #pylint: disable=E1101
    reactor.listenTCP(args.proxy_port, ProxyFactory(ImageReplaceStorage()))
    
    logging.info('Running reactor.')
    reactor.run()
