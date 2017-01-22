import csv
import sys

def filter(inp,out):
	fw= open(out, 'wb')
	writer = csv.writer(fw)
	writer.writerow(('Name', 'Status','Description','References','Phase','Votes','Comments'))

	fr=open(inp)
	reader=csv.DictReader(fr)
	total=0
	rej=0
	res=0
	for line in reader:
		total=total+1
		if line['Description'].find("** REJECT **") != -1: # if rejected, add 1 to rej count
			rej=rej+1
			continue
		else if line['Description'].find("** RESERVED **") != -1:	#if reserved, add 1 to reserved count
			res=res+1
			continue
		else:
			writer.writerow((line['Name'], line['Status'],line['Description'],line['References'],line['Phase'],line['Votes'],line['Comments']))
	
	print "Total= " + total
	print "Rejected= " + rej
	print "Reserved= " + res

if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print "Usage: <path of the raw cve file (.csv format)> <output path and file name with extension>"
        exit(0)
    
    inp=sys.argv[1]
    out=sys.argv[2]

    filter(inp,out)
