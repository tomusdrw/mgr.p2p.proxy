from simulator import Simulator
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

simulator = Simulator(nodesId=["Node1", "Node2", "Node3", "Node4", "Node5", "Node6"])
simulator.start([
                 ("Node1", 1, "someAdress"),
                 ("Node1", 1, "someAdress2"),
                 ("Node2", 4, "someAdress3"),
                 # Those should go from cache
                 ("Node1", 5, "someAdress2"),
                 ("Node2", 5, "someAdress")
                 ])


