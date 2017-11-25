from bs4 import BeautifulSoup
from calendar import month_abbr
import csv
import getopt
import os
import pendulum
import re
import sys

def parse(filename, idroot):
    """
    Parse seclists index file, write csv output.
    
    Args:
        filename: str
        idroot: str, e.g. '2017_01'
    """
    
    with open(filename, 'r') as f:
        raw = f.read()

    #body contains unclosed anchor tag; add the closing tag to make parsing easier.
    raw = raw.replace('<a name="begin">', '<a name="begin"></a>')
    soup = BeautifulSoup(raw, 'html5lib')
    f.close()

    begin = soup.find(attrs={'name':'begin'}) #beginning of msg links
    items = begin.find_next('ul').find_all('li', recursive=False)

    messages = []
    read_messages(items, messages, idroot, None)
    csvfile = filename.replace('.raw.html', '.csv')
    for message in messages:
        parse_reply(filename, message)
    write_csv(csvfile, idroot, messages)

def read_messages(items, messages, idroot, parent):
    """
    RECURSIVE. Read message info from index.
    
    Args:
        items: array of <li> beautifulsoup objects
        messages: array of dict, holds output
        idroot: str, e.g. '2017_01'
        parent: str, id of parent; use None if initial level
    """
    for li in items:
        msg = li.find('a')
        if msg == None:
            #some messages just read "Possible follow-ups" with no link--skip
            continue
        id = idroot + '_' + msg['href']
        title = msg.text
        
        whowhen = li.find('em').text
        rx = re.compile('(.+) \((.+)\)')
        m = rx.search(whowhen)
        if(m is None):
            #some messages just read <em>Message not available</em>--skip
            continue
        who = m.group(1)
        when = m.group(2)

        messages.append({
            'index': msg['href'],
            'id': id,
            'title': title,
            'parent': parent,
            'author': who,
            'date': when
        })
        
        replies = li.find('ul')
        if replies != None:
            read_messages(replies.find_all('li', recursive=False), messages, idroot, id)

    return messages

def parse_reply(index_filename, message):
    reply_filename = index_filename.replace('.raw.html', '_' + message['index']+ '.raw.html') 
    with open(reply_filename, 'r') as f:
        reply = f.read()

    start = reply.index('<!--X-Head-of-Message-->') + 24
    end = reply.index('<!--X-Head-of-Message-End-->')

    head = reply[start:end]
    soup = BeautifulSoup(head, 'html5lib')
    ems = soup.find_all('em')

    for em in ems:
        if em.text == 'From':
            author = em.next_sibling
            #list obfuscates email by replacing @ with ' () ' and removing periods from domain name
            if author.startswith(': '):
                author = author[2:]
            author = author.replace(' () ', '@')
            at = author.find('@')
            author = author[:at] + author[at:].replace(' ', '.') 
            message['author'] = author
        elif em.text == 'Date':
            date = em.next_sibling
            if date.startswith(': '):
                date = date[2:]
            try:
                parsed_date = str(pendulum.parse(date).in_timezone('UTC'))
            except:
                basename = os.path.basename(index_filename)
                parsed_date = str(pendulum.parse(message['date'] + ' ' + basename[0:4]).in_timezone('UTC'))
            message['date'] = parsed_date


def write_csv(filename, idroot, messages):
    with open(filename, 'w') as w:
        output = csv.writer(w)
        output.writerow(['id', 'title', 'date', 'author', 'parent'])
        for x in messages:
            output.writerow([x['id'],
                            x['title'],
                            x['date'],
                            x['author'],
                            x['parent']])
    pass


def process_year(year, path):
    for i in range(1,13):
        month_dir = year + '_' + str(i).zfill(2)
        filename = year + '_' + month_abbr[i] + '.raw.html'
        filepath = os.path.join(path, month_dir, filename)
        print(filepath)
        parse(filepath, month_dir)


def insert_sqlite3(idroot, messages, db):
    pass


def usage():
    print(main.__doc__)


def main(argv=None):
    """
    Args:
        -f <filename>, parse single raw file, e.g. -f ./2011_Jan_0.raw.html
    """
    if argv is None:
        argv = sys.argv

    try:
        opts, args = getopt.getopt(argv[1:], 'f:')
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    # process options
    if len(opts) == 0:
        usage()
        sys.exit(0)

    for o, a in opts:
        try:
            if o == '-f':
                path = os.path.realpath(a)
                directory = os.path.dirname(path)
                idroot = os.path.basename(os.path.normpath(directory))
                parse(a, idroot)
        except Exception as e:
            print(e)
            usage()
            sys.exit(2)


if __name__ == "__main__":
    main()