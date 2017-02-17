# This is the script for crawling the CVE Details website. The input format is as follows:
# python crawler.py <file path of the urls file> <output path and file name with extension>
# The urls file should be in csv format with two columns of the names: url, number of pages where url is the separate url of the first page
# of a vulnerability type and the number of pages that are spanned to cover all CVE entries 

from bs4 import BeautifulSoup
import urllib
import requests
import csv
import sys


def crawl(inpath, filename):
	
	f= open(filename, 'wb')
	urls= []
	writer = csv.writer(f)
	writer.writerow(('CVE-ID', 'Vulnerability Type','Description','CWE-ID'))

	f12=open(inpath)
	reader=csv.DictReader(f12)
	for l in reader:
		basetemp=l['url'].split("page=1")
		base="page=".join((basetemp[0],""))
		base2=basetemp[1]
		no_pages=l['number of pages']

		for i in range(1,int(no_pages)+1):
			temp="".join((base,str(i)))
			url="".join((temp,base2))
			urls.append(url)
		
		for u in urls:
			print u
			html = urllib.urlopen(u).read()
			bs = BeautifulSoup(html,"lxml")
			table = bs.find(lambda tag: tag.name=='table' and tag.has_attr('id') and tag['id']=="vulnslisttable")
		#print "hi"
			rows = table.findAll('tr')
			for j in range(1,len(rows)):
				r= rows[j].findAll('td')
			
				if j%2==0:	# description
					desc= r[0].text.strip()

				else:		# id and vulnerability type and weakness id
					cid= r[1].text.strip()
					vtype= r[4].text.strip()
					cweid= r[2].text.strip()

				if j%2==0:
					try:
						writer.writerow([cid, vtype, desc,cweid])
					except UnicodeEncodeError:
						print "Ignoring"


if __name__ == "__main__":
    if len(sys.argv) != 3: 
        print "Usage: <path of the urls file> <output path and file name with extension>"
        exit(0)
    
    inpath= sys.argv[1] 
    outpath = sys.argv[2]
    
    crawl(inpath,outpath)



