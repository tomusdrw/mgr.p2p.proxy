source('commons.R')

library(data.table)

paths = c(
  'No-p2p (1-200k) (:24)',
  'No-p2p (1-200k) (:24) 2',
  'No-p2p (1-200k) (:24) 3',
  'No-p2p (1-200k) (:24) 4',
  'No-p2p (1-200k) (:24) 5'
)

values = c(256, 512, 1024, 2048, 4096)


lapply(paths, function(path) {
  #Read results
  path.data <- read.table(file=paste('logs/', path, '/nop2p_results', sep=''))
  path.data[, 'type'] <- rownames(path.data)
  
  path.data
}) -> results

# Combine results
do.call(rbind, results) -> combined.results

# Define order
levels.sorted <- unlist(do.call(c, lapply(values, function(val){
  lapply(c('lfu', 'lru', 'fifo'), function(p) {
    paste(p, val, sep='.')
  })
})))
# Group values
combined.results[, 'type'] <- factor(combined.results[, 'type'], levels=levels.sorted)
summary(combined.results)

combined.results.table = data.table(combined.results)
mean.results2 <- data.frame(combined.results.table[,mean(L1.Cache.hits....), by=type])

mean.results <- data.frame(row.names = mean.results2[, 'type'], mean.results2[, 'V1'])
groupped.results <- rbind(result[seq(1, 15, 5), 1], result[seq(2, 15, 5), 1], result[seq(3, 15, 5), 1], result[seq(4, 15, 5), 1], result[seq(5, 15, 5), 1])
colnames(groupped.results) <- c("lfu", "lru", "fifo")
rownames(groupped.results) <- c(256, 512, 1024, 2048, 4096)

par(family="Delicious")

setEPS()
postscript('nop2p_mean_1.eps')
midpoints <- barplot(groupped.results*100, beside=TRUE, col = colors(seq(1, 5)), names.arg=c('lfu', 'lru', 'fifo'))
text(x=midpoints, y=2, labels=floor(groupped.results*1000)/10, family="Delicious Heavy", cex=0.7)
legend("right", legend=c('256', '512', '1024', '2048', '4096'), bty='0', pch=19, col=colors(seq(1, 5)))
dev.off()

setEPS()
postscript('nop2p_mean_2.eps')
midpoints <- barplot(t(groupped.results*100), beside=TRUE, col=colors(seq(1, 3)))
legend("right", legend=c('lfu', 'lru', 'fifo'), bty='0', pch=19, col=colors(seq(1, 3)))
text(x=midpoints, y=2, labels=floor(t(groupped.results)*1000)/10, family="Delicious Heavy", cex=0.7)
dev.off()


setEPS()
postscript('nop2p_all.eps')
plot(formula = L1.Cache.hits.... ~ type, data=combined.results, col=colors(seq(1, 3)))
legend("bottomright", legend=c('lfu', 'lru', 'fifo'), bty='0', pch=19, col=colors(seq(1, 3)))
dev.off()