from bs4 import BeautifulSoup
from calendar import month_abbr
import getopt
import os
import pendulum
import random
import re
import requests
import sys
import time


def dl_range(listname, year_start, month_start, year_end, month_end):
    """
    Download multiple months, using start & end year/months.
    See dl_month for contents.
    
    Args:
        listname: str, e.g. fulldisclosure
        year_start: int
        month_start: int (Jan = 1)
        year_end: int
        month_end: int (Jan = 1)
    """

    start = pendulum.date(year_start, month_start, 1)
    end = pendulum.date(year_end, month_end, 1)
    period = pendulum.period(start, end)
    for dt in period.range('months'):
        y, m = dt.year, dt.month
        dl_month(listname, y, m)
    
def dl_month(listname, year, month):
    """
    Download entire raw html contents of month.
    Contents will be written to subdir, e.g. ./2017_01
    
    Args: 
        listname: str, e.g. fulldisclosure
        year: int
        month: int (Jan = 1)
    """
    
    year_str = str(year)
    month_0x = str(month).zfill(2)
    month_str = month_abbr[month]
    
    output_path = './' + year_str + '_' + month_0x
    create_dir(output_path)
    
    index_file = dl_index(listname, year_str, month_str, output_path)
    message_count = parse_index_num(index_file)

    for i in range(message_count):
            dl_message(listname, year_str, month_str, str(i), output_path)
            #use random sleep to prevent banning
            time.sleep(5 * random.random())


def dl_index(listname, year, month, path):
    """
    Download month's index file.
    
    Args:
        listname: str, e.g., fulldisclosure
        year: str, e.g. "2017"
        month: str, e.g., "Jan"
        path: str
    
    Returns:
        str: filename that contents were written into
    
    """
    
    #ex: http://seclists.org/fulldisclosure/2017/Jan/index.html
    url = 'http://seclists.org/' + listname + '/' + year + '/' + month + '/index.html'
    print(url)
    r = requests.get(url)
    
    #save file, e.g.: 2017_Jan.raw.html
    filename = os.path.join(path, year + '_' + month + '.raw.html')
    with open(filename, 'w') as w:
        w.write(r.text)

    return filename


def parse_index_num(filename):
    """
    Determine the max reply id the index file contains. 
    Note: the first line (e.g., <!-- SecLists-Message-Count: 108 -->) can be false!
    
    Args: 
        filename: str
    
    Returns:
        int
    
    """
    with open(filename, 'r') as f:
        raw = f.read()

    raw = raw.replace('<a name="begin">', '<a name="begin"></a>')
    soup = BeautifulSoup(raw, 'html5lib')
    f.close()

    begin = soup.find(attrs={'name':'begin'}) #beginning of msg links
    replies = begin.find_next('ul').find_all('li')
    
    max_id = 0
    for reply in replies:
        msg = reply.find('a')
        if msg is not None:
            id = int(msg['href'])
            max_id = max(max_id, id)

    return max_id + 1

def dl_message(listname, year, month, id, path):
    """
    Download individual message.
    
    Args: 
        listname: str, e.g., "fulldisclosure"
        year: str, e.g. "2017"
        month: str, e.g., "Jan"
        id: str, e.g., "0"
        path: str
    
    """
    
    #ex: http://seclists.org/fulldisclosure/2017/Jan/0
    url = 'http://seclists.org/' + listname + '/' + year + '/' + month + '/' + id
    print(url)
    r = requests.get(url)
    
    #check for redirect, which can happen if the original message goes missing.
    if(r.url == url):
        #save file, ex: 2017_Jan_0.raw.html
        filename = os.path.join(path, year + '_' + month + '_' + id + '.raw.html')
        with open(filename, 'w') as w:
            w.write(r.text)


def create_dir(directory):
    """
    Create dir if not exists.
    """
    
    if not os.path.exists(directory):
        os.makedirs(directory)


def usage():
    print(main.__doc__)    

def main(argv=None):
    """
    Args:
        Required: 
        -l <listname>, e.g., fulldisclosure, bugtraq
        
        Pick one of: 
        -y <year>, download entire year, e.g., -y 2011
        -m <yearmonth>, download specific month, e.g. -m 201101 for Jan. 2011
        -i <yearmonth-id>, download specific message, e.g., -i 201101-0
    """    
    if argv is None:
        argv = sys.argv
    
    try:
        optslist, args = getopt.getopt(argv[1:], 'l:y:m:i:')
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    
    # process options
    if len(optslist) == 0:
        usage()
        sys.exit(0)
    
    opts = dict(optslist)
    
    if '-l' in opts:
        listname = opts['-l']
    else:
        print('listname (-l) option is required.')
        usage()
        sys.exit(2)
    
    try:
        if '-y' in opts:
            a = opts['-y']
            y = int(a)
            dl_range(listname, y, 1, y, 12)
            sys.exit(0)
        elif '-m' in opts:
            a = opts['-m']
            y = int(a[0:4])
            m = int(a[4:])
            dl_month(listname, y, m)        
        elif '-i' in opts:
            a = opts['-i']
            y = a[0:4]
            m = month_abbr[int(a[4:6])]
            i = a[7:]
            print(y,m,i)
            dl_message(listname, y,m,i,'.')        

    except Exception as e:
        print(e)
        usage()
        sys.exit(2)


if __name__ == "__main__":
    main()
