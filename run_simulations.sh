#!/bin/bash

ALGOS1=(lfu lru)
ALGOS=(lfu lru fifo)
SIZES=(128 256)

for memAlgo in ${ALGOS1[*]}
do
  for p2pAlgo in ${ALGOS[*]}
  do
    for size in ${SIZES[*]}
    do
      echo "Running simulation for ${memAlgo}(${size}) ${p2pAlgo}(${size})"
      time ./simulator_main.py --mem-algo $memAlgo --p2p-algo $p2pAlgo --mem-size $size --p2p-size $size > logs/run_${memAlgo}_${size}_${p2pAlgo}_${size}.log
    done
  done
done
