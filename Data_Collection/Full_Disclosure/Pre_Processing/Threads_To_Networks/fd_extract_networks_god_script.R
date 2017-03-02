library(plyr)
library(gsubfn)


for(year in 2002:2016){

#Load data files
datalist <- read.csv(file = paste0("./author_document_data_", year,".csv"), header = T, stringsAsFactors = F)
wordlist <- read.csv(file = paste0("./document_seed_data_", year,".csv"), header = T, stringsAsFactors = F, strip.white = T)
wordlist <- wordlist[wordlist$noun != " ",]

nodeseeds <- data.frame(unique(wordlist$noun), stringsAsFactors = F)
nodeseeds$Label <- nodeseeds[,1]
nodeseeds[,"Label1"] <- NA
nodeseeds[,"Label2"] <- NA
# nodeseeds[,"Label4"] <- NA
# nodeseeds[,"Label5"] <- NA
nodeseeds[,"Color"] <- "#0000FF"
nodeseeds[,"nodeType"] <- "seed"
names(nodeseeds)[1] <- "Id"

nodeauthors <- data.frame(unique(datalist$author), stringsAsFactors = F)
nodeauthors$Label <- nodeauthors[,1]
nodeauthors[,"Label1"] <- NA
nodeauthors[,"Label2"] <- NA
# nodeauthors[,"Label4"] <- NA
# nodeauthors[,"Label5"] <- NA
nodeauthors[,"Color"] <- "#FF0000"
names(nodeauthors)[1] <- "Id"
nodeauthors[,"nodeType"] <- "author"

nodedocs <- data.frame(unique(datalist$parentDocument_ID), stringsAsFactors = F)
names(nodedocs)[1] <- "Id"

for (i in 1:nrow(nodedocs)){
   nodedocs$Label[i] <- datalist$parentTitle[datalist$document_ID == nodedocs$Id[i]][1]
   nodedocs$Label1[i] <- datalist$listOfReplys[datalist$document_ID == nodedocs$Id[i]][1]
   nodedocs$Label2[i] <- paste0("http://seclists.org/fulldisclosure/", gsubfn("_","/",nodedocs$Id[i]))
}
nodedocs[,"Color"] <- "#000000"
nodedocs[,"nodeType"] <- "document"


nodelist <- nodeseeds
nodelist <- rbind(nodelist, nodeauthors)
nodelist <- rbind(nodelist, nodedocs)
write.csv(nodelist, file = paste0("nodelist_", year, ".csv"), row.names = F)

nodelist_doc_seed <- nodeseeds
nodelist_doc_seed <- rbind(nodelist_doc_seed, nodedocs)
write.csv(nodelist_doc_seed, file = paste0("nodelist_doc_seed_", year, ".csv"), row.names = F)

nodelist_aut_doc <- nodeauthors
nodelist_aut_doc <- rbind(nodelist_aut_doc, nodedocs)
write.csv(nodelist_aut_doc, file = paste0("nodelist_aut_doc_", year, ".csv"), row.names = F)


author_threadID <- data.frame(datalist$author, datalist$parentDocument_ID, stringsAsFactors = F)
names(author_threadID) <- c("author", "threadID")
author_threadID_edgelist <- data.frame(count(author_threadID, vars = c("author","threadID")), stringsAsFactors = F)
names(author_threadID_edgelist)[3] <- "nReplies_in_thread"
names(author_threadID_edgelist) <- c("Source","Target","Weight")
write.csv(author_threadID_edgelist, file = paste0("author_threadID_edgelist_",year,".csv"), row.names = F)

threadID_seed <- data.frame(wordlist$document_ID, wordlist$noun, stringsAsFactors = F)
names(threadID_seed) <- c("document_ID","seed")
for(i in 1:nrow(threadID_seed)){
   threadID_seed$thread_ID[i] <- datalist$parentDocument_ID[datalist$document_ID == threadID_seed$document_ID[i]]
}
threadID_seed <- threadID_seed[threadID_seed$thread_ID != " ",]

threadID_seed_edgelist <-data.frame(count(threadID_seed, vars = c("thread_ID", "seed")))
names(threadID_seed_edgelist)[3]<- "nSeedOccurance_in_thread"
names(threadID_seed_edgelist) <- c("Source", "Target","Weight")
write.csv(threadID_seed_edgelist, file = paste0("threadID_seed_edgelist_",year,".csv"), row.names = F)

edgelist <- threadID_seed_edgelist
edgelist <- rbind(edgelist, author_threadID_edgelist)
write.csv(edgelist, file = paste0("edgelist_", year, ".csv"), row.names = F)
}
