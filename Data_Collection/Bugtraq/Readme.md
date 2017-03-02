This script assumes that the packages (rvest, magrittr & gsubfn) to be installed on the host system.

The script can be run as is. Follow the prompts on the screen to customize the data extraction process.

The script creates a directory for each year & each month and saves the Bugtraq records. There is also a Monthly aggregated .csv file 

User inputs -

1. User can change starting year & ending year through the prompts while running the script
2. User can also change starting and ending month numbers through the prompts on the scripts

Changes to be made to reuse the crawler for scraping other seclists data

1. Line 34 - Change 'bugtraq' to new crawler url 
2. Line 66 - In the trycatch command change 'bugtraq' to new crawler url 
3. Line 116 - While writing output file change filename in write.csv from 'Bugtraq' to new crawler name

Link to BugTraq repository on Mega: https://mega.nz/#F!CRV3kChD!ui9BpUzn1GW7AVaUdVXRog
