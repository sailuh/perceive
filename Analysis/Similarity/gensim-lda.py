import gensim
import sys
import os
from nltk.corpus import stopwords
from collections import defaultdict
from gensim import corpora, models, similarities
import string
import numpy
import re
import csv

# function for running the LDA model 
def lda_v1(topc,thrd,vul_type):
  
  raw_corpus= []

  f=open(vul_type)

# Reading each line of the file and preprocessing the text data

  for text in f:
    raw_corpus.append(text)
       #pre-processing the corpus
  punctuation = list(string.punctuation)
  stop = stopwords.words('english') + punctuation
  texts = [[word for word in document.lower().split() if word not in stop] for document in raw_corpus]

# Creating a dictionary of frequency of the words in the text data
  frequency = defaultdict(int)
  for text in texts:
      for token in text:
        frequency[token] += 1

  processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]

    	#creating a dictionary of words
  dictionary = corpora.Dictionary(processed_corpus)

    	#creating a vector of the corpus
  corpus = [dictionary.doc2bow(text) for text in processed_corpus]

# applying the LDA model on the corpus vector
  lda = models.LdaModel(corpus, num_topics=topc,id2word=dictionary)
  index = similarities.MatrixSimilarity(lda[corpus])  

  fw=open("LDA_Word_Topic_distribution.csv",'wb')
  writer = csv.writer(fw)

# writing the word-topic distribution to a csv file
  writer.writerow(('Topic_id', 'Word','Weight'))

  for j in range(len(lda.print_topics(-1,int(topc)))):
    w=lda.show_topic(j,int(topc))
    for t in w:
      top=j
      word=t[0]
      prob=t[1]  
      writer.writerow([top,word,prob])

 
# writing the topic-document distribution to a csv file
  fwr1=open("LDA_Topic_Document_distribution.csv",'wb')
  wtr1 = csv.writer(fwr1)
  wtr1.writerow(('Document','Topic_id','Weight'))

  frd=open(vul_type)
  reader= csv.DictReader(frd)

  for txt in reader:
    d=" ".join((txt['Vulnerability_Type'],txt['Description']))
    d_bow = dictionary.doc2bow(d.lower().split())
    v_lda=lda[d_bow]

    for  i in range(len(v_lda)):
      document=txt['CVE_Id']
      topic=v_lda[i][0]
      weight=v_lda[i][1]
      wtr1.writerow([document,topic,weight])

  fwr=open("LDA_Document_Similarity.csv",'wb')
  wtr = csv.writer(fwr)
  
# writing the FD thread - topic distribution to a csv file
  row1=["Thread"]

  for i in range(int(topc)):
    t1="_".join(("Topic",str(i+1)))
    row1.append(t1)

  wtr.writerow(row1)

  record={}

  for fl in os.listdir(thrd):
    fn = os.path.join(thrd, fl)
    if fn.lower().endswith('.txt'):
      f = open(fn,'rb')
      doc = f.read()
      try:
        doc_bow = dictionary.doc2bow(doc.lower().split())
      except UnicodeDecodeError:
        print "Ignore"
        continue
      vec_lda=lda[doc_bow]
      document=fl
                
      for j in range(int(topc)):
        record[j]=0
      for  i in range(len(vec_lda)):
        topic=vec_lda[i][0] 
        record[topic]=vec_lda[i][1]
        
      row2=[document]

      for kt in range(int(topc)):
        row2.append(record[kt])

      wtr.writerow(row2)

if __name__ == "__main__":
    if len(sys.argv) != 4: 
      print "Usage: <location of the folder containing all email threads> <Number of topics> <name of the csv file containing the details of a particular vulnerability along with location>"
      exit(0)

    topc=sys.argv[2]
    thrd=sys.argv[1]
    vul_type=sys.argv[3]
 

    lda_v1(topc,thrd,vul_type)