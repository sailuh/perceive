<h3>SIMILARITY MODEL: GENSIM LDA </h3>
<p>
This folder contains the script for running the LDA model on text data. This specific script extracts the topics from the CVE and FD mailing lists. Also, it calculates the similarity score (between 0 and 1) between the two.
</p>

<h5>Example input script:</h5>
<p>
python genism-lda_v2.py (location of the folder containing all email threads) (Number of topics) (name of the csv file containing the details of a particular vulnerability along with location)
</p>
<p>
python gensim-lda_v2.py C:\Users\PAL\Desktop\PERCEIVE\Threads\2016 20 C:\Users\PAL\Desktop\PERCEIVE\Week11\DoS.csv
</p>

<h5>Output:</h5>
<p>
This script generates three output files (sample files put up in ‘Output’ subfolder):<br>
•	LDA_Word_Topic_distribution.csv (contains distribution of the terms in each topic of the LDA model)<br>
•	LDA_Topic_Document_distribution.csv (contains the distribution of topics and corresponding weights for each CVE entry in the vulnerability file; here the DoS.csv file)<br>
•	LDA_Document_Similarity.csv (contains the similarity value of each email thread with each topic of the LDA model)
</p>

<h5>Notes:</h5>
<p>
•	The text-data from the vulnerability file is pre-processed/cleaned (i.e. stopwords and punctuations are removed) in this script. The text of the Full Disclosure mailing list threads is NOT pre-processed/cleaned. <br>
•	Please NOTE that the input format clearly. Each thread of the FD mailing list is in .txt format. One text file for one thread (Use the fd_to_Threads script) <br>
•	The third argument is a csv file containing all CVE entries related to a particular vulnerability type. Sample file is put up in the “Input” subfolder under the name of DoS.csv <br>
</p>
