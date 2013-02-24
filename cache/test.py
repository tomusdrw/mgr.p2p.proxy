from twisted.internet.defer import Deferred
from cache import CacheStorage
from twisted.internet import reactor

class EmptyCacheStorage(CacheStorage):
    def get(self, key):
        d = Deferred()
        reactor.callLater(0, d.callback, {
            'success': False, 
            'result': None
        })
        return d

    def store(self, key, value):
        pass

