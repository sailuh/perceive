This script assumes that the Capec XML data is in the same directory as the script. 
The required R packages (rvest, magrittr & gsubfn) are installed on the host computer.

For this script capec_v2.8.xml was user, In case there is a newer version available on the CAPEC website please download it into the same folder as the script and change line number 7 to the new filename.

The script can be run as is. There are 3 output files for the script:
  1. Attack Pattern Data.csv : Contains all extracted data from the XML document
  2. Nodelist.csv : Contains Node table that can be directly loaded into Gephi
  3. Edgelist.csv : COntains Edge table that can be directly loaded into Gephi
