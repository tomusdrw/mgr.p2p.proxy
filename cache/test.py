from cache import CacheStorage, CacheObject
from twisted.web.http_headers import Headers
import StringIO
import gzip
import re
import logging

class EmptyCacheStorage(CacheStorage):
    def get(self, key, headers=Headers()):
        return None

class ImageReplaceStorage(CacheStorage):
    def get(self, key, requestHeaders=Headers()):
        if not re.match(r'.+\.(png|jpg|jpeg|gif)$', key):
            return None        
        f = open('foto_4.jpg', 'r')
        content = f.read()
        f.close()
        
        headers = {
          'content-type' : ['image/jpg']
        }
        accept = requestHeaders.getRawHeaders('accept-encoding', default=[])
        if len(accept) and re.match(r'gzip', accept[0]):
            # We can gzip content
            strObj = StringIO.StringIO()
            gzipFile = gzip.GzipFile(fileobj=strObj, mode='w')
            gzipFile.write(content)
            gzipFile.close()
            content = strObj.getvalue()
            strObj.close()
            headers['content-encoding'] = ['gzip']
                                        
        return CacheObject(key, content, headers)
    
class StoreEverytingStorage(CacheStorage):
    class MyCacheObject(CacheObject):
        pass
        
    _storage = None
    _items = None
    
    def __init__(self):
        self._storage = {}
        self._items = []
        CacheStorage.__init__(self)
    
    def items(self):
        return self._items
    
    def remove(self, key):
        if key in self._storage:
            val = self._storage[key]
            # Remove from dictionary
            del self._storage[key]
            # Remove from order table
            self._items.remove(val)
            # Notify item about removal
            val.destroy()
    
    def get(self, key, headers=Headers()):
        if key in self._storage:
            # TODO: 304 responses?
            logging.info('Cache hit for ' + key)
            cacheObject = self._storage[key]
            cacheObject.hit()
            return cacheObject
        return None
        
    def put(self, key, headers, value, metadata=None):
        # First remove any previous element
        self.remove(key)
        logging.info('Storing to cache: ' + key)
        headersDict = dict(headers.getAllRawHeaders())
        cacheObject = self.MyCacheObject(key, value, headersDict, metadata)
        
        self._storage[key] = cacheObject
        self._items.append(cacheObject)
    
        
    
