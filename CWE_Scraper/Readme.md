The scraper script needs downloaded CWE data in XML format. Make sure the XML file is in the same folder as the scraper script.
For this script I have used the cwec_v2.9.xml file from the CWE archives

Incase there is a new version available on the CWE archive, please change the input file on line 8

There is no need to change or set any parameters, just install the required packages and run the script as is. 
There are 3 outputs from the script:
  1. Weakness_Data.csv : Contains all extracted data from the XML file
  2. Nodelist.csv : Contains the nodelist 
  3. Edgelist.csv : Contains the edgelist
