#script to get the thread FD data in the format required for Running LDA

import csv
import sys

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
	if len(sys.argv) != 2: 
		print "Usage: <Name of the file>"
		exit(0)

	fname=sys.argv[1]

	j=0

	with open(fname) as f:
		reader = csv.DictReader(f)
		for row in reader:
			ids=row['threadtId'].strip()
			reply_id=row['reply_IDs'].strip()
			reply_ids=reply_id.split(",")
			i=".".join((ids,"txt"))
			text=get_data(i)
			jf="_".join(("thread",str(j)))
			jfile=".".join((jf,"txt"))
			fn= open(jfile,'wb')
			for r in reply_ids:
				f1=".".join((r,"txt"))
				if f1==".txt":
					continue
				else:
					t=get_data(f1)
					#print t
					text="".join((text,t))
			#print text
			fn.write(text)
			j=j+1