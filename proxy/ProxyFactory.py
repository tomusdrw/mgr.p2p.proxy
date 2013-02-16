'''
@author: tomusdrw
'''
from twisted.web import http
from proxy.Proxy import Proxy


class ProxyFactory(http.HTTPFactory):
    protocol = Proxy