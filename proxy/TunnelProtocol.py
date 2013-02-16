'''
@author: tomusdrw
'''
from twisted.internet.protocol import Protocol

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
