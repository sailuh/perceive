# PERCEIVE Database modeling

- This model contains the basic understanding for two categories of tables:

1. Tables related to the website experiment.
1. Vulnerabity entites' package. 'Flexible' tables related to the cve, nvd and mitre csv files.

- Tables related to the website experiment.

2. User consent is a referece table that aggregate information about the content of the other tables;
2. Session is the table that stores data about the access made by the user;
2. Knwoledge source refers to the type material evaluated by the user;
2. Email thread is table that contails the group of email text to be analyzed;
2. Authentication is the table that stores information about the login. 


- Tables related to the experiment.

3. Vunerability is a table for receiving data from cve, nvd and mitre csv files, both 'fixed' data and 'flexible' data. 
3. Tables detail\_atribute and vulnerability\_ has\_detail\_attribute manage the flexible attributes from the former table;
3. Vunerability\_type is a table to identify if the vunerability is sql injection etc. 
