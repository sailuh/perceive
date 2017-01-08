The scraper script needs downloaded CWE data in XML format. Make sure the XML file is in the same folder as the scraper script.
For this script I have used the cwec_v2.9.xml file from the CWE archives

Incase there is a new version available on the CWE archive, please change the input file on line 8

Node Filtering: 

1. In Line 41 we are filtering the weakness nodes that only have a relationship of the type 'Weakness Class' from among the various categories like Weakness Class, Category, Views etc 

2. In Line 43 we are filtering the weakness nodes that are only of the relationship type 'Category' from among the various other relation types Weakness class, Category, Views etc 

The following variables have been included in the node list because they are attributes unique to each specific weakness in the CWE database:

i) Weakness ID : unique ID in the CWE database that identifies the weakness

ii) Weakness Name: unique name given to the weakness

iii) Weakness Description: Description about the weakness

iv) CAPEC ID for related attacks: Links to the CAPEC ID for related attack patterns for the weakness

The following variables have been included in the Edge  list to define edge relationship between the nodes:
i) Source: Weakness ID of the source for the relationship

ii) Target: Weakness ID of the destination node in the relationship

iii) Relationship type: Type of relationship between the nodes ( Childof, ParentOF, SameAs, Is Preceded By, etc)

There is no need to change or set any parameters, just install the required packages and run the script as is. 
There are 3 outputs from the script:
  1. Weakness_Data.csv : Contains all extracted data from the XML file
  2. Nodelist.csv : Contains the nodelist 
  3. Edgelist.csv : Contains the edgelist
