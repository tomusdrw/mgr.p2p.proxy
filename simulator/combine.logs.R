source('commons.R')

data <- 'UC'
paths = c(
 #'No mem (1-250k) (:18) - dell - SJ',
 #'No mem (1-250k) (:18) - dell - SV',
 'No mem (1-250k) (:18) - dell - UC',
 #'No mem (1-250k) (:18) - morse2 - SJ',
 #'No mem (1-250k) (:18) - morse2 - SV',
 'No mem (1-250k) (:18) - morse2 - UC'
)

values = c(512, 1024, 2048, 4096, 8192)


lapply(paths, function(path) {
  #Read results
  path.data <- read.table(file=paste('logs/', path, '/kad_results', sep=''))
  path.data <- floor(path.data*1000)/10
  path.data <- path.data[, seq(1, 3)]
  colnames(path.data)<- c('L1.Cache', 'L2.Cache', 'Mean')
  path.data[, 'type'] <- rownames(path.data)
  
  path.data
}) -> results

# Combine results
do.call(rbind, results) -> combined.results

# Define order
levels.sorted <- unlist(do.call(c, lapply(values, function(val){
  lapply(c('kad.lfu', 'kad.lru', 'kad.fifo'), function(p) {
    paste(p, val, sep='.')
  })
})))
# Combine values
combined.results[, 'type'] <- factor(combined.results[, 'type'], levels=levels.sorted)
summary(combined.results)

# Group values
vals <- length(values)
size <- vals * length(paths) * 3

sapply(seq(1, vals), function(i){
  cbind(
    mean(combined.results[seq(i, size, 3*vals), 2]), # lfu
    mean(combined.results[seq(i+vals, size, 3*vals), 2]), #lru
    mean(combined.results[seq(i+2*vals, size, 3*vals), 2]) #fifo
  )
}) -> mean.results
rownames(mean.results) <- c('lfu', 'lru', 'fifo')
colnames(mean.results) <- values
mean.results

setEPS()
postscript(paste('p2p_mean_', tolower(data), '_1.eps', sep=''))
midpoints <- barplot(t(mean.results), beside=TRUE, col=colors(seq(1, 5)), ylim=c(0, 45))
grid(nx=NA, ny=NULL)
legend("topleft", legend=colnames(mean.results), bty='0', pch=19, col=colors(seq(1, 5)), bg="#ffffff")
text(x=midpoints, y=t(mean.results) + 1, labels=t(mean.results), family="Delicious Heavy", cex=0.8)
title("Mean Cache Hits [%]")
mtext(paste("Kademlia cache for ", data, " data", sep=''))
dev.off()

setEPS()
postscript(paste('p2p_mean_', tolower(data), '_2.eps', sep=''))
midpoints <- barplot(mean.results, beside=TRUE, col=colors(seq(1, 3)), ylim=c(0, 45))
grid(nx=NA, ny=NULL)
legend("topleft", legend=rownames(mean.results), bty='0', pch=19, col=colors(seq(1, 3)), bg="#ffffff")
text(x=midpoints, y=mean.results+1, labels=mean.results, family="Delicious Heavy", cex=0.8)
title("Mean Cache Hits [%]")
mtext(paste("Kademlia cache for ", data, " data", sep=''))
dev.off()



levels(combined.results[, 4]) <- unlist(do.call(c, lapply(values, function(val){
  lapply(c('lfu', 'lru', 'fifo'), function(p) {
    paste(p, val, sep='.')
  })
})))

setEPS()
postscript('p2p_combined_all.eps')
plot(formula = L2.Cache ~ type, data=combined.results, col=colors(seq(1, 3)), xlab="", ylab="", ylim=c(0, 45))
grid(nx=NA, ny=NULL)
legend("bottomright", legend=c('lfu', 'lru', 'fifo'), bty='0', pch=19, col=colors(seq(1, 3)))
title("Cache Hits [%]")
mtext("Kademlia P2P cache")
dev.off()



