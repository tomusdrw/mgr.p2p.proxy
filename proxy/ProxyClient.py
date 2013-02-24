from twisted.web.proxy import ProxyClient as TwistedProxyClient, \
    ProxyClientFactory as TwistedProxyClientFactory
import cStringIO
import logging

class ProxyClient(TwistedProxyClient):
    isCached = False
    responseContent = None
    
    def handleStatus(self, version, code, message):
        TwistedProxyClient.handleStatus(self, version, code, message)
        self.isCached = int(code) == 200
        self.responseContent = cStringIO.StringIO()
    
    def handleResponsePart(self, bufferData):
        TwistedProxyClient.handleResponsePart(self, bufferData)
        if self.isCached:
            self.responseContent.write(bufferData)
            
    def handleResponseEnd(self):
        if self.isCached and not self._finished:
            father = self.father
            content = self.responseContent.getvalue()
            self.responseContent.close()
            father.cacheStorage.store(father.uri, father.responseHeaders, content)
        TwistedProxyClient.handleResponseEnd(self)
            

class ProxyClientFactory(TwistedProxyClientFactory):
    protocol = ProxyClient
