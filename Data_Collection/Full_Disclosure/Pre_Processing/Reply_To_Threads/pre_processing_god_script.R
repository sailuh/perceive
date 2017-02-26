library(plyr)
library(gsubfn)


months_names <- format(ISOdatetime(2000,1:12,1,0,0,0),"%b")

# Please uncomment the below lines incase you want the script to run on a per year basis

# readYear <- function()
# {
#    year <- readline(prompt = "Enter the year for analysis: ")
#    return(as.integer(year))
# }
# 
# year <- readYear()
# print(paste0("The year to be analyzed is ", year))
# 

group_replies_by_thread <- function(year){

  #Load the list of replies header (.csv of every month) and merge in a single file. 
  replies.header.filepaths <- list.files(path =file.path(paste0("./body_corpus"), paste0(year)), pattern = "*.csv", full.names = T)
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
  return(replies.header)
}


seeded_data <- function(data){
   csv_file_list2 <- list.files(path = file.path(paste0("./edited_edgelists")), pattern = paste0(year,"_edgelist.csv"), full.names = T)
   
   seed_file<-read.csv(csv_file_list2, stringsAsFactors = F)
   names(seed_file)<-c("noun", "reply_id")
   
   return(seed_file)
}


edge_data <- function(gephi_data){
   edgelist <- data.frame(count(gephi_data, vars = c("thread_id","noun", "thread_title")))
   names(edgelist)<-c("Source","Target", "thread_title","Weight")
   edgelist$color <- "yellow"
   edgelist<- edgelist[edgelist$Target != " ",]
   return(edgelist)
}


node_data<- function(gephi_data){
   nodelist <- data.frame(count(gephi_data, vars = c("thread_id", "thread_title","thread_author","thread_reply_ids","thread_reply_authors","thread_n_authors","thread_n_replies")))
   nodelist<- nodelist[nodelist$thread_n_replies!= 0,-ncol(nodelist)]
   seedNodes <- data.frame(count(gephi_data, vars = c("noun","thread_id", "thread_title")))
   #nodelist <- rbind.data.frame(count(gephi_data, vars = c("noun", "seedOccurance")))
   names(nodelist)<- c("Id","Label","thread_author","List_of_Reply_Ids","thread_reply_authors","thread_n_authors","Weight")
   nodelist$Weight<- nodelist$Weight - 1
   
   nodelist<- nodelist[order(nodelist$Weight,nodelist$thread_n_authors, decreasing = T),]
   
   for (l in 1:nrow(nodelist)) {
      nodelist$documentURL[l] <- gephi_data$document_url[nodelist$Id[l] == gephi_data$reply_id][1]  
   }
   return(nodelist)
}


for(year in 2002:2016){
  data <- group_replies_by_thread(year)
  write.csv(data, file = paste0("author_document_data_",year,".csv"), row.names = F)

  seed_file<- seeded_data(data)
  write.csv(seed_file, file = paste0("document_seed_data_",year,".csv"), row.names = F)


  gephi_data <- merge(x= data, y = seed_file, by="reply_id", all.y = TRUE, sort = TRUE)
  gephi_data<- gephi_data[order(-gephi_data$thread_n_replies,gephi_data$months_names.j.,gephi_data$reply_month_id),]
  gephi_data$color <- "blue"
  write.csv(gephi_data, file = paste0("gephi_data_",year,".csv"), row.names = FALSE)


  nodelist <- node_data(gephi_data)
  write.csv(nodelist, file = paste0("nodelist",year,".csv"), row.names = FALSE)

  edgelist <- edge_data(gephi_data)
  write.csv(edgelist, file = paste0("edgelist", year,".csv"), row.names = FALSE)

  Author_Document_data <- nodelist
  names(Author_Document_data)<- c("threadtId", "threadTitle", "thread_author", "reply_IDs","thread_reply_authors","nAuthors","nReplys", "threadURL")
  write.csv(Author_Document_data, file = paste0("FD_Threads",year,".csv"), row.names = F)
}