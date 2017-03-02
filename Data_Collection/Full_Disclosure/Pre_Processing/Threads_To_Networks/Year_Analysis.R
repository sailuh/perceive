library(plyr)

#years = c(2002:2)

years1 =c(2002:2015)
years2=c(2003:2016)
months_names <- format(ISOdatetime(2000,1:12,1,0,0,0),"%b")
for (i in 1:length(years1)){

csv_file_list1 <- list.files(path = normalizePath(file.path("body_corpus", paste0(years1[i]))), pattern = "*.csv", full.names = T)

datalist1 = lapply(csv_file_list1, FUN = "read.csv", header = T, stringsAsFactors = F)
for(j in 1:length(datalist1)){
   names(datalist1[[j]])<- c("X", "years.i.", "months_names.j.","k","title","author","dateStamp")
}
   
merged.data_1 = Reduce(function(...) rbind(...), datalist1)
merged.data_1<- merged.data_1[,-1]

merged.data_1[,2] <- factor(merged.data_1[,2], levels = months_names, ordered = 1)
merged.data_1 <- merged.data_1[order(merged.data_1$months_names.j.,merged.data_1$k),]

unique_titles_1 <- as.data.frame(table(merged.data_1$title))
unique_titles_1 <- unique_titles_1[order(-unique_titles_1$Freq),]
names(unique_titles_1)[1]<-"title"

unique_authors_1 <- as.data.frame(table(merged.data_1$author))
unique_authors_1 <- unique_authors_1[order(-unique_authors_1$Freq),]
names(unique_authors_1)[1] <- "author_name"

write.csv(unique_titles_1, file =paste0("Unique_Titles",years1[i],".csv") , row.names = F)
write.csv(unique_authors_1, file =paste0("Unique_Authors",years1[i],".csv"), row.names = F)

csv_file_list2 <- list.files(path = normalizePath(file.path("body_corpus", paste0(years2[i]))), pattern = "*.csv", full.names = T)
datalist2 = lapply(csv_file_list2, FUN = "read.csv", header = T, stringsAsFactors = F)

for(j in 1:length(datalist2)){
   names(datalist2[[j]])<- c("X", "years.i.", "months_names.j.","k","title","author","dateStamp")
}


merged.data_2 = Reduce(function(...) rbind(...), datalist2)
merged.data_2<- merged.data_2[,-1]

merged.data_2[,2] <- factor(merged.data_2[,2], levels = months_names, ordered = 1)
merged.data_2 <- merged.data_2[order(merged.data_2$months_names.j.,merged.data_2$k),]

unique_titles_2 <- as.data.frame(table(merged.data_2$title))
unique_titles_2 <- unique_titles_2[order(-unique_titles_2$Freq),]
names(unique_titles_2)[1]<-"title"

unique_authors_2 <- as.data.frame(table(merged.data_2$author))
unique_authors_2 <- unique_authors_2[order(-unique_authors_2$Freq),]
names(unique_authors_2)[1] <- "author_name"

write.csv(unique_titles_2, paste0(file = "Unique_Titles_",years2[i],".csv"), row.names = F)
write.csv(unique_authors_2,paste0(file = "Unique_Authors_",years2[i],".csv"), row.names = F)

merged.data_1_2 <- rbind(merged.data_1, merged.data_2)
write.csv(merged.data_1_2,paste0(file = "",years1[i],"_",years2[i],".csv"), row.names = F)

common_titles_1_2 <- Reduce(intersect, list(unique_titles_1$title, unique_titles_2$title))
common_authors_1_2 <- Reduce(intersect, list(unique_authors_1$author_name, unique_authors_2$author_name))

write.csv(common_authors_1_2,file = paste0("Common_Authors_",years1[i],"_",years2[i],".csv"), row.names = F)
write.csv(common_titles_1_2, file = paste0("Common_Titles_",years1[i],"_",years2[i],".csv"), row.names = F)
}
