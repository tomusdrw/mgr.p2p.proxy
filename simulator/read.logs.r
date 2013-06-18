source('commons.R')

path = './logs/No-p2p (1-200k) (:24)/'


#kad.lfu.128 = readLogs(path, 'kademlia_no_mem_lfu_128.logs')
kad.lfu.256 = readLogs(path, 'kademlia_no_mem_lfu_256.logs')
kad.lfu.512 = readLogs(path, 'kademlia_no_mem_lfu_512.logs')
kad.lfu.1024 = readLogs(path, 'kademlia_no_mem_lfu_1024.logs')
kad.lfu.2048 = readLogs(path, 'kademlia_no_mem_lfu_2048.logs')
kad.lfu.4096 = readLogs(path, 'kademlia_no_mem_lfu_4096.logs')
#kad.lru.128 = readLogs(path, 'kademlia_no_mem_lru_128.logs')
kad.lru.256 = readLogs(path, 'kademlia_no_mem_lru_256.logs')
kad.lru.512 = readLogs(path, 'kademlia_no_mem_lru_512.logs')
kad.lru.1024 = readLogs(path, 'kademlia_no_mem_lru_1024.logs')
kad.lru.2048 = readLogs(path, 'kademlia_no_mem_lru_2048.logs')
kad.lru.4096 = readLogs(path, 'kademlia_no_mem_lru_4096.logs')
#kad.fifo.128 = readLogs(path, 'kademlia_no_mem_fifo_128.logs')
kad.fifo.256 = readLogs(path, 'kademlia_no_mem_fifo_256.logs')
kad.fifo.512 = readLogs(path, 'kademlia_no_mem_fifo_512.logs')
kad.fifo.1024 = readLogs(path, 'kademlia_no_mem_fifo_1024.logs')
kad.fifo.2048 = readLogs(path, 'kademlia_no_mem_fifo_2048.logs')
kad.fifo.4096 = readLogs(path, 'kademlia_no_mem_fifo_4096.logs')

compareLogs(list(
  #kad.lfu.128 = kad.lfu.128,
  kad.lfu.256 = kad.lfu.256,
  kad.lfu.512 = kad.lfu.512,
  kad.lfu.1024 = kad.lfu.1024,
  kad.lfu.2048 = kad.lfu.2048,
  kad.lfu.4096 = kad.lfu.4096,
  #kad.lru.128 = kad.lru.128,
  kad.lru.256 = kad.lru.256,
  kad.lru.512 = kad.lru.512,
  kad.lru.1024 = kad.lru.1024,
  kad.lru.2048 = kad.lru.2048,
  kad.lru.4096 = kad.lru.4096,
  #kad.fifo.128 = kad.fifo.128,
  kad.fifo.256 = kad.fifo.256,
  kad.fifo.512 = kad.fifo.512,
  kad.fifo.1024 = kad.fifo.1024,
  kad.fifo.2048 = kad.fifo.2048,
  kad.fifo.4096 = kad.fifo.4096
)) -> result


groupped.results <- rbind(result[seq(1, 15, 5), 2], result[seq(2, 15, 5), 2], result[seq(3, 15, 5), 2], result[seq(4, 15, 5), 2], result[seq(5, 15, 5), 2])

#groupped.results <- rbind(result[seq(1, 9, 3), 2], result[seq(2, 9, 3), 2], result[seq(3, 9, 3), 2])

colnames(groupped.results) <- c("kad.lfu", "kad.lru", "kad.fifo")
rownames(groupped.results) <- c(256, 512, 1024, 2048, 4096)
#rownames(groupped.results) <- c(128, 256, 512)

groupped.results

par(family="Delicious")

midpoints <- barplot(groupped.results*100, beside=TRUE, legend.text=TRUE, col=colors(seq(1, 5)))
text(x=midpoints, y=2, labels=floor(groupped.results*1000)/10, family="Delicious Heavy")

midpoints <- barplot(t(groupped.results*100), beside=TRUE, legend.text=TRUE, col=colors(seq(1, 3)))
text(x=midpoints, y=2, labels=floor(t(groupped.results)*1000)/10, family="Delicious Heavy")


#Saving results
write.table(groupped.results, file=paste(path, 'kad_groupped', sep=''))
write.table(result, file=paste(path, 'kad_results', sep=''))
