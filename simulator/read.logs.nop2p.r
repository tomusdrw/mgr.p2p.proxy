source('commons.R')

path = './logs/No P2P (1-250k) (:18) - UC/'

lfu.1024 = readLogs(path, 'lfu_1024_no_p2p.logs')
lfu.2048 = readLogs(path, 'lfu_2048_no_p2p.logs')
lfu.4096 = readLogs(path, 'lfu_4096_no_p2p.logs')
lfu.8192 = readLogs(path, 'lfu_8192_no_p2p.logs')
lfu.16384 = readLogs(path, 'lfu_16384_no_p2p.logs')

lru.1024 = readLogs(path, 'lru_1024_no_p2p.logs')
lru.2048 = readLogs(path, 'lru_2048_no_p2p.logs')
lru.4096 = readLogs(path, 'lru_4096_no_p2p.logs')
lru.8192 = readLogs(path, 'lru_8192_no_p2p.logs')
lru.16384 = readLogs(path, 'lru_16384_no_p2p.logs')

fifo.1024 = readLogs(path, 'fifo_1024_no_p2p.logs')
fifo.2048 = readLogs(path, 'fifo_2048_no_p2p.logs')
fifo.4096 = readLogs(path, 'fifo_4096_no_p2p.logs')
fifo.8192 = readLogs(path, 'fifo_8192_no_p2p.logs')
fifo.16384 = readLogs(path, 'fifo_16384_no_p2p.logs')

compareLogs(list(
  lfu.1024 = lfu.1024,
  lfu.2048 = lfu.2048,
  lfu.4096 = lfu.4096,
  lfu.8192 = lfu.8192,
  lfu.16384 = lfu.16384,
  
  lru.1024 = lru.1024,
  lru.2048 = lru.2048,
  lru.4096 = lru.4096,
  lru.8192 = lru.8192,
  lru.16384 = lru.16384,
  
  fifo.1024 = fifo.1024,
  fifo.2048 = fifo.2048,
  fifo.4096 = fifo.4096,
  fifo.8192 = fifo.8192,
  fifo.16384 = fifo.16384
)) -> result


groupped.results <- rbind(result[seq(1, 15, 5), 1], result[seq(2, 15, 5), 1], result[seq(3, 15, 5), 1], result[seq(4, 15, 5), 1], result[seq(5, 15, 5), 1])

colnames(groupped.results) <- c("lfu", "lru", "fifo")
rownames(groupped.results) <- c(1024, 2048, 4096, 8192, 16384)

groupped.results

par(family="Delicious")


setEPS()
postscript('nop2p_uc_1.eps')
midpoints <- barplot(groupped.results*100, beside=TRUE, col=colors(seq(1, 5)))
legend("right", legend=rownames(groupped.results), bty='0', pch=19, col=colors(seq(1, 5)), bg="#ffffff")
text(x=midpoints, y=2, labels=floor(groupped.results*1000)/10, family="Delicious Heavy", cex=0.8)
title("Percentage of Cache Hits [%]")
mtext("Local cache for UC data")
dev.off()

midpoints <- barplot(t(groupped.results*100), beside=TRUE, col=colors(seq(1, 3)))
legend("right", legend=colnames(groupped.results), bty='0', pch=19, col=colors(seq(1, 3)), bg="#ffffff")
text(x=midpoints, y=2, labels=floor(t(groupped.results)*1000)/10, family="Delicious Heavy", cex=0.8)
title("Percentage of Cache Hits [%]")
mtext("Local cache for UC data")

#Saving results
write.table(groupped.results, file=paste(path, 'nop2p_groupped', sep=''))
write.table(result, file=paste(path, 'nop2p_results', sep=''))
