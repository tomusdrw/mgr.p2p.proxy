#!/usr/bin/python2

from main import initLogger
from simulator import Simulator
from twisted.python import log
import argparse
import csv



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

def readClients(clientsFilename = 'simulator/data/clients.txt'):
    clientsFile = open(clientsFilename, 'rb')
    clients = []
    line = clientsFile.readline().strip()
    while line:
        clients.append(line)
        line = clientsFile.readline().strip()
    return clients
    
def readClientsData():
    clientsDir = 'simulator/data/clients/'
    clients = readClients()
    
    clientsData = {}
    for c in clients:
        data = []
        with open(clientsDir + c, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                # Trim columns
                if row[0] != 'time':
                    data.append((float(row[0]), row[1]))
        clientsData[c] = data
        
    return clientsData
    

if __name__ == '__main__':
    args = parser().parse_args()
    
    initLogger(args.log)
    log.startLogging(open('logs/twisted.logs', 'w+'))
    
    simulator = Simulator(requests=readClientsData())
    simulator.start()


