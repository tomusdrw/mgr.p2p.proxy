'''
@author: tomusdrw
'''
from twisted.web import proxy
from proxy.TunnelProtocolFactory import TunnelProtocolFactory

class ProxyRequest(proxy.ProxyRequest):
    def process(self):
        """ Support https proxying """
        if self.method == 'CONNECT':
            self.processConnect()
        else:
            print "Address: " + self.uri
            return proxy.ProxyRequest.process(self)
    def processConnect(self):
        try:
            host, portStr = self.uri.split(':', 1)
            port = int(portStr)
        except ValueError:
            self.setResponseCode(400)
            self.finish()
        else:
            self.reactor.connectTCP(host, port, TunnelProtocolFactory(self))