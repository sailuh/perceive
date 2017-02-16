# Load required packages
library(rvest)
library(magrittr)
library(gsubfn)

#Load XML file that contains CAPEC data
doc <- read_xml("capec_v2.8.xml")

Nodes <- doc %>% xml_nodes(xpath ="//*/capec:Attack_Pattern")

ID <- Nodes %>% xml_find_all("./@ID") %>% xml_text(trim=T)

Name <- Nodes %>% xml_find_all("./@Name") %>% xml_text(trim = T)

Summary <- Nodes %>% xml_find_first(".//capec:Description/capec:Summary") %>% xml_text(trim=T)

Typical_Severity <- Nodes %>% xml_find_first("capec:Typical_Severity") %>% xml_text(trim = T)

Typical_Likelihood_of_Exploit <- Nodes %>% xml_find_first("capec:Typical_Likelihood_of_Exploit") %>% xml_text(trim = T)

Attack_Prerequisite <- Nodes %>% xml_find_first("capec:Attack_Prerequisites") %>% xml_text(trim = T)

Submitter <- Nodes %>% xml_find_first(".//capec:Submitter") %>% xml_text

Submission_Source <- Nodes %>% xml_find_first(".//capec:Submission/@Submission_Source") %>% xml_text

Date <- Nodes %>% xml_find_first(".//capec:Submission_Date") %>% xml_text


#Extracting variables that may contain null values

Relationship <- vector()
Methods_of_Attack <- vector()
Related_Weaknesses_CWE_ID <- vector()
Related_Attack_Pattern <- vector()

for (i in 1:length(Nodes)){
   
   Methods_of_Attack[i] <- paste(Nodes[i] %>% xml_find_all("capec:Methods_of_Attack/capec:Method_of_Attack") %>% xml_text(trim = T), collapse = ", ")
      
   Related_Weaknesses_CWE_ID[i] <- paste(Nodes[i] %>% xml_find_all("capec:Related_Weaknesses/capec:Related_Weakness/capec:CWE_ID") %>% xml_text(trim = T), collapse = ", ")
   
   Related_Attack_Pattern[i] <- paste(Nodes[i] %>% xml_find_all("capec:Related_Attack_Patterns/capec:Related_Attack_Pattern/capec:Relationship_Nature") %>% xml_text(trim = T),Nodes[i] %>% xml_find_all("capec:Related_Attack_Patterns/capec:Related_Attack_Pattern/capec:Relationship_Target_ID") %>% xml_text(trim = T),sep = " - ", collapse = ", ")
   
}

Attack_Pattern_Data <- data.frame(ID,Name,Summary,Typical_Severity,Typical_Likelihood_of_Exploit,Attack_Prerequisite, Methods_of_Attack, Related_Weaknesses_CWE_ID, Related_Attack_Pattern ,Submitter,Submission_Source, Date,stringsAsFactors = F)

Attack_Pattern_Data$ID <- as.numeric(Attack_Pattern_Data$ID)

Attack_Pattern_Data<- Attack_Pattern_Data[order(Attack_Pattern_Data$ID, decreasing = F),]

write.csv(Attack_Pattern_Data, file = "CAPEC_Attack_Pattern_Data.csv", row.names = F)

#Creating Node and Edge tables

CAPEC_Nodelist <- data.frame(ID = Attack_Pattern_Data$ID, Label = Attack_Pattern_Data$Name, Attack_Pattern_Data$Summary, Attack_Pattern_Data$Methods_of_Attack, Attack_Pattern_Data$Related_Weaknesses_CWE_ID, stringsAsFactors = F)

Relations_list <- strsplit(as.character(Attack_Pattern_Data$Related_Attack_Pattern), ",")

CAPEC_Edgelist <- data.frame(Target = unlist(Relations_list), Source = rep(Attack_Pattern_Data$ID, sapply(Relations_list, FUN = length)), stringsAsFactors = F)
CAPEC_Edgelist$Relationship <- strapplyc(CAPEC_Edgelist$Target, "(.*) -",simplify = T)
CAPEC_Edgelist$Target <- strapplyc(CAPEC_Edgelist$Target, "- (.*)", simplify = T)
CAPEC_Edgelist$Relationship <- trimws(CAPEC_Edgelist$Relationship, which = "b")
CAPEC_Edgelist$Target <- as.numeric(CAPEC_Edgelist$Target)
CAPEC_Edgelist$Source <- as.numeric(CAPEC_Edgelist$Source)
CAPEC_Edgelist$Relationship <- as.factor(CAPEC_Edgelist$Relationship)

write.csv(CAPEC_Nodelist, file = "CAPEC_Nodelist.csv", row.names = F)
write.csv(CAPEC_Edgelist, file = "CAPEC_Edgelist.csv")
