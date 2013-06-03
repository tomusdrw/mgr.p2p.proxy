#!/bin/bash

ALGOS=(lfu lru fifo)
SIZES=(128 256 512)

for p2pAlgo in ${ALGOS[*]}
do
  for size in ${SIZES[*]}
  do
    echo "Running simulation for P2P ${p2pAlgo}(${size})"
    time ./simulator_main.py --no-mem --p2p-algo $p2pAlgo --p2p-size $size  > logs/run_no_mem_${p2pAlgo}_${size}.log
  done
done
