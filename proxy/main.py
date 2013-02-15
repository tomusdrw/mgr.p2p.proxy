'''
@author: tomusdrw
'''
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.python import log
from twisted.web import proxy, http
import sys

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
            
class TunnelProtocol(Protocol):
    def __init__(self, request):
        self.request = request
        self.channel = request.channel
        self.peerTransport = request.channel.transport
        
    def connectionMade(self):
        self.channel.registerTunnel(self)
        self.request.setResponseCode(200, 'Connection estabilished')
        # Write nothing to trigger sending the response headers, but do 
        # not call finish, which may close the connection:
        self.request.write('')
    def dataReceived(self, data):
        self.peerTransport.write(data)

            
class TunnelProtocolFactory(ClientFactory):
    protocol = TunnelProtocol
    
    def __init__(self, request):
        self.request = request
        
    def buildProtocol(self, addr):
        return self.protocol(self.request)
    
    def clientConnectionFailed(self, connector, reason):
        self.request.SetResponseCode(501, 'Gateway error')
        self.request.finish()
                   
class Proxy(http.HTTPChannel):
    requestFactory = ProxyRequest
    
    def __init__(self):
        self.tunnel = None
        http.HTTPChannel.__init__(self)
        
    def registerTunnel(self, tunnel):
        self.tunnel = tunnel
    
    def dataReceived(self, data):
        if self.tunnel is not None:
            self.tunnel.transport.write(data)
        else:
            return http.HTTPChannel.dataReceived(self, data)
    
class ProxyFactory(http.HTTPFactory):
    protocol = Proxy

if __name__ == '__main__':
    log.startLogging(open('logs/twisted.logs', 'a+'))
    
    reactor.listenTCP(8080, ProxyFactory())
    reactor.run()
