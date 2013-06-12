#!/usr/bin/python2

from simulator import Simulator, ResultsLogger
from twisted.python import log
from multiprocessing import Queue
import argparse
import csv
import logging
from multiprocessing.process import Process
from common import ArgsClientFactory, initLogger, initDefaultParserOptions



PROG_NAME = 'p2p.proxy.simulator'
PROG_VERSION = '0.0.1'


def parser():
    p = argparse.ArgumentParser(description='Run and test simulations of distributed caching proxy.')
    p.add_argument('--version',
        action='version',
        version=PROG_VERSION)

    initDefaultParserOptions(p, memSize=256, p2pSize=256)
    return p

def readClients(clientsFilename = 'simulator/data/clients.txt'):
    logging.info("Reading clients list from {}".format(clientsFilename))
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
    
    logging.info("Reading clients data from {}".format(clientsDir)) 
    clientsData = {}
    for c in clients:
        data = []
        logging.debug("Reading client {}".format(c))
        with open(clientsDir + c, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                # Trim columns
                if row[0] != 'time':
                    data.append((float(row[0]), row[1]))
        clientsData[c] = data
        
    logging.debug("Reading clients done")
    return clientsData
    

class FileResultsLogger(ResultsLogger):
    
    process = None
    queue = None
    logFileName = None
    
    def __init__(self, args):
        self.queue = Queue()
        if args.no_mem:
            fileName = '_'.join([args.p2p_net, 'no_mem', args.p2p_algo, str(args.p2p_size)])
        else:
            fileName = '_'.join([args.p2p_net, args.mem_algo, str(args.mem_size), args.p2p_algo, str(args.p2p_size)])
        self.logFileName = 'logs/' + fileName + '.logs'
    
    def logRequest(self, nodeId, address, latency, cacheLevel=-1):
        ResultsLogger.logRequest(self, nodeId, address, latency, cacheLevel=cacheLevel)
        self.queue.put("{}\t{}\t{}\t{}\n".format(nodeId, address, latency, cacheLevel))

    def finish(self):
        self.queue.put("STOP")
        self.process.join()
            
    def writerProcess(self):
        fileObject = open(self.logFileName, 'w+')
        for logEntry in iter(self.queue.get, "STOP"):
            fileObject.write(logEntry)
        fileObject.close()
        
    def start(self):
        self.process = Process(target=self.writerProcess)
        self.process.start()
      
if __name__ == '__main__':
    args = parser().parse_args()
    
    initLogger(args.log)
    log.startLogging(open('logs/twisted.logs', 'w+'))
    
    resultsLogger = FileResultsLogger(args)
    resultsLogger.start()
    factory = ArgsClientFactory(args)
    
    #"""
    simulator = Simulator(requests = readClientsData(), resultsLogger = resultsLogger, factory = factory)
    """
    simulator = Simulator(requests = {
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
    }, resultsLogger = resultsLogger, factory=factory)
    #"""
    logging.debug("Starting simulation.")
    simulator.start()
    # Write output to file
    logging.info("Waiting for logs to write to file")
    resultsLogger.finish()

