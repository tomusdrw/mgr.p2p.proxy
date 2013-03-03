'''
@author: tomusdrw
'''
from proxy.ProxyClient import ProxyClientFactory
from proxy.TunnelProtocolFactory import TunnelProtocolFactory
from twisted.internet import reactor
from twisted.web import http
import logging
import urlparse


log = logging.getLogger(__name__)


class ProxyRequest(http.Request):
    # pylint: disable=E1103
    """
    Used by Proxy to implement a simple web proxy.

    @ivar reactor: the reactor used to create connections.
    @type reactor: object providing L{twisted.internet.interfaces.IReactorTCP}
    """

    protocols = {'http': ProxyClientFactory}
    ports = {'http': 80}

    def __init__(self, channel, queued, reactor2=reactor):
        http.Request.__init__(self, channel, queued)
        self.cacheStorage = channel.cacheStorage
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

    def requestWebObject(self):
        parsed = urlparse.urlparse(self.uri)
        protocol = parsed[0]
        host, port = self.extractHostAndPort(parsed, protocol)
        rest = self.extractQuery(parsed)

        class_ = self.protocols[protocol]

        headers = self.getAllHeaders().copy()

        if 'host' not in headers:
            headers['host'] = host

        log.info('Performing {} request for {}'.format(self.method, self.uri))
        self.content.seek(0, 0)
        s = self.content.read()
        clientFactory = class_(self.method, rest, self.clientproto, headers,
                               s, self)
        self.reactor.connectTCP(host, port, clientFactory)

    def returnWebObject(self, cacheObject):
        self.setResponseCode(200, "Returned from cache")
        cacheObject.applyHeaders(self.responseHeaders)
        self.write(cacheObject.content)
        self.finish()

    def processCacheResult(self, result):
        if result['success']:
            self.returnWebObject(result['result'])
        else:
            self.requestWebObject()

    def processHttp(self):
        if self.method == 'GET':
            cacheItem = self.cacheStorage.search(self.uri, self.requestHeaders)
            cacheItem.addCallback(self.processCacheResult)
        else:
            self.requestWebObject()

    def processConnect(self):
        try:
            host, portStr = self.uri.split(':', 1)
            port = int(portStr)
        except ValueError:
            self.setResponseCode(400)
            self.finish()
        else:
            self.reactor.connectTCP(host, port, TunnelProtocolFactory(self))
