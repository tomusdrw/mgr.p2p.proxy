
from entangled.node import EntangledNode
from p2p import store

class Node(EntangledNode):
    def __init__(self, port=4000, cacheStorage=None):
        dataStore = store.CacheDataStore(cacheStorage)
        EntangledNode.__init__(self, udpPort=port, dataStore=dataStore)
