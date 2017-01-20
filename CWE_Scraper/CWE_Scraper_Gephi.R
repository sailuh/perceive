#load required packages
library(rvest)
library(magrittr)
library(gsubfn)

#Load downloaded XML file with CWE data

doc <- read_xml("cwec_v2.9.xml")

#Extract the required fields from the XML document

Nodes <- doc %>% xml_nodes(xpath ="//*/Weakness")

ID <- Nodes %>% xml_find_all("./@ID") %>% xml_text(trim=T)
   
Name <- Nodes %>% xml_find_all("./@Name") %>% xml_text(trim = T)
   
Description_Summary <- Nodes %>% xml_find_all(".//Description_Summary") %>% xml_text(trim=T)

Extended_Description <- Nodes %>% xml_find_first(".//Extended_Description")%>% xml_text(trim = T)
   
Causal_Nature <- Nodes %>% xml_find_first("./Causal_Nature") %>% xml_text(trim = T)
   
Submitter <- Nodes %>% xml_find_first(".//Submitter") %>% xml_text
   
Submission_Source <- Nodes %>% xml_find_first(".//Submission/@Submission_Source") %>% xml_text
   
   
   Weakness_Relationship <- vector()
   Category_Relationship <- vector()
   Time_of_Introduction <- vector()
   Taxonomy_Mapping <- vector()
   Taxonomy <- vector()
   Mapping <- vector()
   CAPEC_ID_for_Related_Attacks <- vector()

#Below technique is used to ectract data that may contain empty values

for (i in 1:length(Nodes)){   
    
    Weakness_Relationship[i] <- paste(Nodes[i] %>% xml_find_all(".//Relationship[./Relationship_Target_Form/text()='Weakness']/Relationship_Nature") %>% xml_text(trim=T),Nodes[i] %>% xml_find_all(".//Relationship[./Relationship_Target_Form/text()='Weakness']/Relationship_Target_ID") %>% xml_text(trim=T), sep = " - ", collapse = ", ")
    
    Category_Relationship[i] <- paste(Nodes[i] %>% xml_find_all(".//Relationship[./Relationship_Target_Form/text()='Category']/Relationship_Nature") %>% xml_text(trim=T),Nodes[i] %>% xml_find_all(".//Relationship[./Relationship_Target_Form/text()='Category']/Relationship_Target_ID") %>% xml_text(trim=T), sep = " - ", collapse = ", ")
    
    
    Time_of_Introduction[i] <- paste(Nodes[i] %>% xml_find_all(".//Time_of_Introduction/Introductory_Phase") %>% xml_text(trim =T), collapse = ", ")
    
    Taxonomy_Mapping[i] <- paste(Nodes[i] %>% xml_find_all(".//Taxonomy_Mapping/@Mapped_Taxonomy_Name") %>% xml_text(),Nodes[i] %>% xml_find_all(".//Mapped_Node_Name") %>% xml_text(), sep = " - " ,collapse = ", ")
    
   Taxonomy[i]<- Nodes[i] %>% xml_find_first(".//Taxonomy_Mapping//@Mapped_Taxonomy_Name") %>% xml_text()
    
   Mapping[i] <- Nodes[i] %>% xml_find_first(".//Mapped_Node_Name") %>% xml_text()
    
    CAPEC_ID_for_Related_Attacks[i] <- paste(Nodes[i] %>% xml_find_all(".//CAPEC_ID") %>% xml_text, collapse = ", ")
}
   
Weakness_Data <- data.frame(ID,Name,Description_Summary,Extended_Description,Time_of_Introduction,Weakness_Relationship,Category_Relationship, Taxonomy_Mapping,Taxonomy,Mapping, CAPEC_ID_for_Related_Attacks, Submitter, Submission_Source, stringsAsFactors = F)

Weakness_Data$ID <- as.numeric(Weakness_Data$ID)

Weakness_Data<- Weakness_Data[order(Weakness_Data$ID, decreasing = F),]

write.csv(Weakness_Data, file = "CWE_Weakness_Data.csv", row.names = F)


# Creating edge and nodelists

CWE_Nodelist <- data.frame(ID = Weakness_Data$ID, Label = Weakness_Data$Name, Weakness_Data$Description_Summary,Weakness_Data$CAPEC_ID_for_Related_Attacks, stringsAsFactors = F)


Relations_list <- strsplit(as.character(Weakness_Data$Weakness_Relationship),",")

CWE_Edgelist <- data.frame(Target = unlist(Relations_list), Source = rep(Weakness_Data$ID, sapply(Relations_list, FUN = length)), stringsAsFactors = F)

CWE_Edgelist$Relationship <- strapplyc(CWE_Edgelist$Target, "(.*) -",simplify = T )
CWE_Edgelist$Target <- strapplyc(CWE_Edgelist$Target,"- (.*)", simplify = T )
CWE_Edgelist$Relationship <- trimws(CWE_Edgelist$Relationship, which="b")
CWE_Edgelist$Target <- as.numeric(CWE_Edgelist$Target)
CWE_Edgelist$Source <- as.numeric(CWE_Edgelist$Source)
CWE_Edgelist$Relationship <- as.factor(CWE_Edgelist$Relationship)

write.csv(CWE_Nodelist, file = "CWE_Nodelist.csv", row.names = F)
write.csv(CWE_Edgelist, file = "CWE_Edgelist.csv", row.names = F)
