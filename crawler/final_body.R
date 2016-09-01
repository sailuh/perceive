require(XML)
require(magrittr) # For writing pipeline commands
require(rvest) # For web scraping
require(gsubfn) #For string manipulation

# For creating the month's variable in the format
months_names <- format(ISOdatetime(2000,1:12,1,0,0,0),"%b")
years <- c(2002:2016)

# Set up the URL
url<- "http://seclists.org/fulldisclosure/"

## Extract table that provides information about number of iterations to be performed every month

tab <- readHTMLTable(url, stringsAsFactors = F, colClasses = "numeric")[4]
tab <- data.frame(tab)
row.names(tab)<- tab[,1]
tab <- tab[,-1]
names(tab)<- c(months_names)


#default years loop - covers all 15 years
#for (i in 1:length(years)){
  
#customized year loop: type in year number from starting from 2002    
for (i in 1:5){
      
   #Default  Months loop covers all 12 months in that year
   #for(j in 1:length(months_names)){
   
   # customized months loop eg: for jan to june input month numbers 1 to 6
   for(j in 1:6){
      flag=0;
      # Number of cases in each month saved in iteration variable
      iterations <- tab[as.character(years[i]), months_names[j]]
      if(is.na(iterations)){
         next
      }
      
      # Extract individual cases
      for(k in 0:(iterations-1)){
      #for(k in 75:80){
         tryCatch(   
         doc <- read_html(paste0("http://seclists.org/fulldisclosure/", as.character(years[i]), "/", months_names[j],"/", as.character(k))),
         error = function(e){NA}
         
         )
         Sys.sleep(2*runif(1))
         
         text_body <- doc %>% html_nodes(xpath = "/html/body/table[2]//tr[1]/td[2]/table//tr/td//pre |/html/body/table[2]//tr[1]/td[2]/table//tr/td/tt") %>% html_text(trim= T) %>% paste(collapse = '') 
         
         text_body <- gsub('[\n|+]',' ', text_body) 
         
         write(text_body[1], file = paste0(years[i], "_", months_names[j],"_", k, ".txt"))
         
         
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
         entry = data.frame(years[i],months_names[j],k,title,author,dateStamp)
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
      write.csv(mail_table, file = paste0("Full_Disclosure_Mailing_List_", months_names[j],years[i], ".csv"))
      Sys.sleep(5)
   }
   
}

