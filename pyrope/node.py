# -*- coding:utf-8 -*-
__author__    = "Nicolas Dumazet"
__copyright__ = "Copyright 2009, Nicolas Dumazet"
__license__   = "MIT"
__version__   = "0.1.0dev"
__email__     = "nicdumz@gmail.com"
__status__    = "Prototype"

# network size (< 2^SIZE)
SIZE = 16
MAX = 2**SIZE

import network
import routing

def comparer(leftop, rightop, doc):
    def comp(n, lo, hi):
        if lo <= hi:
            return leftop(lo, n) and rightop(n, hi)
        return leftop(lo, n) or rightop(n, hi)

    comp.__doc__ = doc
    return comp

from operator import le, lt

inRange = comparer(le, lt, "Returns True if i in [j, k[")
inStrictRange = comparer(lt, lt, "Returns True if i in ]j, k[")
inRange2 = comparer(lt, le, "Returns True if i in ]j, k]")

class Node(object):
    """
    Methods starting by _ are helper/private methods.
    Other methods are registered in the Json RPC server, and can
    be remotely called by other nodes.
    """
    def __init__(self, id, port, remoteAddr=None):
        id %= MAX
        self.id = id
        self.port = port
        routing.table[id] = ('',port)

        self.fingers = [id] * SIZE
        self.starts = []
        tmp = 1
        for i in range(SIZE):
            self.starts.append((id + tmp) % MAX)
            tmp *= 2

        self.predecessor = id

        self.server = network.Server(id, port, log=True)

        self.server.register_instance(self)

        if remoteAddr is not None:
            self._join(remoteAddr)

        self.server.serve()


    def _join(self, address):
        """
        Join a chord network. At (address, port), there should be a
        chord Node listening for connections.
        """
        other = network.ServerProxy(routing.table[self.id],
                                    self.id,
                                    address)

        self.fingers[0], addr = other.find_successor(self.starts[0])
        if addr is not None:
            # self.fingers[0] is different from 'other'
            routing.table[self.fingers[0]] = addr
        self.predecessor, addr = self._getNode(self.fingers[0]).updatePredecessor(self.id)
        if addr is not None:
            routing.table[self.predecessor] = addr

        tmp = [self.fingers[0]]
        for start in self.starts[1:]:
            if inRange(start, self.id, tmp[-1]):
                tmp.append(tmp[-1])
            else:
                id, addr = other.find_successor(start)
                if addr is not None:
                    routing.table[id] = addr
                tmp.append(id)

        self.fingers = tmp

        # update others
        for i in range(SIZE):
            p = self._find_predecessor((self.id - 2**i) % MAX)
            p.update_finger_table(self.id, i)


    def _getNode(self, id):
        if id == self.id:
            return self
        try:
            address = routing.table[id]
        except KeyError:
            print('routing problem, can\'t find id', id)
        return network.ServerProxy(routing.table[self.id],
                                    self.id,
                                    address)

    def find_successor(self, id):
        """
        @return id, address
        """
        return self._find_predecessor(id).getSuccessor()


    def getSuccessor(self):
        """
        @return id, address
        """
        id = self.fingers[0]
        if id == self.id:
            return id, None
        return id, routing.table[id]

    def updatePredecessor(self, newId):
        """
        @return id, addr
        """
        ret = self.predecessor
        self.predecessor = newId
        if ret == self.id:
            return ret, None
        return ret, routing.table[ret]

    def _find_predecessor(self, id):
        """
        @return Node
        """
        n = self
        n_id = self.id
        next_id, n_succ  = self.closest_preceding_and_successor(id)
        while inRange2(id, n_succ, n_id):
            n_id = next_id
            n = self._getNode(n_id)
            next_id, n_succ  = n.closest_preceding_and_successor(id)
        return n

    def closest_preceding_and_successor(self, id):
        return self._closest_preceding_finger(id), self.getSuccessor()[0]

    def _closest_preceding_finger(self, id):
        """
        @return id
        """
        for e in self.fingers[::-1]:
            if inStrictRange(e, self.id, id):
                return e
        return self.id

    def update_finger_table(self, s, i):
        """
        Notification.
        """
        if inRange(s, self.id, self.fingers[i]):
            self.fingers[i] = s
            p = self._getNode(self.predecessor)
            p.update_finger_table(s, i)
