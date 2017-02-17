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

merge_data <- function(year){
   
csv_file_list1 <- list.files(path =file.path(paste0("./body_corpus"), paste0(year)), pattern = "*.csv", full.names = T)

datalist = lapply(csv_file_list1, FUN = "read.csv", header = T, stringsAsFactors = F)

merged.data = Reduce(function(...) rbind(...), datalist)
merged.data<- merged.data[,-1]

merged.data$document_ID <- paste(merged.data$years.i., merged.data$months_names.j., merged.data$k, sep = "_") 
merged.data$document_url <- paste("http://seclists.org/fulldisclosure", merged.data$years.i., merged.data$months_names.j., merged.data$k, sep = "/")

merged.data[,2] <- factor(merged.data[,2], levels = months_names, ordered = 1)

merged.data <- merged.data[order(merged.data$months_names.j.,merged.data$k),]

#merged.data$email <- unlist(strapplyc(merged.data$author, "<(.*)>")

#merged.data$author <- gsubfn("<.*>", "", merged.data$author)
merged.data$author<- gsubfn("\"","", merged.data$author)
merged.data<- merged.data[,c("document_ID", "title", "author", "dateStamp","document_url" ,"months_names.j." ,"k")]

for(i in 1:nrow(merged.data)){
   merged.data$documentWeight[i] <- sum(gsub(".*Re: ","",merged.data$title) == paste0(merged.data$title[i]))
}

for(i in 1:nrow(merged.data)){
   repeated_emails <- subset(merged.data, gsub(".*Re: ","",merged.data$title) == paste0(gsub(".*Re: ","",merged.data$title[i])))
   merged.data$parentDocument_ID[i] <- repeated_emails$document_ID[repeated_emails$k == min(repeated_emails$k)]
   merged.data$threadAuthor[i]<- repeated_emails$author[repeated_emails$k == min(repeated_emails$k)]
   merged.data$parentTitle[i]<- repeated_emails$title[repeated_emails$k == min(repeated_emails$k)]
   merged.data$listOfReplys[i]<- paste(repeated_emails$document_ID[repeated_emails$documentWeight == 0], collapse = ",")
   merged.data$contributingAuthors[i]<- paste(merged.data$threadAuthor[i], unique(repeated_emails$author[repeated_emails$documentWeight == 0 & repeated_emails$author != repeated_emails$threadAuthor]), collapse = ",", sep = ",")
   merged.data$authorCount[i]<- length(unique(repeated_emails$author[repeated_emails$documentWeight == 0 & repeated_emails$author != repeated_emails$threadAuthor])) + 1
}

return(merged.data)
}


seeded_data <- function(data){
   csv_file_list2 <- list.files(path = file.path(paste0("./edited_edgelists")), pattern = paste0(year,"_edgelist.csv"), full.names = T)
   
   seed_file<-read.csv(csv_file_list2, stringsAsFactors = F)
   names(seed_file)<-c("noun", "document_ID")
   
   return(seed_file)
}


edge_data <- function(gephi_data){
   
   edgelist <- data.frame(count(gephi_data, vars = c("parentDocument_ID","noun", "parentTitle")))
   names(edgelist)<-c("Source","Target", "parentTitle","Weight")
   edgelist$color <- "yellow"
   edgelist<- edgelist[edgelist$Target != " ",]
   return(edgelist)
}


node_data<- function(gephi_data){
   nodelist <- data.frame(count(gephi_data, vars = c("parentDocument_ID", "parentTitle","threadAuthor","listOfReplys","contributingAuthors","authorCount","documentWeight")))
   nodelist<- nodelist[nodelist$documentWeight!= 0,-ncol(nodelist)]
   seedNodes <- data.frame(count(gephi_data, vars = c("noun","parentDocument_ID", "parentTitle")))
   #nodelist <- rbind.data.frame(count(gephi_data, vars = c("noun", "seedOccurance")))
   names(nodelist)<- c("Id","Label","threadAuthor","List_of_Reply_Ids","contributingAuthors","authorCount","Weight")
   nodelist$Weight<- nodelist$Weight - 1
   
   nodelist<- nodelist[order(nodelist$Weight,nodelist$authorCount, decreasing = T),]
   
   for (l in 1:nrow(nodelist)) {
      nodelist$documentURL[l] <- gephi_data$document_url[nodelist$Id[l] == gephi_data$document_ID][1]  
   }
   return(nodelist)
}


for(year in 2002:2016){
data <- merge_data(year)
write.csv(data, file = paste0("author_document_data_",year,".csv"), row.names = F)

seed_file<- seeded_data(data)
write.csv(seed_file, file = paste0("document_seed_data_",year,".csv"), row.names = F)


gephi_data <- merge(x= data, y = seed_file, by="document_ID", all.y = TRUE, sort = TRUE)
gephi_data<- gephi_data[order(-gephi_data$documentWeight,gephi_data$months_names.j.,gephi_data$k),]
gephi_data$color <- "blue"
write.csv(gephi_data, file = paste0("gephi_data_",year,".csv"), row.names = FALSE)


nodelist <- node_data(gephi_data)
write.csv(nodelist, file = paste0("nodelist",year,".csv"), row.names = FALSE)

edgelist <- edge_data(gephi_data)
write.csv(edgelist, file = paste0("edgelist", year,".csv"), row.names = FALSE)

Author_Document_data <- nodelist
names(Author_Document_data)<- c("threadtId", "threadTitle", "threadAuthor", "reply_IDs","contributingAuthors","nAuthors","nReplys", "threadURL")
write.csv(Author_Document_data, file = paste0("FD_Threads",year,".csv"), row.names = F)
}
