#!/usr/bin/python2

from main import initLogger
from simulator import Simulator, ResultsLogger
from twisted.python import log
from multiprocessing import Queue
import argparse
import csv
import logging
from multiprocessing.process import Process



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
    

class FileResultsLogger(ResultsLogger):
    
    process = None
    queue = None
    logFileName = None
    
    def __init__(self, logFileName):
        self.queue = Queue()
        self.logFileName = logFileName
    
    def logRequest(self, nodeId, address, latency, cacheLevel=-1):
        ResultsLogger.logRequest(self, nodeId, address, latency, cacheLevel=cacheLevel)
        self.queue.put("{};{};{};{}\n".format(nodeId, address, latency, cacheLevel))

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
    
    logFile = 'logs/simulator.logs'
    
    resultsLogger = FileResultsLogger(logFile)
    resultsLogger.start()
    #simulator = Simulator(requests=readClientsData())
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
    }, resultsLogger = resultsLogger)
    simulator.start()
    # Write output to file
    logging.info("Waiting for logs to write to file")
    resultsLogger.finish()

