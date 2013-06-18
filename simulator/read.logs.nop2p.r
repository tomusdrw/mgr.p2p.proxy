source('commons.R')

path = './logs/No-p2p (1-200k) (:24) 6/'

lfu.256 = readLogs(path, 'lfu_256_no_p2p.logs')
lfu.512 = readLogs(path, 'lfu_512_no_p2p.logs')
lfu.1024 = readLogs(path, 'lfu_1024_no_p2p.logs')
lfu.2048 = readLogs(path, 'lfu_2048_no_p2p.logs')
lfu.4096 = readLogs(path, 'lfu_4096_no_p2p.logs')

lru.256 = readLogs(path, 'lru_256_no_p2p.logs')
lru.512 = readLogs(path, 'lru_512_no_p2p.logs')
lru.1024 = readLogs(path, 'lru_1024_no_p2p.logs')
lru.2048 = readLogs(path, 'lru_2048_no_p2p.logs')
lru.4096 = readLogs(path, 'lru_4096_no_p2p.logs')

fifo.256 = readLogs(path, 'fifo_256_no_p2p.logs')
fifo.512 = readLogs(path, 'fifo_512_no_p2p.logs')
fifo.1024 = readLogs(path, 'fifo_1024_no_p2p.logs')
fifo.2048 = readLogs(path, 'fifo_2048_no_p2p.logs')
fifo.4096 = readLogs(path, 'fifo_4096_no_p2p.logs')

compareLogs(list(
  lfu.256 = lfu.256,
  lfu.512 = lfu.512,
  lfu.1024 = lfu.1024,
  lfu.2048 = lfu.2048,
  lfu.4096 = lfu.4096,
  
  lru.256 = lru.256,
  lru.512 = lru.512,
  lru.1024 = lru.1024,
  lru.2048 = lru.2048,
  lru.4096 = lru.4096,
  
  fifo.256 = fifo.256,
  fifo.512 = fifo.512,
  fifo.1024 = fifo.1024,
  fifo.2048 = fifo.2048,
  fifo.4096 = fifo.4096
)) -> result


groupped.results <- rbind(result[seq(1, 15, 5), 1], result[seq(2, 15, 5), 1], result[seq(3, 15, 5), 1], result[seq(4, 15, 5), 1], result[seq(5, 15, 5), 1])

#groupped.results <- rbind(result[seq(1, 9, 3), 2], result[seq(2, 9, 3), 2], result[seq(3, 9, 3), 2])

colnames(groupped.results) <- c("lfu", "lru", "fifo")
rownames(groupped.results) <- c(256, 512, 1024, 2048, 4096)
#rownames(groupped.results) <- c(128, 256, 512)

groupped.results

par(family="Delicious")

midpoints <- barplot(groupped.results*100, beside=TRUE, legend.text=TRUE, col=colors(seq(1, 5)))
text(x=midpoints, y=2, labels=floor(groupped.results*1000)/10, family="Delicious Heavy")

midpoints <- barplot(t(groupped.results*100), beside=TRUE, legend.text=TRUE, col=colors(seq(1, 3)))
text(x=midpoints, y=2, labels=floor(t(groupped.results)*1000)/10, family="Delicious Heavy")


#Saving results
write.table(groupped.results, file=paste(path, 'nop2p_groupped', sep=''))
write.table(result, file=paste(path, 'nop2p_results', sep=''))
