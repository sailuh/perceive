The fd_to_thread.py script converts the csv format of email threads of Full disclosure mailing list(example-FD_Threads2002.csv) to
separate text files for each email thread; which are further used as input for similarity calculation script.

NOTES:
1.	If running the script for 2002 FD list, place this script in the folder containing all the individual FD mails for that particular 
year
2.	This script will then generate the text files for each email thread mentioned in the FD_Threads2002.csv file. The text body contains
only the description for each of the participating mails for each mail thread.

INSTRUCTIONS TO RUN SCRIPT:
python fd_to_thread.py FD_Threads2002.csv 
python fd_to_thread.py FD_Threads2007.csv 

.....and so on for all years

A sample input file (FD_Threads2005.csv) has been uploaded.
