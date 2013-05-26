
from entangled import kademlia
from p2p import store
from cache import DeferredCacheStorage, CacheObject
from twisted.web.http_headers import Headers
import hashlib
from twisted.internet.defer import Deferred
import logging

class Node(kademlia.node.Node):
    def __init__(self, port=4000, cacheStorage=None):
        dataStore = store.CacheDataStore(cacheStorage)
        kademlia.node.Node.__init__(self, udpPort=port, dataStore=dataStore)

class DeferredNodeCache(DeferredCacheStorage):
    class NodeCacheObject(CacheObject):
        level = 2
    
    node = None
    
    def __init__(self, node):
        """
        @param node: {Node}
        """
        self.node = node
    def hash(self, key):
        # pylint: disable=E1101
        h = hashlib.sha1()
        h.update(key)
        return h.hexdigest()
    
    def cacheObject(self, key, result):
        headers, value = store.deserialize(result)
        return self.NodeCacheObject(key, value, headers)
    
    def search(self, key, headers=Headers()):
        keyHash = self.hash(key)
        d = Deferred()
        logging.debug('Searching for ' + key)
        
        def checkResult(result):
            if type(result) == dict:
                self.respond(d, success=True, result=self.cacheObject(key, result[keyHash]))
            else:
                self.respond(d)
        
        # Try to find value         
        df = self.node.iterativeFindValue(keyHash)
        df.addCallback(checkResult)
        return d
        
    def store(self, key, headers, value):
        keyHash = self.hash(key)
        logging.debug('Storing ' + key + ' in network')
        serialized = store.serialize(dict(headers.getAllRawHeaders()), value)
        self.node.iterativeStore(keyHash, serialized)
