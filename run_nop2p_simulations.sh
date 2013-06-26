#!/bin/bash

#NET=(kademlia kademlia kademlia kademlia kademlia)
DATA=(sv)
#ALGOS=(lfu lru fifo)
ALGOS=(lfu lru)
SIZES=(8192 16384)
#SIZES=(1024 2048 4096 8192 16384)


for data in ${DATA[*]}
do
  rm simulator/data
  ln -s data-$data simulator/data
  for memAlgo in ${ALGOS[*]}
  do
    for size in ${SIZES[*]}
    do
      echo "Running simulation for MEM ${memAlgo}(${size})"
      time ./simulator_main.py --no-p2p --mem-algo $memAlgo --mem-size $size > logs/run_${memAlgo}_${size}_nop2p.log
    done
  done
  mv logs logs_nop2p_$data
  mkdir logs
done
