source('commons.R')

data = 'SV'
path = paste('./logs/No mem (1-250k) (:18) - morse2 - ', data, '/', sep='')


kad.lfu.512 = readLogs(path, 'kademlia_no_mem_lfu_512.logs')
kad.lfu.1024 = readLogs(path, 'kademlia_no_mem_lfu_1024.logs')
kad.lfu.2048 = readLogs(path, 'kademlia_no_mem_lfu_2048.logs')
kad.lfu.4096 = readLogs(path, 'kademlia_no_mem_lfu_4096.logs')
kad.lfu.8192 = readLogs(path, 'kademlia_no_mem_lfu_8192.logs')
#
kad.lru.512 = readLogs(path, 'kademlia_no_mem_lru_512.logs')
kad.lru.1024 = readLogs(path, 'kademlia_no_mem_lru_1024.logs')
kad.lru.2048 = readLogs(path, 'kademlia_no_mem_lru_2048.logs')
kad.lru.4096 = readLogs(path, 'kademlia_no_mem_lru_4096.logs')
kad.lru.8192 = readLogs(path, 'kademlia_no_mem_lru_8192.logs')
#
kad.fifo.512 = readLogs(path, 'kademlia_no_mem_fifo_512.logs')
kad.fifo.1024 = readLogs(path, 'kademlia_no_mem_fifo_1024.logs')
kad.fifo.2048 = readLogs(path, 'kademlia_no_mem_fifo_2048.logs')
kad.fifo.4096 = readLogs(path, 'kademlia_no_mem_fifo_4096.logs')
kad.fifo.8192 = readLogs(path, 'kademlia_no_mem_fifo_8192.logs')

compareLogs(list(
  kad.lfu.512 = kad.lfu.512,
  kad.lfu.1024 = kad.lfu.1024,
  kad.lfu.2048 = kad.lfu.2048,
  kad.lfu.4096 = kad.lfu.4096,
  kad.lfu.8192 = kad.lfu.8192,
  kad.lru.512 = kad.lru.512,
  kad.lru.1024 = kad.lru.1024,
  kad.lru.2048 = kad.lru.2048,
  kad.lru.4096 = kad.lru.4096,
  kad.lru.8192 = kad.lru.8192,
  kad.fifo.512 = kad.fifo.512,
  kad.fifo.1024 = kad.fifo.1024,
  kad.fifo.2048 = kad.fifo.2048,
  kad.fifo.4096 = kad.fifo.4096,
  kad.fifo.8192 = kad.fifo.8192
)) -> result


groupped.results <- rbind(result[seq(1, 15, 5), 2], result[seq(2, 15, 5), 2], result[seq(3, 15, 5), 2], result[seq(4, 15, 5), 2], result[seq(5, 15, 5), 2])

colnames(groupped.results) <- c("lfu", "lru", "fifo")
rownames(groupped.results) <- c(512, 1024, 2048, 4096, 8192)

groupped.results

par(family="Delicious")

midpoints <- barplot(groupped.results*100, beside=TRUE, col=colors(seq(1, 5)))
legend("right", legend=rownames(groupped.results), bty='0', pch=19, col=colors(seq(1, 5)))
text(x=midpoints, y=2, labels=floor(groupped.results*1000)/10, family="Delicious Heavy", cex=0.8)
title("Percentage of Cache Hits [%]")
mtext(paste("Kademlia cache for", data, "data", sep=' '))

midpoints <- barplot(t(groupped.results*100), beside=TRUE, col=colors(seq(1, 3)))
legend("right", legend=colnames(groupped.results), bty='0', pch=19, col=colors(seq(1, 3)))
text(x=midpoints, y=2, labels=floor(t(groupped.results)*1000)/10, family="Delicious Heavy", cex=0.8)
title("Percentage of Cache Hits [%]")
mtext(paste("Kademlia cache for", data, "data", sep=' '))
            

#Saving results
write.table(groupped.results, file=paste(path, 'kad_groupped', sep=''))
write.table(result, file=paste(path, 'kad_results', sep=''))
