'''
@author: tomusdrw
'''
from twisted.web import http
from proxy.Proxy import Proxy


class ProxyFactory(http.HTTPFactory):
    protocol = Proxy
    
    def __init__(self, cacheStorage, timeout=500):
        self.cacheStorage = cacheStorage
        http.HTTPFactory.__init__(self, timeout=timeout)
        
    def buildProtocol(self, addr):
        p = self.protocol(self.cacheStorage)
        p.factory = self
        p.timeOut = self.timeOut
        
        return p
