This Crawler is for CVE Details. It will download all pages for one type at a time. To create the input file do as follows:

0. Create a .csv file with 2 columns. 
1. Go to CVE Details Website, and then on the left menu click "Vulnerabilities by Type".
2. Pick one of the 13 types by clicking the number on the "Total" row.
3. On the bottom of the page, click on Page 1. 
4. Copy the URL. This constitutes a given type URL field. 
5. On the bottom, observe the number of pages the type has. Copy the highest page number. This constitutes the Page field. 

If you want to add more types, repeats steps 1-5 and add as many rows as required. The current example input file contains 7 types. 
The number of pages updates frequently as new entries are added.

Notice CVE Details do not contain rejected or candidate entries, so no filtering is required.