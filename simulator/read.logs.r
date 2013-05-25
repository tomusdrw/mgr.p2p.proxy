readLogs <- function (fileName) {
  logs <- read.csv(file=paste('../logs/', fileName, sep=''), header=FALSE, sep='\t')
  names(logs) <- c('client', 'address', 'latency', 'level')
  #logs[,'address'] <- as.character(logs[, 'address'])
  logs[,'level'] <- as.factor(logs[,'level'])
  
  summary(logs)
  
  par(mfcol=c(2, 1))
  plot(logs['level'])
  hist(logs[, 'latency'])
  
  return(logs)
}

lru.64.lfu.64 = readLogs('lru_64_lfu_64.logs')
lru.128.lfu.128 = readLogs('lru_128_lfu_128.logs')
