# -*- coding:utf-8 -*-
import logging
__author__    = "Nicolas Dumazet"
__copyright__ = "Copyright 2009, Nicolas Dumazet"
__license__   = "MIT"
__version__   = "0.1.0dev"
__email__     = "nicdumz@gmail.com"
__status__    = "Prototype"
import jsonrpc
import routing

MSG_LIMIT = 2**30

class ChordJsonRpc(jsonrpc.JsonRpc20):
    def __init__(self, nodeid=None, nodeaddr=None):
        jsonrpc.JsonRpc20.__init__(self)
        self.nodeid = nodeid
        self.nodeaddr = nodeaddr

    def dumps_response(self, result, msgid=None):
        # include our id + addr in the answer so that the remote client
        # can update his routing table
        res = dict(nodeid=self.nodeid, nodeaddr=self.nodeaddr, result=result)
        return jsonrpc.JsonRpc20.dumps_response(self, res, msgid)

def decorator(function):
    def decorated(*args, **kwargs):
        # fetch the client addr and id
        caddr, cid, args = args
        # update our routing table
        routing.table[cid] = caddr
        return function(*args, **kwargs)
    decorated.__name__ = function.__name__
    decorated.__doc__ = function.__doc__
    return decorated

def logF(msg):
    logging.debug(msg)

class Server(jsonrpc.Server):

    def __init__(self, id, port, log=False):
        logfunc = (log and logF) or jsonrpc.log_dummy

        address = ('', port)
        jsonrpc.Server.__init__(self, ChordJsonRpc(id, address),
                                jsonrpc.TransportTcpIp(addr=address,
                                    limit=MSG_LIMIT,
                                    timeout=10.0,
                                    logfunc=logfunc), logfile='log')
    def register_function(self, function, name=None):
        f = decorator(function)
        jsonrpc.Server.register_function(self, f, name)

class ServerProxy(jsonrpc.ServerProxy):
    def __init__(self, laddress, lid, raddress):
        """
        laddress:  local address
        lid:       local id
        lrouting:  local routing table
        raddress:  remote address
        """
        # both tuple and list are treated as JSON arrays
        if isinstance(raddress, list):
            raddress = tuple(raddress)

        self._laddress = laddress
        self._lid = lid
        print "Connecting to node: {}".format(raddress)
        jsonrpc.ServerProxy.__init__(self, ChordJsonRpc(),
                                    jsonrpc.TransportTcpIp(addr=raddress,
                                                limit=MSG_LIMIT,
                                                timeout=10.0))

    def __req(self, methodname, args=None, kwargs=None, id=0):
        # send along the address of the querier,
        # + id to update remote routing table
        args = (self._laddress, self._lid, args)

        res = jsonrpc.ServerProxy.__req(self, methodname, args, kwargs, id)

        # update the local routing table
        routing.table[res['nodeid']] = res['nodeaddr']

        return res['result']

