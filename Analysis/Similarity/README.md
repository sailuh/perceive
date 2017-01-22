This folder contains the script for running the LDA model on text data. This specific script extracts the topics from the CVE and FD mailing
lists. Also, it calculates the similarity score between the two.

Example input script:

python gensim-lda_v1.py <Vulnarability Type> <Number of topics to be extracted>

python gensim-lda_v1.py XSS 20

Following are the vulnerabilities that CVE covers:
1) DoS
2) Execute_Code
3) File_Inclusion
4) CSRF
5) Gain_Information
6) Bypass
7) HTTP_Response_Splitting
8) Directory_Traversal
9) XSS
10) SQL_Injection
11) Memory_Corruption
12) Overflow
13) Gain_Privileges
