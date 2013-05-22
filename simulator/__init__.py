from p2p.node import Node, DeferredNodeCache
from cache.test import StoreEverytingStorage
from cache.algo import LRU
from cache.multi import TwoLevelCache
import sched
import time
import logging
from twisted.internet import reactor
from twisted.web.http_headers import Headers
from multiprocessing.process import Process
from multiprocessing import Queue


class SimulatorNode(Node):
    
    port = None
    
    def __init__(self, port=4000, cacheStorage=None):
        self.port = port
        Node.__init__(self, port=port, cacheStorage=cacheStorage)
        
        
class ClientFactory:
    
    port = 4000
    memQueueSize = 128
    
    def getKnownHosts(self):
        return [('localhost', self.port)]
    
    def createNodeStorage(self):
        return StoreEverytingStorage()
    
    def createNode(self, nodeNo):
        return SimulatorNode(port=self.port + nodeNo, cacheStorage=self.createNodeStorage())
    
    def createClientCache(self, node):
        p2pCache = DeferredNodeCache(node)
        memoryCache = LRU(StoreEverytingStorage(), queueSize=self.memQueueSize)
        
        return TwoLevelCache(memoryCache, p2pCache)
     
     
class ResultsLogger:
    
    def logRequest(self, nodeId, address, latency, cacheLevel= -1):   
        logging.info("Request: nodeId: {}, address: {}, latency: {}, cacheLevel: {}".format(nodeId, address, latency, cacheLevel))


class SimulatorClientProcess:
    
    nodeId = None
    nodeNo = None
    resultsLogger = None
    
    node = None
    cache = None
    
    def __init__(self, nodeId, nodeNo, resultsLogger, knownHosts):
        self.nodeId = nodeId
        self.nodeNo = nodeNo
        self.resultsLogger = resultsLogger
        self.knownHosts = knownHosts
        
    def joinNetwork(self):
        self.node.joinNetwork(self.knownHosts)
        
     
    def startNode(self, factory, requests):
        self.node = factory.createNode(self.nodeNo)
        self.cache = factory.createClientCache(self.node)
        
        logging.info("Starting node: {}".format(self.nodeId))
        
        # Take all elements from queue and put them to reactor queue
        self.scheduleRequests(requests)
        self.joinNetwork()
        reactor.run()
        
    def scheduleRequests(self, requests):
         for delay, requestAddress in requests:
            reactor.callLater(delay, self.makeRequest, requestAddress)
   
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
    
        
    def __init__(self, requests=None, factory=None, resultsLogger=None):
        if requests is None:
            requests = {
                    "Node1" : [
                        (1, "someAddress"),
                        (3, "someAddress2")
                        (5, "someAddress"),
                    ],
                    "Node2" : [
                        (1, "someAddress2")
                        (2, "someAddress")
                    ]
                }
        if factory is None:
            factory = ClientFactory()
        if resultsLogger is None:
            resultsLogger = ResultsLogger()
            
        knownHosts = factory.getKnownHosts() 
        nodesIds = requests.keys()
        
        self.clients = dict()
        for i in range(len(nodesIds)):
            nodeName = nodesIds[i]
            nodeRequests = requests[nodeName]
            client = SimulatorClientProcess(nodeName, i, resultsLogger, knownHosts)
            
            process = Process(target=client.startNode, args=(factory, nodeRequests))
            
            self.clients[nodeName] = process
        
    def start(self, maxTime=10):
        # Start all processes
        for client in self.clients.values():
            client.start()
        # # TODO when to finish?
        try:
            time.sleep(maxTime)
        finally:
            for nodeName, client in self.clients.items():
                logging.info('Killing node {}'.format(nodeName))
                client.terminate()
                client.join()


    
