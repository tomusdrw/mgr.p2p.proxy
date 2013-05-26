from p2p.node import Node, DeferredNodeCache
from cache.test import StoreEverytingStorage
from cache.algo import LRU,LFU
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
    p2pQueueSize = 128
    
    memAlgo = LRU
    p2pAlgo = LFU
    
    noMem = False
    
    def __init__(self):
        if self.noMem:
            logging.info("Settings: No memory, P2P {}({})".format(self.p2pAlgo.__name__, self.p2pQueueSize))
        else:
            logging.info("Settings: Mem: {}({}), P2P {}({})".format(self.memAlgo.__name__, self.memQueueSize, self.p2pAlgo.__name__, self.p2pQueueSize))
    
    def getKnownHosts(self):
        return [('localhost', self.port)]
    
    def createNodeStorage(self):
        return self.p2pAlgo(StoreEverytingStorage(), queueSize=self.p2pQueueSize)
    
    def createNode(self, nodeNo):
        return SimulatorNode(port=self.port + nodeNo, cacheStorage=self.createNodeStorage())
    
    def createClientCache(self, node):
        p2pCache = DeferredNodeCache(node)
        
        if self.noMem:
            return p2pCache
        else:
            memoryCache = self.memAlgo(StoreEverytingStorage(), queueSize=self.memQueueSize)
        
            return TwoLevelCache(memoryCache, p2pCache)
     
     
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
    
    
    def __init__(self, nodeId, nodeNo, resultsLogger, knownHosts, shutdownDelay = 5):
        self.nodeId = nodeId
        self.nodeNo = nodeNo
        self.resultsLogger = resultsLogger
        self.knownHosts = knownHosts
        self.shutdownDelay = shutdownDelay
        
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
    
        
    def __init__(self, requests, factory=None, resultsLogger=None):
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


    
