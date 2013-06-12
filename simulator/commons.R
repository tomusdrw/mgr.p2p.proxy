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
