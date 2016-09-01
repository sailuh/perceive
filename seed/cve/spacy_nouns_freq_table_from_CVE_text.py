#!/usr/bin/env python
__version__ = "0.0.3"
__maintainer__ = "Carlos Paradis"
__email__ = "cvas@hawaii.edu"

from spacy.en import English # Load English tokenizer, tagger, parser, NER and word vectors 
import sys #To get the parameters passed to the script by command line
import csv #for writing csv
import operator #for sorting
import pandas as pd

# pip install spacy && python -m spacy.en.download 
parser = English() # Instantiate the english parser from Spacy (Singleton - eats over 3GB of memory!)

def extract_nouns_span(text):
    try:
        doc = parser(text.decode('utf8')) #Parse document with spacy
        noun_span = doc.noun_chunks #This is a list of nouns in the provided text, which may be several tokens
        noun_text = remove_stop_word_and_apply_lemming(noun_span) 
        return noun_text
    except UnicodeEncodeError:
        print 'This row contains characters that cant be decoded and will be ignored in further analysis.'
        print 'Content: '+text      
        
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
    noun_issue_freq = {}
    for list_of_nouns in rows:
        if list_of_nouns is None: continue #This is for cases where we cant parse the unicode and the nouns cant be extracted
        unique_nouns_per_issue = set(list_of_nouns)
        #noun freq
        for noun in list_of_nouns:
            if noun not in noun_freq:
                noun_freq[noun] = 1
            else:
                noun_freq[noun] = noun_freq[noun] + 1     
        #noun issue freq
        for noun in unique_nouns_per_issue:
            if noun not in noun_issue_freq:
                noun_issue_freq[noun] = 1
            else:
                noun_issue_freq[noun] = noun_issue_freq[noun] + 1
                
    #sort noun frequency 
    noun_freq = sorted(noun_freq.items(), key=operator.itemgetter(1),reverse=True)
    noun_issue_freq = sorted(noun_issue_freq.items(), key=operator.itemgetter(1),reverse=True)
        
    return noun_freq,noun_issue_freq
    
    
if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print "Usage: <text or csv file to extract nouns> <output path and file name with extension>"
        exit(0)
        
        

#    text = open(sys.argv[1]).read() 
#    with open(sys.argv[1], 'rb') as csvfile:
#        text = ""
#        text_csv = csv.reader(csvfile, delimiter=' ', quotechar='"')
#        for t in text_csv:
#            text = text+" ".join(t)
            
    #Read the table as a dataframe on Pandas Framework
    df = pd.ExcelFile(sys.argv[1],header=None).parse('Sheet1')
    #Create Header
    df.columns = ['id','description']
#    df = pd.ExcelFile('data/CVE_reports_XSS.xlsx',header=None).parse('Sheet1')
    
    df["nouns"] = df['description'].apply(extract_nouns_span)
    #df['nouns'].apply(calc_noun_fequency_and_issue_frequency,args=(noun_freq,issue_freq))
    noun_freq,issue_freq = calc_and_sort_frequency(df["nouns"])
    df_noun_freq = pd.DataFrame(noun_freq)
    df_noun_freq.columns = ['noun','frequency']

    df_issue_freq = pd.DataFrame(issue_freq)
    df_issue_freq.columns = ['noun','frequency']
    
    df_freqs = pd.merge(df_noun_freq, df_issue_freq, how='outer',on='noun')
    df_freqs.columns = ['noun','noun_frequency','noun_issue_frequency']
    
    df_freqs.to_csv(sys.argv[2],index=False)
    
