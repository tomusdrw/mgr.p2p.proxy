source('commons.R')

path = './logs/No-mem (1-200k) (:24) (rmem=25MB) 6/'

readLogs <- function (fileName) {
  logs <- read.csv(file=paste(path, fileName, sep=''), header=FALSE, sep='\t')
  names(logs) <- c('client', 'address', 'latency', 'level')
  #logs[,'address'] <- as.character(logs[, 'address'])
  logs[,'level'] <- as.factor(logs[,'level'])
  
  summary(logs)
  
  #x11()
  #par(mfcol=c(2, 1))
  #plot(logs['level'])
  #title(fileName)
  #hist(logs[, 'latency'])
  
  return(logs)
}

compareLogs <- function(logs) {
  result <- lapply(logs, function(log){
    cacheL1 <- length(which(log[, 'level'] == 1))
    cacheL2 <- length(which(log[, 'level'] == 2))
    total <- length(log[, 1])
    
    l <- c(cacheL1 / total, cacheL2 / total, mean(log[, 'latency'], na.rm=TRUE))
    return(l)
  })
  df <- t(data.frame(result))
  colnames(df) <- c('L1 Cache hits [%]', 'L2 Cache hits [%]', 'Mean latency')
  return(df)
  #return(data.frame(matrix(unlist(result), nrow=length(logs), byrow=T)))
}

#kad.lfu.128 = readLogs('kademlia_no_mem_lfu_128.logs')
kad.lfu.256 = readLogs('kademlia_no_mem_lfu_256.logs')
kad.lfu.512 = readLogs('kademlia_no_mem_lfu_512.logs')
kad.lfu.1024 = readLogs('kademlia_no_mem_lfu_1024.logs')
kad.lfu.2048 = readLogs('kademlia_no_mem_lfu_2048.logs')
kad.lfu.4096 = readLogs('kademlia_no_mem_lfu_4096.logs')
#kad.lru.128 = readLogs('kademlia_no_mem_lru_128.logs')
kad.lru.256 = readLogs('kademlia_no_mem_lru_256.logs')
kad.lru.512 = readLogs('kademlia_no_mem_lru_512.logs')
kad.lru.1024 = readLogs('kademlia_no_mem_lru_1024.logs')
kad.lru.2048 = readLogs('kademlia_no_mem_lru_2048.logs')
kad.lru.4096 = readLogs('kademlia_no_mem_lru_4096.logs')
#kad.fifo.128 = readLogs('kademlia_no_mem_fifo_128.logs')
kad.fifo.256 = readLogs('kademlia_no_mem_fifo_256.logs')
kad.fifo.512 = readLogs('kademlia_no_mem_fifo_512.logs')
kad.fifo.1024 = readLogs('kademlia_no_mem_fifo_1024.logs')
kad.fifo.2048 = readLogs('kademlia_no_mem_fifo_2048.logs')
kad.fifo.4096 = readLogs('kademlia_no_mem_fifo_4096.logs')

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
