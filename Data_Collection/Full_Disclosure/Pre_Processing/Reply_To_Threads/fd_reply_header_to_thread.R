#!/usr/bin/Rscript
library(plyr)
library(gsubfn)

## Collect arguments
args <- commandArgs(TRUE)

## Extract args
if(length(args) != 2) {
  print("Rscript <folder filepath containing reply headers .csv from fd_crawler.R> <output file path>")
  quit()
}

inputfolderpath <- args[1]
outputfilepath <- args[2]

#Load the list of replies header (.csv of every month) and merge in a single file. 
replies.header.filepaths <- list.files(inputfolderpath, pattern = "*.csv", full.names = T)
replies.header.list <- lapply(replies.header.filepaths, FUN = "read.csv", header = T, stringsAsFactors = F)
replies.header <- Reduce(function(...) rbind(...), replies.header.list)

replies.header$reply_id <- paste(replies.header$year, replies.header$month, replies.header$reply_month_id, sep = "_") 
replies.header$reply_url <- paste("http://seclists.org/fulldisclosure", replies.header$year, replies.header$month, replies.header$reply_month_id, sep = "/")

#order by month, and reply id 
replies.header <- replies.header[order(replies.header$month,replies.header$reply_month_id),]

#Extract author and remove double quotes from the author string
replies.header$author<- gsubfn("\"","", replies.header$author)

#shuffle columns for readability purposes.
replies.header<- replies.header[,c("reply_id", "title", "author", "timestamp","reply_url" ,"month" ,"reply_month_id")]

#Output of the For Loop: The number of replies of the given e-mail thread. If lone thread, it will be 0. 
#
#For every row in merged data (loop), it removes repetitions of 0 or more 'Re:' of the ENTIRE row, and then compares
#it against the current value, string-wise. The resulting operation is a vector of FALSE/TRUE for the size of the entire row.
#This loop is extremely inneficient, it cleans the vector nrow times instead of being reused after applied once!
#The end result of this loop is a new column that indicates the number of times the same e-mail title was repeated, or 
#the number of replies of that e-mail thread. 
for(i in 1:nrow(replies.header)){
  replies.header$thread_n_replies[i] <- sum( gsub(".*Re: ","",replies.header$title) == paste0(replies.header$title[i]) )
}

for(i in 1:nrow(replies.header)){
  
  #another expensive vector operation for every row. for every row this results in a vector of TRUE/FALSE of the row positions with same e-mail thread.
  #the rows are then retrieved on the repeated_replies variable..
  repeated_replies <- subset(replies.header, gsub(".*Re: ","",replies.header$title) == paste0(gsub(".*Re: ","",replies.header$title[i])))
  replies.header$thread_id[i] <- repeated_replies$reply_id[repeated_replies$reply_month_id == min(repeated_replies$reply_month_id)]
  
  #the minimum reply id of the set of e-mail replies in that position is stored.. so basically in a subset of 5 e-mail replies, it will overwrite with the minimum on all the rows rather than remove them already from the vector.... Could have reused the index from above as well at least when getting the min()..
  replies.header$thread_author[i]<- repeated_replies$author[repeated_replies$reply_month_id == min(repeated_replies$reply_month_id)]
  
  #same logic as above to extract the title.. could have at least reused the index from above instead of recalculating it here..
  replies.header$thread_title[i]<- repeated_replies$title[repeated_replies$reply_month_id == min(repeated_replies$reply_month_id)]
  
  #here the vector is flattened out as a string, which will contain the list of all the e-mail ids that were repeated (e.g. 2016_May_36,2016_May_37,2016_May_48,2016_May_54" )
  replies.header$thread_reply_ids[i]<- paste(repeated_replies$reply_id[repeated_replies$thread_n_replies == 0], collapse = ",")
  
  #This is a flattened out as a string, which will contain the list of all authors. Not sure how yet.
  replies.header$thread_reply_authors[i]<- paste(replies.header$thread_author[i], unique(repeated_replies$author[repeated_replies$thread_n_replies == 0 & repeated_replies$author != repeated_replies$thread_author]), collapse = ",", sep = ",")
  
  #Supposedly this line tells you the number of authors for the e-mail thread. Not sure how yet. 
  replies.header$thread_n_authors[i]<- length(unique(repeated_replies$author[repeated_replies$thread_n_replies == 0 & repeated_replies$author != repeated_replies$thread_author])) + 1
}

write.csv(replies.header, file = file.path(outputfilepath,"threads_header.csv"), row.names = F)
