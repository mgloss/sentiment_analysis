setwd("C:/Dropbox/digi_academy/projekt/Czechitas")

commentsO2 <- read.csv("commentsO2.csv")

head(commentsO2)

commentsO2$message <- gsub("\n", " ", commentsO2$message)
commentsO2$message <- gsub("\t", " ", commentsO2$message)
commentsO2$message <- gsub(";", " ", commentsO2$message)
commentsO2$message <- gsub("\"", " ", commentsO2$message)


write.table(commentsO2, "commentsO2_clean.csv", row.names = F, sep = ";", fileEncoding = "UTF-8")



commentstm <- read.csv("commentsTM.csv")

head(commentstm)

commentstm$message <- gsub("\n", " ", commentstm$message)
commentstm$message <- gsub("\t", " ", commentstm$message)
commentstm$message <- gsub(";", " ", commentstm$message)
commentstm$message <- gsub("\"", " ", commentstm$message)


write.table(commentstm, "commentsTM_clean.csv", row.names = F, sep = ";", fileEncoding = "UTF-8")



commentsvf <- read.csv("commentsVF.csv")

head(commentsvf)

commentsvf$message <- gsub("\n", " ", commentsvf$message)
commentsvf$message <- gsub("\t", " ", commentsvf$message)
commentsvf$message <- gsub(";", " ", commentsvf$message)
commentsvf$message <- gsub("\"", " ", commentsvf$message)


write.table(commentsvf, "commentsVF_clean.csv", row.names = F, sep = ";", fileEncoding = "UTF-8")
