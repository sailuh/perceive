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

# function for running the LDA model on document vt and extracting out tp number of topics
def lda_v1(vt,tp):
  
  raw_corpus= []

  t=".".join((vt,'csv'))
  print t
  
  f=open(t)

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
  lda = models.LdaModel(corpus, num_topics=20,id2word=dictionary)
  index = similarities.MatrixSimilarity(lda[corpus])  

  t="_".join((vt,tp))
  t="_".join((t,"topic"))
  t="_".join((t,"terms"))
  t=".".join((t,"csv"))
  print t

  fw=open(t,'wb')
  writer = csv.writer(fw)

# writing the word-topic distribution to a csv file
  writer.writerow(('Topic_id', 'Word','Weight'))

  for j in range(len(lda.print_topics(-1,20))):
    w=lda.show_topic(j,20)
    for t in w:
      top=j
      word=t[0]
      prob=t[1]  
      writer.writerow([top,word,prob])

  t="_".join(("CVE",tp))
  t="_".join((t,"topic"))
  t="_".join((t,vt))
  t=".".join((t,"csv"))
  print t

# writing the topic-document distribution to a csv file
  fwr1=open(t,'wb')
  wtr1 = csv.writer(fwr1)
  wtr1.writerow(('Document','Topic_id','Weight'))

  t=".".join((vt,'csv'))
  print t

  frd=open(t)
  reader= csv.DictReader(frd)

  for txt in reader:
    #print "hi"
    d=" ".join((txt['Vulnerability_Type'],txt['Description']))
    #print doc
    d_bow = dictionary.doc2bow(d.lower().split())
    v_lda=lda[d_bow]

    for  i in range(len(v_lda)):
      document=txt['CVE_Id']
      topic=v_lda[i][0]
      weight=v_lda[i][1]
      wtr1.writerow([document,topic,weight])

  t="_".join(("FD","CVE"))
  t="_".join((t,tp))
  t="_".join((t,vt))
  t="_".join((t,"topic"))
  t="_".join((t,"similarity"))
  t=".".join((t,"csv"))
  print t

  fwr=open(t,'wb')
  wtr = csv.writer(fwr)
  
# reading in the csv file with the url and file-name mapping
  urlfile="addurl.csv"
  furl=open(urlfile)
  creader=csv.reader(furl)

  url={}

  for r in creader:
    url[r[1]]=r[0]
  

  # writing the FD thread - topic distribution to a csv file
  row1=["Year","Thread","URL"]

  for i in range(int(tp)):
    t1="_".join(("Topic",str(i+1)))
    row1.append(t1)

  wtr.writerow(row1)

  record={}

  path="C:\Users\PAL\Desktop\PERCEIVE\Threads"
  for k in range(2002,2017):
    temp="\\".join((path,str(k)))
    for fl in os.listdir(temp):
      fn = "\\".join((temp, fl))
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
        year=k
        
        for j in range(int(tp)):
          record[j]=0
        for  i in range(len(vec_lda)):
          #document=txt['CVE_Id']
          topic=vec_lda[i][0] 
          record[topic]=vec_lda[i][1]

        new_document="_".join((str(year),document))
        row2=[year,document,url[new_document]]

        for kt in range(int(tp)):
          row2.append(record[kt])

        wtr.writerow(row2)
        #wtr.writerow([year,document,record[0],record[1],record[2],record[3],record[4],record[5],record[6],record[7],record[8],record[9],record[10],record[11],record[12],record[13],record[14],record[15],record[16],record[17],record[18],record[19]])

if __name__ == "__main__":
    if len(sys.argv) != 3: 
      print "Usage: <Vulnerability Type> <Number of topics>"
      exit(0)

    vt=sys.argv[1]
    tp=sys.argv[2]

    lda_v1(vt,tp)