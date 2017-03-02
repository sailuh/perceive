#!/usr/bin/Rscript
library(plyr)
library(gsubfn)

## Collect arguments
args <- commandArgs(TRUE)

## Extract args
if(length(args) != 2) {
  print("Rscript <threads_header.csv from fd_reply_header_to_thread.R> <output folder path>")
  quit()
}
threads.header.filepath <- args[1]
node_and_edgelist.folderpath <- args[2]

threads.header <- read.csv(file = file.path(threads.header.filepath), header = T, stringsAsFactors = F)

#############################
####### NODE TABLE ##########
#############################

#Unique Thread Authors Nodes and Node Labels (color, and node type for Gephi)
nodeauthors <- data.frame(unique(threads.header$author), stringsAsFactors = F)
nodeauthors$Label <- nodeauthors[,1]
nodeauthors[,"Label1"] <- NA
nodeauthors[,"Label2"] <- NA
nodeauthors[,"Color"] <- "#FF0000"
names(nodeauthors)[1] <- "Id"
nodeauthors[,"node_type"] <- "author"

#Unique Thread IDs Nodes and Node Labels (color, and node type for Gephi)
  # Label: Thread ID
  # Label 1: All Replies of the Thread ID
  # Label 2: Easy Access URL for Full Disclosure Mailing List Inspection
nodethreads <- data.frame(unique(threads.header$thread_id), stringsAsFactors = F)
names(nodethreads)[1] <- "Id"
for (i in 1:nrow(nodethreads)){
  nodethreads$Label[i] <- threads.header$reply_id[threads.header$reply_id == nodethreads$Id[i]][1]
  nodethreads$Label1[i] <- threads.header$thread_reply_ids[threads.header$reply_id == nodethreads$Id[i]][1]
  nodethreads$Label2[i] <- paste0("http://seclists.org/fulldisclosure/", gsubfn("_","/",nodethreads$Id[i]))
}
nodethreads[,"Color"] <- "#000000"
nodethreads[,"node_type"] <- "reply"

#Creates Gephi Nodes Table by combining the author and thread nodes into one.
nodelist <- rbind(nodeauthors, nodethreads)
write.csv(nodelist, file = file.path(node_and_edgelist.folderpath,"nodelist_author_thread.csv"), row.names = F)

#############################
####### EDGE TABLE ##########
#############################

author_threadID <- data.frame(threads.header$author, threads.header$thread_id, stringsAsFactors = F)
names(author_threadID) <- c("author", "thread_id")
author_threadID_edgelist <- data.frame(count(author_threadID, vars = c("author","thread_id")), stringsAsFactors = F)
names(author_threadID_edgelist)[3] <- "thread_n_replies"
names(author_threadID_edgelist) <- c("Source","Target","Weight")

edgelist <- author_threadID_edgelist
write.csv(edgelist, file = file.path(node_and_edgelist.folderpath,"edgelist_author_thread.csv"), row.names = F)