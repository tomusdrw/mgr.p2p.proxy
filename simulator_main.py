#!/usr/bin/python2

from main import initLogger
from simulator import Simulator
from twisted.python import log
import argparse



PROG_NAME = 'p2p.proxy.simulator'
PROG_VERSION = '0.0.1'


def parser():
    p = argparse.ArgumentParser(description='Run and test simulations of distributed caching proxy.')
    p.add_argument('--version',
        action='version',
        version=PROG_VERSION)
    p.add_argument('--log',
        help='Change logging mode',
        dest='log',
        default='info',
        choices=['info', 'debug', 'warn'])
    return p

if __name__ == '__main__':
    args = parser().parse_args()
    
    initLogger(args.log)
    log.startLogging(open('logs/twisted.logs', 'w+'))
    
    simulator = Simulator(requests={
        "Node1" : [
                     (1, "someAdress"),
                     (1, "someAdress2"),
                     (5, "someAdress2")
                  ],
        "Node2" : [
                     (4, "someAdress3"),
                     (5, "someAdress")
                 ],
        "Node3": [],
        "Node4": [],
        "Node5" : [
                     (0.5, "someAdress7"),
                     (1.5, "someAdress2"),
                     (5, "someAdress4")
                  ],
        "Node6" : [
                     (2, "someAdress3"),
                     (1, "someAdress")
                 ],
        "Node7": [],
        "Node8": []
    })
    simulator.start()


