from p2p.node import Node, DeferredNodeCache
from cache.test import StoreEverytingStorage
from cache.algo import LRU,LFU
from cache.multi import TwoLevelCache
import sched
import time
import logging
import random
from twisted.internet import reactor
from twisted.web.http_headers import Headers
from multiprocessing.process import Process
from multiprocessing import Queue
from common import ClientFactory

class ResultsLogger:
    
    def logRequest(self, nodeId, address, latency, cacheLevel= -1):   
        logging.info("Request: nodeId: {}, address: {}, latency: {}, cacheLevel: {}".format(nodeId, address, latency, cacheLevel))


class SimulatorClientProcess:
    shutdownDelay = None
    
    nodeId = None
    nodeNo = None
    resultsLogger = None
    
    node = None
    cache = None
    
    def __init__(self, port, nodeId, nodeNo, resultsLogger, knownHosts, shutdownDelay = 5):
        self.port = port
        self.nodeId = nodeId
        self.nodeNo = nodeNo
        self.resultsLogger = resultsLogger
        self.knownHosts = knownHosts
        self.shutdownDelay = shutdownDelay
        
    def startNode(self, factory, requests):
        # Everynode is waiting some time to make joining less stressful for machine running simualtor
        time.sleep(self.nodeNo + random.randint(1, 10))
        self.node = factory.createNode(self.port + self.nodeNo, self.knownHosts)
        self.cache = factory.createClientCache(self.node)
        
        logging.info("Starting node: {}".format(self.nodeId))
        
        # Take all elements from queue and put them to reactor queue
        self.scheduleRequests(requests)
        reactor.run()
        
    def scheduleRequests(self, requests):
         maxDelay = 0
         for delay, requestAddress in requests:
            if delay > maxDelay:
                maxDelay = delay
            reactor.callLater(delay, self.makeRequest, requestAddress)
         # Terminate after completion
         reactor.callLater(maxDelay + self.shutdownDelay, self.terminate)
         
    def terminate(self):
        # TODO terminate gently?
        logging.info("Node {} finished. Goodbye.".format(self.nodeId))
        self.node.terminate()
        reactor.stop()
 
    def makeRequest(self, address):
        logging.debug("Making request by {} to {}.".format(self.nodeId, address))
         
        startTime = time.time()
        
        def processResult(result):
            latency = time.time() - startTime
            success = result['success']
            cacheLevel = result['result'].level if success else -1
            # We have to store result if no cacheHit
            if cacheLevel == -1:
                self.cache.store(address, Headers(), '')
            self.resultsLogger.logRequest(self.nodeId, address, latency, cacheLevel)
            
        df = self.cache.search(address)
        df.addCallback(processResult)


class Simulator:
    """
    Dictionary with mapping nodeId -> SimulatorClient
    """
    clients = None
    
    initWait = 10
    
    def startNode(self, requests, nodesIds, idx, factory, resultsLogger, knownHosts):
        nodeName = nodesIds[idx]
        nodeRequests = requests[nodeName]
        client = SimulatorClientProcess(factory.port, nodeName, idx, resultsLogger, knownHosts)
        
        process = Process(target=client.startNode, args=(factory, nodeRequests))
            
        self.clients[nodeName] = process
        
    def __init__(self, requests, factory=None, resultsLogger=None):
        if factory is None:
            factory = ClientFactory()
        if resultsLogger is None:
            resultsLogger = ResultsLogger()
            
        knownHosts = [('localhost', factory.port)]
        nodesIds = requests.keys()
        
        self.clients = dict()
        logging.debug("Spawning client nodes.")
        # Spawn first node first
        self.startNode(requests, nodesIds, 0, factory, resultsLogger, [])
        time.sleep(self.initWait / 2)
        logging.info("Spawning nodes")
        for i in range(1, len(nodesIds)):
            self.startNode(requests, nodesIds, i, factory, resultsLogger, knownHosts)
        # Wait until everynode is ready
        time.sleep(self.initWait)
        logging.debug("Spawning done.")
        
    def start(self):
        # Start all processes
        for client in self.clients.values():
            client.start()
        try:
            # Normally just wait for clients to join
            for client in self.clients.values():
                client.join() 
        except:
            # But in case of exception terminate all
            for nodeName, client in self.clients.items():
                logging.info('Killing node {}'.format(nodeName))
                client.terminate()
                client.join()
        logging.info("Simulation finished. Hope you enjoyed.")


    
