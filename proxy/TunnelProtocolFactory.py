'''
@author: tomusdrw
'''
from twisted.internet.protocol import ClientFactory
from proxy.TunnelProtocol import TunnelProtocol

class TunnelProtocolFactory(ClientFactory):
    protocol = TunnelProtocol
    
    def __init__(self, request):
        self.request = request
        
    def buildProtocol(self, addr):
        return self.protocol(self.request)
    
    def clientConnectionFailed(self, connector, reason):
        self.request.SetResponseCode(501, 'Gateway error')
        self.request.finish()