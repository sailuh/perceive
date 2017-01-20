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
