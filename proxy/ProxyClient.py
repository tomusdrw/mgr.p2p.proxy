from twisted.web.proxy import ProxyClient as TwistedProxyClient, \
    ProxyClientFactory as TwistedProxyClientFactory
import cStringIO
import logging

class ProxyClient(TwistedProxyClient):
    isCached = False
    responseContent = None
    
    def cachableCode(self, code):
        intCode = int(code)
        # TODO partial content (206) cacheable? Some youtube optimizations for keys required.
        return intCode == 200
    
    def sendCommand(self, command, path):
        TwistedProxyClient.sendCommand(self, command, path)
        self.isCached = command == 'GET'
        
    
    def handleStatus(self, version, code, message):
        TwistedProxyClient.handleStatus(self, version, code, message)
        logging.info('Response for {}: {}'.format(self.father.uri, code))
        self.isCached = self.isCached and self.cachableCode(code)
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
