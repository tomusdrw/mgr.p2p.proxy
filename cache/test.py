from cache import CacheStorage, CacheObject
from twisted.internet import reactor
from twisted.internet.defer import Deferred
import StringIO
import gzip
import re

# pylint: disable=E1101

def respond(deferred, success=False, result=None):
    reactor.callLater(0, deferred.callback, {
        'success': success,
        'result': result
    })
    

class EmptyCacheStorage(CacheStorage):
    def get(self, key, headers=None):
        d = Deferred()
        respond(d)
        return d

    def store(self, key, value):
        pass

class ImageReplaceStorage(CacheStorage):
    
    def get(self, key, requestHeaders=None):
        d = Deferred()
        if not re.match(r'.+\.(png|jpg|jpeg|gif)$', key):        
            respond(d)
        else:
            f = open('foto_4.jpg', 'r')
            content = f.read()
            headers = {
              'content-type' : 'image/jpg'
            }
            accept = requestHeaders.getRawHeaders('accept-encoding', default=[])
            if len(accept) and re.match(r'gzip', accept[0]):
                # We can gzip content
                strObj = StringIO.StringIO()
                gzipFile = gzip.GzipFile(fileobj=strObj, mode='w')
                gzipFile.write(content)
                gzipFile.close()
                content = strObj.getvalue()
                headers['content-encoding'] = 'gzip'
                                            
            respond(d, success=True, result=CacheObject(content, headers))
            f.close()
        return d
        
    
