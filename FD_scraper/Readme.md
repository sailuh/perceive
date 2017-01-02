Crawlers

# PERCIEVE
Steps to execute the R code:

The code is very flexible and can be configured to extract data for specific records in any particular month in any particular year.
There are three user configurable variables that can be set to configure the crawler.

“ i ” (year parameter) – This can be used to set the specific years that need to be extracted for the data. By default, this value is set to iterate between 1 to 16 to extract the data from 2002 to 2016. For example, to extract data from the year 2006 we need to set the “ i ” variable to iterate from 5 to 16 because 2006 is the 5th year from the starting year (2002).

“ j ” (month parameter) – This variable holds the value for the specific months for which data needs to be extracted. By default, this value is set to iterate between 1 to 12 on order to cover all the 12 months within a year. For example to extract data from the months of June and July, we need to set the “ j ” variable to iterate between 6 and 7 because June is the 6th month in the year and July is the 7th month.

“ k ” (records parameter) – This variable can be altered to extract specific records within each month. By default, it has been set to iterate from 0 to the ending record in each month. For example, in order to extract records from 480 to the ending, we need to set the “ k ” variable to 480 to the end ( ‘ iterations -1 ’).

The user just needs to alter these three variables in order to extract specific set of records within each year for a particular month.

Example: To extract data from 2005 to 2007, Jan through June please set the "i" (year) variable to 4:6, "j" (month) to 1:6. The crawler creates .txt files each email with the naming convention Year_Month_documentNumber. A .csv file is created for each month that contains data regarding the author name, title, dateStamp. 

Make these changes to customize the crawler 
for(i in 4:6){}
for(j in 1:6){}

