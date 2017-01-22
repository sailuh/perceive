import csv #for reading from csv
import string
import sys

def create_edgelist(source_file,dest_file):		#fname is the year
	text_file= open(dest_file, 'wb')		#the text file where the edgelist is to be made
	writer = csv.writer(text_file)
	writer.writerow(['noun','document_list'])
	with open(source_file) as f:
		reader = csv.DictReader(f)
		for row in reader:
			noun= row['noun']
			docs= row['document_list']
			doc_list=docs.split(';')	#splitting the list of documents that the nounform appears in 
			for d in doc_list:
				d1 = d.split('.')
				#line=",".join((noun,d1[0]))
				writer.writerow([noun,d1[0]])
	return "done"


if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print "Usage: <name of the csv file with the path> <output path and file name with extension>"
        exit(0)

    s= create_edgelist(sys.argv[1], sys.argv[2])
    print s
    
