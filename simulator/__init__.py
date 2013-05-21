from p2p.node import Node, DeferredNodeCache
from cache.test import StoreEverytingStorage
from cache.algo import LRU
from cache.multi import TwoLevelCache

class SimulatorNode(Node):
    
    def __init__(self, port=4000, cacheStorage=None):
        Node.__init__(self, port=port, cacheStorage=cacheStorage)





node = SimulatorNode(cacheStorage = StoreEverytingStorage())
#node.joinNetwork(knownNodeAddresses)

p2pCache = DeferredNodeCache(node)
memoryCache = LRU(StoreEverytingStorage(), queueSize=128)

multiCache = TwoLevelCache(memoryCache, p2pCache)


    