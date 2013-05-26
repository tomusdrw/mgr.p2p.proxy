import logging
import sys
from cache.test import StoreEverytingStorage
from cache.multi import TwoLevelCache
from cache.algo import LRU, LFU, Fifo
from p2p.node import Node, DeferredNodeCache
from p2p.chord import ChordNode, DeferredChordNodeCache

def initLogger(logLevel):
    levels = {
     'info' : logging.INFO,
     'debug' : logging.DEBUG,
     'warn' : logging.WARN
    }
    logging.basicConfig(stream=sys.stdout, level=levels[logLevel])


def initDefaultParserOptions(p, memAlgo='lru', memSize=1024, p2pAlgo='lfu', p2pSize=1024):
    p.add_argument('--log',
        help='Change logging mode',
        dest='log',
        default='info',
        choices=['info', 'debug', 'warn'])
    
    p.add_argument('--p2p-network',
        help='Change p2p network implementation',
        dest='p2p_net',
        default='kademlia',
        choices=['kademlia', 'chord']
    )
    
    p.add_argument('--p2p-port',
        metavar='P2P PORT',
        dest='p2p_port',
        type=int,
        default=4000,
        action='store',
        help='Port for P2P network node. In case of spawn it would be start port.'
    )
    
    p.add_argument('--mem-algo',
        help='Change memory cache algorithm',
        dest='mem_algo',
        default=memAlgo,
        choices=['lru', 'lfu', 'fifo'])
    p.add_argument('--mem-size',
        help='Change memory cache queue size',
        dest='mem_size',
        type=int,
        default=memSize)
    
    p.add_argument('--no-mem',
        help='Disable memory cache (use only P2P)',
        dest='no_mem',
        action='store_true'
        )
    
    p.add_argument('--p2p-algo',
        help='Change p2p cache algorithm',
        dest='p2p_algo',
        default=p2pAlgo,
        choices=['lru', 'lfu', 'fifo'])
    p.add_argument('--p2p-size',
        help='Change p2p cache queue size',
        dest='p2p_size',
        type=int,
        default=p2pSize)    

class ClientFactory:
    port = 4000
    
    memQueueSize = 128
    p2pQueueSize = 128
    
    memAlgo = LRU
    p2pAlgo = LFU
    
    noMem = False
    
    nodeClass = None
    nodeCacheClass = None
    
    def __init__(self):
        if self.noMem:
            logging.info("Settings: No memory, P2P {}({})".format(self.p2pAlgo.__name__, self.p2pQueueSize))
        else:
            logging.info("Settings: Mem: {}({}), P2P {}({})".format(self.memAlgo.__name__, self.memQueueSize, self.p2pAlgo.__name__, self.p2pQueueSize))
    
    def createNodeStorage(self):
        return self.p2pAlgo(StoreEverytingStorage(), queueSize=self.p2pQueueSize)
    
    def createNode(self, port, knownHosts):
        return self.nodeClass(knownHosts, port=port, cacheStorage=self.createNodeStorage())
    
    def createNodeCache(self, node):
        return self.nodeCacheClass(node)
    
    def createClientCache(self, node):
        p2pCache = self.createNodeCache(node)
        
        if self.noMem:
            return p2pCache
        else:
            memoryCache = self.memAlgo(StoreEverytingStorage(), queueSize=self.memQueueSize)
        
            return TwoLevelCache(memoryCache, p2pCache)
        

class ArgsClientFactory(ClientFactory):

    def __init__(self, args):
        self.port = args.p2p_port
        self.memAlgo = self.getAlgo(args.mem_algo)
        self.p2pAlgo = self.getAlgo(args.p2p_algo)
        
        self.memQueueSize = args.mem_size
        self.p2pQueueSize = args.p2p_size
        
        self.noMem = args.no_mem
        
        if args.p2p_net == 'kademlia':
            self.nodeClass = Node
            self.nodeCacheClass = DeferredNodeCache
        elif args.p2p_net == 'chord':
            self.nodeClass = ChordNode
            self.nodeCacheClass = DeferredChordNodeCache
        else:
            raise ValueError("Unknown p2p network implementation: {}".format(args.p2p_net))
                
        ClientFactory.__init__(self)
        
    def createNodeCache(self, node):
        # In case of chord we need to pass node proxy
        if self.nodeClass == ChordNode:
            node = node.node
            
        return ClientFactory.createNodeCache(self, node)
    
    def getAlgo(self, algoStr):
        algos = {
            'lfu' : LFU,
            'lru' : LRU,
            'fifo' : Fifo
        }
        return algos[algoStr]

     