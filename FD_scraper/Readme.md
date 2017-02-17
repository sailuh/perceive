Crawlers

Dependencies 

packages - rvest, magrittr, gsubfn

# PERCIEVE
Steps to execute the R code:

The code is very flexible and can be configured to extract data for specific records in any particular month in any particular year.
There are three user configurable variables that can be set to configure the crawler.

“ k ” (records parameter) – This variable can be altered to extract specific records within each month. By default, it has been set to iterate from 0 to the ending record in each month. For example, in order to extract records from 480 to the ending, we need to set the “ k ” variable to 480 to the end ( ‘ iterations -1 ’).

Changes to be made to reuse this script for other seclists crawlers

User inputs -

User can change starting year & ending year through the prompts while running the script
User can also change starting and ending month numbers through the prompts on the scripts
Changes to be made to reuse the crawler for scraping other seclists data

Line 32 - Change 'fulldisclosure' to new crawler url

Line 62 - In the trycatch command change 'fulldisclosure' to new crawler url

Line 110 - While writing output file change filename in write.csv from 'fulldisclosure' to new crawler name



Meta data for node & edge list in Gephi:
Link to Mega folder: https://mega.nz/#F!CUEByR5I!GY56GzTpYz68IlTqj4aQNQ 

There are three different networks that were created for the social network analysis in Gephi:

1. Author - Document Thread- Seed network

Nodelist - Contains the following variables
    -> Id - Indicates the author name or document name or the seed 
    -> Label 1 - Repetition of Id information for display
    -> Label 2 - For the document thread nodes, it indicates the other documents that are children of this parent thread
    -> Label 3 - For document thread nodes it gives a url link to the parent document
    -> Color - Indicates the color for the node 
    -> nodeType - Indicates if the node is a seed, document or author
    
Edgelist - Contains the following variables
    -> Source - Contains source nodes of author or documents
    -> Target - Contains the destination seed node for the documents, destination document nodes for the authors
    -> Weight - Indicates the strength of the relationship between two nodes (Number of occurances)
  
2. Author - Document thread network


Nodelist - Contains the following variables
    -> Id - Indicates the author name or document name
    -> Label 1 - Repetition of Id information for display
    -> Label 2 - For the document thread nodes, it indicates the other documents that are children of this parent thread
    -> Label 3 - For document thread nodes it gives a url link to the parent document
    -> Color - Indicates the color for the node 
    -> nodeType - Indicates if the node is a document or author
    
Edgelist - Contains the following variables
    -> Source - Contains source nodes of author
    -> Target - Contains the destination document nodes for the authors
    -> Weight - Indicates the strength of the relationship between two nodes (Number of occurances)
    

3.   Document - Seed thread network

Nodelist - Contains the following variables
    -> Id - Indicates the document name or the seed 
    -> Label 1 - Repetition of Id information for display
    -> Label 2 - For the document thread nodes, it indicates the other documents that are children of this parent thread
    -> Label 3 - For document thread nodes it gives a url link to the parent document
    -> Color - Indicates the color for the node 
    -> nodeType - Indicates if the node is a seed or document
    
Edgelist - Contains the following variables
    -> Source - Contains source nodes of documents
    -> Target - Contains the destination seed node for the documents
    -> Weight - Indicates the strength of the relationship between two nodes (Number of occurances)
  
