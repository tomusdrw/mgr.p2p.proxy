from twisted.web.http_headers import Headers
from twisted.internet import reactor
from twisted.internet.defer import Deferred
        
class DeferredCacheStorage(object):
    def respond(self, deferred, success=False, result=None):
        # pylint: disable=E1101
        reactor.callLater(0, deferred.callback, {
            'success': success,
            'result': result
        })
    def search(self, key, headers=Headers()):
        """
        Search for an item in cache
        returns {twisted.internet.defer.Deferred} instance
        """
    def store(self, key, headers, value):
        """
        Store item in cache.
        """

class CacheStorage(object):
    """ Storage for local cache """
    def get(self, key, headers=Headers()):
        """ 
        Retrieve item from cache
        returns a {CacheObject} instance
        """
        
    def items(self):
        """
        Get all {CacheObject} instances that are handled by this storage
        returns an array of {CacheObject}
        """ 
    
    def remove(self, key):
        """
        Remove item with key {key} from storage.
        Do nothing if {key} does not exist.
        """
    
    def put(self, key, headers, value, metadata=None):
        """
        Store {value} to this storage under {key} 
        Additionaly provide response headers and metadata for {CacheObject}.
        """
        
class ForwardingCacheStorage(CacheStorage):
    """ {CacheStorage} that forwards all calls to delegate. """
    delegate = None
    
    def __init__(self, delegate):
        self.delegate = delegate
        CacheStorage.__init__(self)
        
    def get(self, key, headers=Headers()):
        return self.delegate.get(key, headers=headers)
    
    def items(self):
        return self.delegate.items()
        
    def remove(self, key):
        return self.delegate.remove(key)
        
    def put(self, key, headers, value, metadata=None):
        return self.delegate.put(key, headers, value, metadata)
    
class DeferredDecorator(ForwardingCacheStorage, DeferredCacheStorage):
    """ This decorator turns normal CacheStorage into {DeferredCacheStorage} """
    
    def store(self, key, headers, value):
        return ForwardingCacheStorage.put(self, key, headers, value)
    
    def search(self, key, headers=Headers()):
        cacheObject = ForwardingCacheStorage.get(self, key, headers=headers)
        d = Deferred()
        
        if cacheObject:
            self.respond(d, success=True, result=cacheObject)
        else:
            self.respond(d)
            
        return d
            

class CacheObject:
    key = None
    headers = None
    _content = None
    hits = 0
    metadata = None

    def __init__(self, key, content, headers=None, metadata=None):
        self.key = key
        self.content = content
        self.headers = headers or {}
        self.metadata = metadata
        
    def applyHeaders(self, headerObject):
        for key, value in self.headers.items():
            headerObject.setRawHeaders(key, value)
    @property
    def content(self):
        return self._content
    def hit(self):
        self.hits += 1
        
    def destroy(self):
        """ Can be used to clear allocated objects etc """
