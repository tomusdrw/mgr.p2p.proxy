#!/usr/bin/python2

from proxy.ProxyFactory import ProxyFactory
from twisted.internet import reactor
import argparse
import logging
from multiprocessing.process import Process
import time
from common import initLogger, ArgsClientFactory, initDefaultParserOptions

PROG_NAME = 'p2p.proxy'
PROG_VERSION = '0.0.1'


def parser():
    p = argparse.ArgumentParser(description='Run and test distributed caching proxy.')
    p.add_argument('--version',
        action='version',
        version=PROG_VERSION)
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
        help='Spawn some nodes that will be in P2P network')
 
    p.add_argument('--bootstrap',
        metavar='HOST:PORT',
        dest='bootstrap',
        type=str,
        action='store',
        help='Provide known bootstrap node for P2P network.')
    p.add_argument('--known-nodes',
        metavar='filename',
        dest='known_nodes',
        type=argparse.FileType('r'),
        action='store',
        help='Provide filename with known nodes in P2P network.')
    
    initDefaultParserOptions(p)
    return p


def getKnownNodes(args):
    knownNodes = []
    if args.bootstrap:
        host, port = args.bootstrap.split(':')
        knownNodes.append((host, int(port)))
    if args.known_nodes:
        line = args.known_nodes.readLine()
        while line:
            host, port = line.split()
            knownNodes.append((host, int(port)))
            line = args.known_nodes.readLine()
    return knownNodes


def startNode(id2, factory, port, knownNodes=None):
    logging.info('Starting p2p node {}'.format(id2))
    node = factory.createNode(port, knownNodes)
    return node
        

if __name__ == '__main__':
    args = parser().parse_args()
    
    initLogger(args.log)
    #log.startLogging(open('logs/twisted.logs', 'w+'))
    factory = ArgsClientFactory(args)
    
    if args.spawn:
        nodes = []
        logging.info('Spawning {} processes'.format(args.spawn))
        startNode('Main node', factory, args.p2p_port, getKnownNodes(args))
        for i in range(1, args.spawn):
            process = Process(target=startNode, args=('Node {}'.format(i), factory, args.p2p_port + i, [('localhost', args.p2p_port)]))
            process.start()
            nodes.append(process)
        
        try:
            while 1:
                time.sleep(1)
        finally:
            for n in nodes:
                logging.info('Killing node {}'.format(n))
                n.terminate()
                n.join()
    else:
        node = startNode('P2P node', factory, args.p2p_port, getKnownNodes(args))
        
        # pylint: disable=E1101
        if not args.no_proxy:
            logging.info("Starting proxy at :{}".format(args.proxy_port))
            
            clientCache = factory.createClientCache(node)
            reactor.listenTCP(args.proxy_port, ProxyFactory(clientCache))
            

        logging.info('Running reactor.')
        reactor.run()
