from cache import DeferredCacheStorage, CacheStorage
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred
import logging


class TwoLevelCache(DeferredCacheStorage):
    """
    @type l1Cache: cache.CacheStorage
    """ 
    l1Cache = None
    """
    @type l2Cache: cache.DeferredCacheStorage
    """
    l2Cache = None
    
    def __init__(self, l1CacheStorage, l2DeferredCacheStorage):
        assert isinstance(l1CacheStorage, CacheStorage)
        assert isinstance(l2DeferredCacheStorage, DeferredCacheStorage)
        
        self.l1Cache = l1CacheStorage
        self.l2Cache = l2DeferredCacheStorage
            
    def search(self, key, headers=Headers()):
        logging.debug("Searching for item in L1 cache " + key)
        cacheObject = self.l1Cache.get(key, headers)
        if cacheObject is None:
            logging.debug("Searching for item in L2 cache: "+key)
            """ If not found in L1, search in L2 """ 
            return self.l2Cache.search(key, headers)
        else:
            logging.debug("Found in L1, responding")
            """ Else respond but wrap in deferred """
            d = Deferred()
            self.respond(d, success=True, result=cacheObject)
            return d

    def store(self, key, headers, value):
        logging.debug("Storing "+key+" in L1 & L2 caches")
        """ Stores in both, L1 and L2 cache """
        self.l1Cache.put(key, headers, value)
        self.l2Cache.store(key, headers, value)
