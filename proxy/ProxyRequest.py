'''
@author: tomusdrw
'''
from proxy.TunnelProtocolFactory import TunnelProtocolFactory
from twisted.web import http
from twisted.internet import reactor
from twisted.web.proxy import ProxyClientFactory
import urlparse
import re
import logging


log = logging.getLogger(__name__)
class ProxyRequest(http.Request):
    """
    Used by Proxy to implement a simple web proxy.

    @ivar reactor: the reactor used to create connections.
    @type reactor: object providing L{twisted.internet.interfaces.IReactorTCP}
    """

    protocols = {'http': ProxyClientFactory}
    ports = {'http': 80}

    def __init__(self, channel, queued, reactor2=reactor):
        http.Request.__init__(self, channel, queued)
        self.reactor = reactor2
        
    def process(self):
        """ Support https proxying """
        if self.method == 'CONNECT':
            self.processConnect()
        else:
            print "Address: " + self.uri
            self.processHttp()


    def extractHostAndPort(self, parsed, protocol):
        host = parsed[1]
        port = self.ports[protocol]
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        return host, port


    def extractQuery(self, parsed):
        rest = urlparse.urlunparse(('', '') + parsed[2:])
        if not rest:
            rest = rest + '/'
        return rest


    def replyWithImageFromDisk(self):
        f = open('foto_4.jpg', 'r')
        imgContent = f.read()
        f.close()
        self.setResponseCode(200, "Found file on disk")
        self.responseHeaders.addRawHeader("content-type", "image/jpeg")
        self.write(imgContent)
        self.finish()
    
    
    def processHttp(self):
        parsed = urlparse.urlparse(self.uri)
        protocol = parsed[0]
        host, port = self.extractHostAndPort(parsed, protocol)
        rest = self.extractQuery(parsed)
        
        class_ = self.protocols[protocol]
        headers = self.getAllHeaders().copy()
        
        if 'host' not in headers:
            headers['host'] = host
            
        if re.match(r'.+\.png$', rest):
            self.replyWithImageFromDisk()
            log.warning('Replying with image from disk')
        else:
            log.info('Performing request for ' + self.uri)
            self.content.seek(0, 0)
            s = self.content.read()
            clientFactory = class_(self.method, rest, self.clientproto, headers,
                                   s, self)
            self.reactor.connectTCP(host, port, clientFactory)

    def processConnect(self):
        try:
            host, portStr = self.uri.split(':', 1)
            port = int(portStr)
        except ValueError:
            self.setResponseCode(400)
            self.finish()
        else:
            self.reactor.connectTCP(host, port, TunnelProtocolFactory(self))
