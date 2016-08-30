from spacy.en import English # Load English tokenizer, tagger, parser, NER and word vectors 
import sys #To get the parameters passed to the script by command line
import csv #for writing csv
import operator #for sorting
import pandas as pd
import os

# pip install spacy && python -m spacy.en.download 
parser = English() # Instantiate the english parser from Spacy (Singleton - eats over 3GB of memory!)


def extract_nouns_span(text):
    try:
        doc = parser(text.decode('utf-8')) #Parse document with spacy
        noun_span = doc.noun_chunks #This is a list of nouns in the provided text, which may be several tokens
        noun_text = remove_stop_word_and_apply_lemming(noun_span) 
        #print noun_text
        return noun_text
    except UnicodeDecodeError:
        print 'This row contains characters that cant be decoded and will be ignored in further analysis.'
        #print 'Content: '+text      
        
def remove_stop_word_and_apply_lemming(row_text,lemming=True):
    row_text_nouns = []
    if lemming:
        for noun_span in row_text: #This is the list of nouns on the provided text
            noun_text = ""
            for noun_token in noun_span: #This is the list of tokens on each noun 
                if noun_token.is_stop:
                    continue
                else:
                    noun_text = noun_text+" "+noun_token.lemma_ #lemming
            row_text_nouns.append(noun_text)
            
    else:
        for noun_span in row_text:
            noun_text = ""
            for noun_token in noun:
                if noun_token.is_stop:
                    continue
                else:
                    noun_text = noun_text+" "+noun_token.orth_ #token text representation
            row_text_nouns.append(noun_text)
    return row_text_nouns
    

def calc_and_sort_frequency(rows):        
    #each row contain a list of nouns
    
    #calculate the noun frequencies
    noun_freq = {}
    noun_document_freq = {}
    for list_of_nouns in rows:
        if list_of_nouns is None: continue #This is for cases where we cant parse the unicode and the nouns cant be extracted
        unique_nouns_per_document = set(list_of_nouns)
        #noun freq
        for noun in list_of_nouns:
            if noun not in noun_freq:
                noun_freq[noun] = 1
            else:
                noun_freq[noun] = noun_freq[noun] + 1     
        #noun document freq
        for noun in unique_nouns_per_document:
            if noun not in noun_document_freq:
                noun_document_freq[noun] = 1
            else:
                noun_document_freq[noun] = noun_document_freq[noun] + 1
                
    #sort noun frequency 
    noun_freq = sorted(noun_freq.items(), key=operator.itemgetter(1),reverse=True)
    noun_document_freq = sorted(noun_document_freq.items(), key=operator.itemgetter(1),reverse=True)


        
    return noun_freq,noun_document_freq

if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print "Usage: <directory path for the input files> <output path and file name with extension>"
        exit(0)
        
    nouns=[]
    path = sys.argv[1]

    
    i=0  
    for fl in os.listdir(path):
        fn = "".join((path, fl))
        if fn.lower().endswith('.txt'):
        	f = open(fn,'rb')
        	text = f.read()
        	nouns.append(extract_nouns_span(text))
        	
    noun_freq,issue_freq = calc_and_sort_frequency(nouns)

    f1= open(sys.argv[2], 'wb')
    writer = csv.writer(f1)
    writer.writerow(('noun', 'noun_frequency','noun_issue_frequency'))



    for (p,q) in zip(noun_freq,issue_freq):
        try:
            writer.writerow([p[0], p[1], q[1]])
            
        except UnicodeEncodeError:
            print "ignoring"
        
