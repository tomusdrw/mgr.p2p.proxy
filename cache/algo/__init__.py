from cache import CacheStorage
from twisted.web.http_headers import Headers

class CacheLogic(CacheStorage):
    baseStorage = None
    
    def __init__(self, baseStorage):
        self.baseStorage = baseStorage
        CacheStorage.__init__(self)
        
    def get(self, key, headers=Headers()):
        return self.baseStorage.get(key, headers=headers)
    
    def items(self):
        """
        returns an array
        """
        return self.baseStorage.items()
        
    def remove(self, key):
        return self.baseStorage.remove(key)
        
    def store(self, key, headers, value):
        return self.baseStorage.store(key, headers, value)
        

class Fifo(CacheLogic):
    
    def __init__(self, baseStorage, queueSize=128):
        assert queueSize > 0
        self._queueSize = queueSize
        CacheLogic.__init__(self, baseStorage)
    
    def store(self, key, headers, value):
        items = self.items()
        if len(items) == self._queueSize:
            # Remove first element from items queue
            self.remove(items[0].key)
            
        CacheLogic.store(self, key, headers, value)
