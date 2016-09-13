require(XML)
require(magrittr)
require(rvest)
require(gsubfn)


months_names <- format(ISOdatetime(2000,1:12,1,0,0,0),"%b")
startYear <- function(){
   sy <- readline(prompt = "Enter starting year as integer (YYYY):")
   return(as.integer(sy))
}
   
endYear <- function(){
   ey <- readline(prompt = "Enter ending year as integer (YYYY):")
   return(as.integer(ey))
}

years <- c(startYear():endYear())

startMonth<-function(){
   sm <- readline(prompt = "Enter month number of starting month (range 1 to 12):")
   return(as.integer(sm))
}


endMonth<-function(){
   em <- readline(prompt = "Enter month number of ending month (range 1 to 12):")
   return(as.integer(em))
}

months<-c(startMonth():endMonth())
# Set up the URL
url<- "http://seclists.org/fulldisclosure/"

## Extract table that provides information about number of iterations to be performed every month

tab <- readHTMLTable(url, stringsAsFactors = F, colClasses = "numeric")[4]
tab <- data.frame(tab)
row.names(tab)<- tab[,1]
tab <- tab[,-1]
names(tab)<- c(months_names)


#  years loop
#for (i in 1:length(years)){
   
for (i in years){
      
   # Months loop
   #for(j in 1:length(months_names)){
    for(j in months){
      flag=0;
      # Number of cases in each month saved in iteration variable
      iterations <- tab[as.character(i), months_names[j]]
      if(is.na(iterations)){
         next
      }
      
      # Extract individual cases
      for(k in 0:(iterations-1)){
      #for(k in 75:76){
         tryCatch(   
         doc <- read_html(paste0("http://seclists.org/fulldisclosure/", as.character(i), "/", months_names[j],"/", as.character(k))),
         error = function(e){NA}
         
         )
         Sys.sleep(2*runif(1))
         
         text_body <- doc %>% html_nodes(xpath = "/html/body/table[2]//tr[1]/td[2]/table//tr/td//pre |/html/body/table[2]//tr[1]/td[2]/table//tr/td/tt") %>% html_text(trim= T) %>% paste(collapse = '') 
         
         text_body <- gsub('[\n|+]',' ', text_body) 
         
         write(text_body[1], file = paste0(i, "_", months_names[j],"_", k, ".txt"))
         
         
         #Email title
         title <- doc %>% html_node(xpath = "/html/body/table[2]//tr[1]/td[2]/table//tr/td/font[1]/b") %>% html_text 
         
         # Email Author
         author <- doc %>% html_node(xpath = "/html/body/table[2]//tr[1]/td[2]/table//tr/td/text()[6]") %>% html_text %>% strapplyc(": (.*)", simplify = T)
         
         # Email time stamp
         dateStamp <- doc %>% html_node(xpath = "/html/body/table[2]//tr[1]/td[2]/table//tr/td/text()[7]") %>% html_text %>% strapplyc(": (.*)", simplify = T)
         
         
         
         if(is.na(title)){
            next
         }
         
         # Data form one iteration
         entry = data.frame(i,months_names[j],k,title,author,dateStamp)
         Sys.sleep(3*runif(1))
         if(k %% 25 == 0){
            Sys.sleep(3*runif(1))
            Sys.sleep(1*runif(1))
         }
         
         if(flag == 0){
            mail_table = entry
            flag = 1
         }else{
            # Merged data from all iterations
            mail_table <- rbind(mail_table,entry) 
         }
         
         #Introduced to produce a delay - so that our IP isn't blocked
         Sys.sleep(0.5)
         Sys.sleep(2*runif(1))
         }
      write.csv(mail_table, file = paste0("Full_Disclosure_Mailing_List_", months_names[j],i, ".csv"))
      Sys.sleep(5)
   }
   
}

