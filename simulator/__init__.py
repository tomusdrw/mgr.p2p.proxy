from p2p.node import Node, DeferredNodeCache
from cache.test import StoreEverytingStorage
from cache.algo import LRU
from cache.multi import TwoLevelCache
import sched
import time
import logging
from twisted.internet import reactor
from twisted.web.http_headers import Headers


class SimulatorNode(Node):
    
    port = None
    
    def __init__(self, port=4000, cacheStorage=None):
        self.port = port
        Node.__init__(self, port=port, cacheStorage=cacheStorage)
        
        
class SimulatorClient:
    
    node = None
    cacheStorage = None
    
    def __init__(self, node, cacheStorage):
        self.node = node
        self.cacheStorage = cacheStorage
    
        
class ClientFactory:
    
    def createNodeStorage(self):
        return StoreEverytingStorage()
    
    def createNode(self, nodeId):
        return SimulatorNode(port=4000 + nodeId, cacheStorage=self.createNodeStorage())
    
    def createClientCache(self, node):
        p2pCache = DeferredNodeCache(node)
        memoryCache = LRU(StoreEverytingStorage(), queueSize=128)
        
        return TwoLevelCache(memoryCache, p2pCache)
     
     
class ResultsLogger:
    
    def logRequest(self, nodeId, address, latency, cacheLevel=-1):   
        logging.info("Request: nodeId: {}, address: {}, latency: {}, cacheLevel: {}".format(nodeId, address, latency, cacheLevel))

class Simulator:
    """
    Dictionary with mapping nodeId -> SimulatorClient
    """
    clients = None
    resultsLogger = None
    
    def __init__(self, nodesId=["Node1"], factory=None, resultsLogger=None):
        if factory is None:
            factory = ClientFactory()
        if resultsLogger is None:
            self.resultsLogger = ResultsLogger()
        else:
            self.resultsLogger = resultsLogger
            
        self.clients = dict()
        for i in range(len(nodesId)):
            node = factory.createNode(i)
            cache = factory.createClientCache(node)
        
            self.clients[nodesId[i]] = SimulatorClient(node, cache)
        
    def makeRequest(self, nodeId, address):
        logging.debug("Making request by " + nodeId + " to " + address)
        client = self.clients[nodeId]
        
        startTime = time.time()
        
        def processResult(result):
            latency = time.time() - startTime
            success = result['success']
            cacheLevel = result['result'].level if success else -1
            # We have to store result if no cacheHit
            if cacheLevel == -1:
                client.cacheStorage.store(address, Headers(), 'a')
            self.resultsLogger.logRequest(nodeId, address, latency, cacheLevel)
            
        df = client.cacheStorage.search(address)
        df.addCallback(processResult)
        
    def start(self, requests):
        self.buildNetwork()
        
        #Bind makeRequest function
        def makeRequest(nodeId, address):
            self.makeRequest(nodeId, address)
            
        
        scheduler = sched.scheduler(time.time, time.sleep)
        
        for nodeId, delay, requestAddress in requests:
            #Since in same thread there are nodes running use callLater method
            reactor.callLater(delay, makeRequest, nodeId, requestAddress)
        
        logging.info("Starting scheduler. Waiting for events to complete.")
        scheduler.run()
        logging.info("All requests completed. Check log file for results.")
        
        
    def buildNetwork(self):
        knownHosts = [('localhost', self.clients.values()[0].node.port)]
        
        # First join network
        for client in self.clients.values():
            client.node.joinNetwork(knownHosts)


    
