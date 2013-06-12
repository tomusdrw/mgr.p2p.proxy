source('commons.R')

paths = c(
  'No-mem (1-200k) (:24) 2',
  'No-mem (1-200k) (:24) 3',
  'No-mem (1-200k) (:24) 4',
  'No-mem (1-200k) (:24) 5',
  'No-mem (1-200k) (:24) (rmem=25MB) 2'
)

values = c(256, 512, 1024, 2048)


lapply(paths, function(path) {
  #Read results
  path.data <- read.table(file=paste('logs/', path, '/kad_results', sep=''))
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
# Group values
combined.results[, 'type'] <- factor(combined.results[, 'type'], levels=levels.sorted)
summary(combined.results)

plot(formula = L2.Cache.hits.... ~ type, data=combined.results, col=colors(seq(1, 3)))
legend("bottomright", legend=c('lfu', 'lru', 'fifo'), bty='0', pch=19, col=colors(seq(1, 3)))