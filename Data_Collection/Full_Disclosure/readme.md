# Full Disclosure Mailing List E-mail Reply Crawler

This describes how to parse data from the Full Disclosure Mailing List. If you are only interested in some of the data, you can find the output of this script here: https://mega.nz/#F!iFdlkQKK!9EFzYq6CptBJtTdCOaY7ew

## Dependencies 

packages - rvest, magrittr, gsubfn, xml

## How to Use 

Running the downloaded script as is, should suffice to crawl the e-mail replies from Full Disclosure. The script has four prompts: 

 1. Start Year 
 2. End Year
 3. Start Month
 4. End Month
 
Prompts 1 and 2 should specify the desired year range to download.
Prompts 3 and 4 should specify the desired month range to download. 

The year and month range are independent. For instance, if the year range is 2013 to 2015 and month range is 04 to 07, the downloaded data will contain only the 4 months for all the 3 years. 

After the 4 prompts, the script will start downloading one e-mail reply at a time from Full Disclosure. A progress status message should be printed for every e-mail reply at least once a minute. The message will also indicate the month and year of the downloaded e-mail reply. 

The outputs are saved on an `output_ml` folder (created if it doesn't already exist) containing: 

 1. A number of files, each of every e-mail reply BODY. The file name will follow the format <Year>_<Month>_<Reply_ID>.txt, which uniquely identify the reply on the mailing list (observe the URL of a given reply, for example http://seclists.org/fulldisclosure/2016/May/0 contains Year, Month and ID). This facilitates quick inspection the parser extracted correctly the e-mail BODY.  
 2. A .csv table containing other metadata for the e-mail reply: Author, Timestamp and E-mail Title. 


Note that the .csv table is only saved after all e-mail replies have been downloaded.  

## Debugging 

If the crawler failed to download one or more e-mail replies, it is not required the entire month is downloaded again. Instead, modify `k` in the script. 

“ k ” (records parameter) – This variable can be altered to extract specific records within each month. By default, it has been set to iterate from 0 to the ending record in each month. For example, in order to extract records from 480 to the ending, we need to set the “ k ” variable to 480 to the end ( ‘ iterations -1 ’).

## Crawling other Seclists.org Mailing Lists 

Currently, reusing this script to download other mailing lists in Seclists.org require a few changes directly in the code. Later, we will modify the crawler so that a config file can be used instead of applying directly code changes. 

Line 32 - Change 'fulldisclosure' to new crawler url

Line 62 - In the trycatch command change 'fulldisclosure' to new crawler url

Line 110 - While writing output file change filename in write.csv from 'fulldisclosure' to new crawler name