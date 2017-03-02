#script to get the thread FD data in the format required for Running LDA

import csv
import sys
import os

def get_data(f):
	try:
		f2= open(f)
		d=f2.read().strip()
		f2.close()
	except IOError:
		print "error"
		d=""
	return d


if __name__ == "__main__":
	if len(sys.argv) != 4: 
		print "Usage: <folder with all .txt replies output from fd_group_reply_by_thread.R> <.csv output from fd_group_reply_by_thread.R> <output folder>"
		exit(0)

	csvpath=sys.argv[1]
	folderpath=sys.argv[2]
	sname=sys.argv[3]

	j=0 #thread index

	with open(csvpath) as f:
		reader = csv.DictReader (f)
		for row in reader:
            #extract the reply file name that is the root and add .txt suffix
			ids=row['thread_id'].strip()
			i=".".join((ids,"txt"))
            #extract root reply content.
			text=get_data(os.path.join(folderpath,i))            
            #extract to a python list reply file names of the given row 
			reply_id=row['thread_reply_ids'].strip()
			reply_ids=reply_id.split(",")                                    
            #create thread file name and add .txt suffix
			jf="_".join(("thread",str(j)))
			jfile=".".join((jf,"txt"))            
			fn= open(os.path.join(sname,jfile),'wb')
			for r in reply_ids:
                #add .txt suffix to reply ID
				f1=".".join((r,"txt"))
                #if the thread contained no reply IDs, then the suffix will be the entire string. Move to the next row.
				if f1==".txt":
					continue
                #otherwise, there are replies which the content must be appended to the thread id reply file.     
				else:                    
					t=get_data(os.path.join(folderpath,f1))
					#print t
                    #5 line breaks are used to separate e-mail replies. Required for term co-ocurrence. 
					text="\n\n\n\n\n".join((text,t)) 
			#print text
            #writes all the aggregated replies of a given thread into the thread file.
			fn.write(text)
			fn.close()
			j=j+1