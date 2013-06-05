path = './logs/No-mem (1-200k) (:24)/'

colors <- function(type = seq(1, 7)) {
  if (length(type) > 1) {
    sapply(type, FUN=colors)
  } else {
    intVal = as.integer(type)
    if (is.factor(type))
      intVal = as.integer(paste(type))
    
    switch(intVal,
{"#4262e0"}, 
{"#1eb956"},
{"#e04242"},
{"#faf057"},
{"#FF8A17"},
{"#B03CD4"},
{"#f56991"}
    )
  }
}

readLogs <- function (fileName) {
  logs <- read.csv(file=paste(path, fileName, sep=''), header=FALSE, sep='\t')
  names(logs) <- c('client', 'address', 'latency', 'level')
  #logs[,'address'] <- as.character(logs[, 'address'])
  logs[,'level'] <- as.factor(logs[,'level'])
  
  summary(logs)
  
  x11()
  par(mfcol=c(2, 1))
  plot(logs['level'])
  title(fileName)
  hist(logs[, 'latency'])
  
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

kad.lfu.128 = readLogs('kademlia_no_mem_lfu_128.logs')
kad.lfu.256 = readLogs('kademlia_no_mem_lfu_256.logs')
kad.lfu.512 = readLogs('kademlia_no_mem_lfu_512.logs')
kad.lru.128 = readLogs('kademlia_no_mem_lru_128.logs')
kad.lru.256 = readLogs('kademlia_no_mem_lru_256.logs')
kad.lru.512 = readLogs('kademlia_no_mem_lru_512.logs')
kad.fifo.128 = readLogs('kademlia_no_mem_fifo_128.logs')
kad.fifo.256 = readLogs('kademlia_no_mem_fifo_256.logs')
kad.fifo.512 = readLogs('kademlia_no_mem_fifo_512.logs')

compareLogs(list(
  kad.lfu.128 = kad.lfu.128,
  kad.lfu.256 = kad.lfu.256,
  kad.lfu.512 = kad.lfu.512,
  kad.lru.128 = kad.lru.128,
  kad.lru.256 = kad.lru.256,
  kad.lru.512 = kad.lru.512,
  kad.fifo.128 = kad.fifo.128,
  kad.fifo.256 = kad.fifo.256,
  kad.fifo.512 = kad.fifo.512
)) -> result


groupped.results <- rbind(result[seq(1, 9, 3), 2], result[seq(2, 9, 3), 2], result[seq(3, 9, 3), 2])

colnames(groupped.results) <- c("kad.lfu", "kad.lru", "kad.fifo")
rownames(groupped.results) <- c(128, 256, 512)

groupped.results

par(family="Delicious")

midpoints <- barplot(groupped.results*100, beside=TRUE, legend.text=TRUE, col=colors(seq(1,3)))
text(x=midpoints, y=2, labels=floor(groupped.results*1000)/10, family="Delicious Heavy")

midpoints <- barplot(t(groupped.results*100), beside=TRUE, legend.text=TRUE, col=colors(seq(1, 3)))
text(x=midpoints, y=2, labels=floor(t(groupped.results)*1000)/10, family="Delicious Heavy")


#Saving results
write.table(groupped.results, file=paste(path, 'kad_groupped', sep=''))
write.table(result, file=paste(path, 'kad_results', sep=''))
