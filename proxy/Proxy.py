'''
@author: tomusdrw
'''
from twisted.web import http
from proxy.ProxyRequest import ProxyRequest

class Proxy(http.HTTPChannel):
    #pylint: disable=E0202
    requestFactory = ProxyRequest
    
    def __init__(self, cacheStorage):
        self.tunnel = None
        self.cacheStorage = cacheStorage
        http.HTTPChannel.__init__(self)
        
    def registerTunnel(self, tunnel):
        self.tunnel = tunnel
    
    def dataReceived(self, data):
        if self.tunnel is not None:
            self.tunnel.transport.write(data)
        else:
            return http.HTTPChannel.dataReceived(self, data)
    