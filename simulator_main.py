from simulator import Simulator
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

simulator = Simulator(requests={
    "Node1" : [
                 (1, "someAdress"),
                 (1, "someAdress2"),
                 (5, "someAdress2")
              ],
    "Node2" : [
                 (4, "someAdress3"),
                 (5, "someAdress")
             ],
    "Node3": [],
    "Node4": [],
    "Node5" : [
                 (0.5, "someAdress7"),
                 (1.5, "someAdress2"),
                 (5, "someAdress4")
              ],
    "Node6" : [
                 (2, "someAdress3"),
                 (1, "someAdress")
             ],
    "Node7": [],
    "Node8": []
})
simulator.start()


