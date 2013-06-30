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
{"#f56991"},
{"#eeeeee"}
    )
  }
}


compareLogs <- function(logs) {
  result <- lapply(logs, function(log){
    cacheL1 <- length(which(log[, 'level'] == 1))
    cacheL2 <- length(which(log[, 'level'] == 2))
    total <- length(log[, 1])
   
    latencyTake <- log[, 'level'] == 2
    l <- c(cacheL1 / total, cacheL2 / total, mean(log[latencyTake, 'latency'], na.rm=TRUE))
    l <- c(l, as.vector(summary(na.omit(log[latencyTake, 'latency']))))
    return(l)
  })
  df <- t(data.frame(result))
  colnames(df) <- c('L1 Cache hits [%]', 'L2 Cache hits [%]', 'Mean', 'Min latency', '1st Q.', 'Median', 'Mean', '3rd Q', 'Max latency')
  return(df)
  #return(data.frame(matrix(unlist(result), nrow=length(logs), byrow=T)))
}

readLogs <- function (path, fileName) {
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
