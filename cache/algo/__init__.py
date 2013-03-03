from cache import CacheStorage, ForwardingCacheStorage
from twisted.web.http_headers import Headers

class CacheLogic(ForwardingCacheStorage):
    pass        

class Fifo(CacheLogic):
    
    def __init__(self, baseStorage, queueSize=128):
        assert queueSize > 0
        self._queueSize = queueSize
        CacheLogic.__init__(self, baseStorage)
    
    def put(self, key, headers, value, metadata=None):
        items = self.items()
        if len(items) == self._queueSize:
            # Remove first element from items queue
            self.remove(items[0].key)
            
        CacheLogic.put(self, key, headers, value, metadata)
