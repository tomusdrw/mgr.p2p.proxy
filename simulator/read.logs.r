readLogs <- function (fileName) {
  logs <- read.csv(file=paste('../logs/', fileName, sep=''), header=FALSE, sep='\t')
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

lru.128.lfu.128 = readLogs('lru_128_lfu_128.logs')
lru.128.lru.128 = readLogs('lru_128_lru_128.logs')
lfu.128.lru.128 = readLogs('lru_128_lru_128.logs')
lfu.128.lfu.128 = readLogs('lfu_128_lfu_128.logs')
lru.128.fifo.128 = readLogs('lru_128_fifo_128.logs')
lfu.128.fifo.128 = readLogs('lfu_128_fifo_128.logs')

compareLogs(list(
  lru_128_lfu_128 = lru.128.lfu.128,
  lru_128_lru_128 = lru.128.lru.128,
  lfu_128_lru_128 = lfu.128.lru.128,
  lfu_128_lfu_128 = lfu.128.lfu.128,
  lru_128_fifo_128 = lru.128.fifo.128,
  lfu_128_fifo_128 = lfu.128.fifo.128
)) -> result

plot(result)
