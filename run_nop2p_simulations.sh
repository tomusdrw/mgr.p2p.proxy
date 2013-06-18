#!/bin/bash

NET=(kademlia kademlia kademlia kademlia kademlia)
#NET=(kademlia)
ALGOS=(lfu lru fifo)
SIZES=(256 512 1024 2048 4096)


I=0
for network in ${NET[*]}
do
  for memAlgo in ${ALGOS[*]}
  do
    for size in ${SIZES[*]}
    do
      echo "Running simulation for MEM ${memAlgo}(${size})"
      time ./simulator_main.py --no-p2p --mem-algo $memAlgo --mem-size $size  --p2p-network $network > logs/run_${memAlgo}_${size}_nop2p.log
    done
  done
  mv logs logs_$I
  mkdir logs
  I=$I+1
done
