source(commons.R)


# Plot mean webpage size
data <- data.frame(row.names = c('2000', '2010', '2011', '2012', '2013'), c(60, 702, 929, 1269, 1462))
colnames(data) <- c('Mean Webpage Size')


setEPS()
postscript('mean_webpage_size.eps')
midpoints <- barplot(data[, 1], names.arg=row.names(data), col=colors(seq(1, 5)))
text(x=midpoints, y=500, labels=data[, 1], family="Delicious Heavy")
title('Mean Webpage Size [kB]')
dev.off()