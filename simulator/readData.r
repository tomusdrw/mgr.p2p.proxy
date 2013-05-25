data <- read.table('data/uc.sanitized-access.20070109')
# REmove some superflous columns
data <- data[, -8] #
data <- data[, -2]
# Name columns properly
colnames(data) <- c('time', 'client', 'type', 'size', 'verb', 'address', 'original', 'mimetype')
# Normalize time
data['time'] <- data['time'] - data[1, 'time']

# Filter only GET requests and only some columns
getData <- data[data['verb'] == 'GET', c('time', 'client', 'address')]

# Data is taken from 24 hours, but we don't want to wait so long for tests
getData['time'] <- getData['time'] / 48

# Get unique clients
clients <- unique(getData[, 'client'])
for (client in clients) {
  clientData <- getData[getData['client'] == client, c('time', 'address')]
  write.csv(clientData, file = paste('data/client/', client, sep=''), col.names=FALSE, row.names=FALSE, quote=FALSE)
}

write.csv(clients, file='data/clients.txt', row.names=FALSE, col.names=FALSE, quote=FALSE)