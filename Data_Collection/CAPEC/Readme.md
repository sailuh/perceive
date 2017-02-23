This script assumes that the Capec XML data is in the same directory as the script. 
The required R packages (rvest, magrittr & gsubfn) are installed on the host computer.

For this script capec_v2.8.xml was user, In case there is a newer version available on the CAPEC website please download it into the same folder as the script and change line number 7 to the new filename.

In Line 9 of the code, we are filtering the xml nodes that are only of the type 'Attack Pattern' hence extracting data only for the required fields. 

The nodelist contains variables that are unique to every attack pattern. The variables included are as follows:

1. ID

2. Name

3. Summary

4. Typical Severity

5. Typical_Likelihood of exploit

6. Attack Prerequisit

7. Methods of Attack 

8. Related Weakness CWE ID

Link to CAPEC data repository: https://mega.nz/#F!7JEnESzY!_1RDa8xqyqeny3evsU1VLQ

The edgelist contains information about the Source CAPEC ID, Target CAPEC ID anf the relationship type between the Attack Patterns. 

The script can be run as is. There are 3 output files for the script:
  1. Attack Pattern Data.csv : Contains all extracted data from the XML document
  2. Nodelist.csv : Contains Node table that can be directly loaded into Gephi
  3. Edgelist.csv : COntains Edge table that can be directly loaded into Gephi


