#!/bin/bash

NET=(kademlia kademlia kademlia kademlia)
#NET=(kademlia)
ALGOS=(lfu lru fifo)
SIZES=(256 512 1024 2048 4096)

# Increase UDP buffer size
sudo sysctl -w net.core.rmem_max=26214400
sudo sysctl -w net.core.rmem_default=26214400

# This is (probably) not needed if no errors is reported in netstat -s
#sudo sysctl -w net.core.wmem_max=5242880
#sudo sysctl -w net.core.wmem_default=5242880

I=0
for network in ${NET[*]}
do
  for p2pAlgo in ${ALGOS[*]}
  do
    for size in ${SIZES[*]}
    do
      echo "Running simulation for P2P ${p2pAlgo}(${size})"
      time ./simulator_main.py --no-mem --p2p-algo $p2pAlgo --p2p-size $size  --p2p-network $network > logs/run_no_mem_${network}_${p2pAlgo}_${size}.log
    done
  done
  mv logs logs_$I
  mkdir logs
  I=$I+1
done
