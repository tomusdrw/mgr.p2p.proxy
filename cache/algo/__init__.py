from cache import CacheStorage, ForwardingCacheStorage
from twisted.web.http_headers import Headers

class CacheLogic(ForwardingCacheStorage):
    pass 

class MarkingCache(CacheLogic):
    def __init__(self, baseStorage, queueSize=128):
        assert queueSize > 0
        self._queueSize = queueSize
        CacheLogic.__init__(self, baseStorage)
    
    def put(self, key, headers, value, metadata=None):
        items = self.items()
        if len(items) == self._queueSize:
            self.removeElement(items)
            
        CacheLogic.put(self, key, headers, value, metadata)
    
    #Removes element to make place for new one
    def removeElement(self):
        pass
           

class Fifo(MarkingCache):
    def removeElement(self, items):
        # Remove first element from items queue
        self.remove(items[0].key)
    
        
class LRU(MarkingCache):
    def removeElement(self, items):
        # Find Least Recently Used
        v = min(items, key=lambda x: x.lastUsed)
        self.remove(v.key)
        
class LFU(MarkingCache):
    def removeElement(self, items):
        #Find element with smallest number of hits
        v = min(items, key=lambda x: x.hits)
        self.remove(v.key)
