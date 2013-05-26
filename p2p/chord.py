from pyrope.node import Node as PyRopeNode
import logging
from twisted.web.http_headers import Headers
from cache import DeferredCacheStorage, CacheObject
from twisted.internet.defer import Deferred
import random
import hashlib
from multiprocessing.process import Process
from pyrope.network import ChordJsonRpc, ServerProxy
from pyrope import jsonrpc

NETWORK_SIZE = 2**16

class BlockingChordNode(PyRopeNode):
    
    cacheStorage = None
    
    def __init__(self, nodeId, knownHosts, port=4000, cacheStorage=None):
        self.cacheStorage = cacheStorage
        if len(knownHosts) > 0:
            host = knownHosts[0]
        else:
            host = None
            
        PyRopeNode.__init__(self, nodeId, port, host)
    
    def findValue(self, key):
        nodeId, address = self.find_successor(key)
        node = self._getNode(nodeId)
        return node.get(key)
    
    def storeValue(self, key, value):
        nodeId, address = self.find_successor(key)
        node = self._getNode(nodeId)
        node.store(key, value)
    
    def get(self, key):
        cacheObject = self.cacheStorage.get(key)
        if cacheObject is None:
            return None
        else: 
            return (key, cacheObject.content)
    
    def store(self, key, value):
        self.cacheStorage.put(key, Headers(), value)

class ChordNode:
    
    process = None
    node = None
    
    def createNode(self, nodeId, port, cacheStorage, knownHosts):
        BlockingChordNode(nodeId, knownHosts, port, cacheStorage)
    
    def __init__(self, knownHosts, port=4000, cacheStorage=None):
        # TODO id?
        nodeId = random.randrange(NETWORK_SIZE)
        
        self.process = Process(target=self.createNode, args=(nodeId, port, cacheStorage, knownHosts))
        self.process.start()
        self.node = ServerProxy(('', port), nodeId, ('localhost', port))
    
        
        
class DeferredChordNodeCache(DeferredCacheStorage):
    class NodeCacheObject(CacheObject):
        level = 2
    
    node = None
    
    def __init__(self, node):
        """
        @param node: {ChordNode}
        """
        self.node = node
        
    def hash(self, key):
        # pylint: disable=E1101
        h = hashlib.sha1()
        h.update(key)
        return int(h.hexdigest(), base=16) % NETWORK_SIZE
    
    def cacheObject(self, key, result):
        value = result[1].decode('base64').decode('zlib')
        return self.NodeCacheObject(key, value)
    
    def search(self, key, headers=Headers()):
        keyHash = self.hash(key)
        d = Deferred()
        logging.debug('Searching for ' + key)
        
        def checkResult(result):
            if result is not None:
                self.respond(d, success=True, result=self.cacheObject(key, result))
            else:
                self.respond(d)
        
        # Try to find value         
        value = self.node.findValue(keyHash)
        checkResult(value)
        return d
        
    def store(self, key, headers, value):
        keyHash = self.hash(key)
        logging.debug('Storing ' + key + ' in network')
        encodedValue = value.encode('zlib').encode('base64')
        print "Compression: original: {}, encoded: {}".format(len(value), len(encodedValue))
        self.node.storeValue(keyHash, encodedValue)
