from cache import CacheStorage
from entangled.kademlia import datastore
from twisted.web.http_headers import Headers

def serialize(headers, value):
    return {
      'headers': headers,
      'value': value
    }
    
def deserialize(serializedValue):
    # TODO Something is wrong when running simulations value is not always present.
    value = serializedValue['value'] if 'value' in serializedValue else None
    return serializedValue['headers'], value

class CacheDataStore(datastore.DataStore):
    class Metadata:
        lastPublished = None
        originallyPublished = None
        originalPublisherID = None
        def __init__(self, lastPublished, originallyPublished, originalPublisherID):
            self.lastPublished = lastPublished
            self.originallyPublished = originallyPublished
            self.originalPublisherID = originalPublisherID
    
    storage = None
    
    def __init__(self, cacheStorage):
        """
        @var cacheStorage: cache.CacheStorage
        """         
        assert isinstance(cacheStorage, CacheStorage)
        
        self.storage = cacheStorage

    def keys(self):
        """ Return a list of the keys in this data store """
        return [item.key for item in self.storage.items()]
    
    def lastPublished(self, key):
        return self.storage.get(key).metadata.lastPublished

    def originalPublisherID(self, key):
        """ Get the original publisher of the data's node ID
        
        @param key: The key that identifies the stored data
        @type key: str
        
        @return: Return the node ID of the original publisher of the
        C{(key, value)} pair identified by C{key}.
        """
        return self.storage.get(key).metadata.originalPublisherID

    def originalPublishTime(self, key):
        """ Get the time the C{(key, value)} pair identified by C{key}
        was originally published """
        return self.storage.get(key).metadata.originallyPublished

    def setItem(self, key, serializedValue, lastPublished, originallyPublished, originalPublisherID):
        """ I assume that received value will be json encoded string """
        headers, value = deserialize(serializedValue)
        metadata = self.Metadata(lastPublished, originallyPublished, originalPublisherID)
        
        return self.storage.put(key, Headers(headers), value, metadata)
        

    def __getitem__(self, key):
        item = self.storage.get(key)
        if item:
            return serialize(item.headers, item.content)
        raise KeyError()

    def __delitem__(self, key):
        return self.storage.remove(key)
