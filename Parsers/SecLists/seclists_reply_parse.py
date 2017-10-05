from bs4 import BeautifulSoup
import getopt
import html
import json
import os
import re
import sys
from urllib.parse import urlparse

from talon.signature.bruteforce import extract_signature

def parse_month_folder(path):
    """
    Parse .raw.html files in specific directry

    Args:
        path: str, directory containing .raw.html files
    """

    for f in [f for f in os.listdir(path) if (f.endswith('raw.html') and len(f) > 17)]: #ignore index file
        print(f)
        parse_reply(os.path.join(path, f))


def parse_reply(filename):
    """
    Extract body contents from reply, stripping away html tags.

    Args:
        filename: str, full path of .raw.html file
    """

    with open(filename, 'r') as f:
        raw = f.read()

    title = parse_reply_title(raw)
    bodyhtml, bodytext = parse_reply_body(raw)
    content = strip_sig_footer(bodytext)

    body_filename = filename.replace('.raw.html', '.reply.body.txt')
    with open(body_filename, 'w') as w:
        w.write(bodytext)

    title_body_filename = filename.replace('.raw.html', '.reply.title_body.txt')
    with open(title_body_filename, 'w') as w:
        w.writelines([title, '\n', bodytext])

    body_no_sig_filename = filename.replace('.raw.html', '.reply.body_no_signature.txt')
    with open(body_no_sig_filename, 'w') as w:
        w.write(content)

    title_body_no_sig_filename = filename.replace('.raw.html', '.reply.title_body_no_signature.txt')
    with open(title_body_no_sig_filename, 'w') as w:
        w.writelines([title, '\n', content])

    #parse tags
    tag_data = parse_reply_tags(bodyhtml)

    body_tags_filename = filename.replace('.raw.html', '.reply.body_tags.txt')
    with open(body_tags_filename, 'w') as w:
        w.write(json.dumps(tag_data))


def parse_reply_title(raw):
    """
    Read reply title.

    Args:
        raw: str, body contents of .raw.html file
    """

    soup = BeautifulSoup(raw, 'html5lib')
    subject = soup.find('meta', attrs={'name':'Subject'})
    title = subject['content']
    return html.unescape(title)


def parse_reply_body(raw):
    """
    Extract body content from reply, stripping away html tags.

    Args:
        raw: str, body contents of .raw.html file

    Returns:
        str, str: bodyhtml, body text (no html)
    """

    # Message body is contained between two comments; use basic indexing
    # <!--X-Body-of-Message-->
    # <!--X-Body-of-Message-End-->
    start = raw.index('<!--X-Body-of-Message-->') + 24
    end = raw.index('<!--X-Body-of-Message-End-->')
    body = raw[start:end]
    soup = BeautifulSoup(body, 'html5lib')

    # default parser adds html basic tags, so search inside <body>
    bodysoup = soup.find('body')
    bodytext = bodysoup.text
    return body, bodytext

def parse_reply_tags(bodyhtml):
    """
    Parse tag types and href domains from body html.

    Args:
        bodyhtml: html content of reply

    Returns:
        dict, {'tags': {}, 'sites': {} }
    """

    body = strip_footers(bodyhtml, True)

    rx = re.compile('<([^\s>]+)(\s|/>)+')
    tags = {}
    for tag in rx.findall(body):
        tagtype = tag[0]
        if not tagtype.startswith('/'):
            if tagtype in tags:
                tags[tagtype] = tags[tagtype] + 1
            else:
                tags[tagtype] = 1

    sites = {}
    bodysoup = BeautifulSoup(body, 'html5lib')
    atags = bodysoup.find_all('a')
    hrefs = [link.get('href') for link in atags]

    for link in hrefs:
        try:
            parsedurl = urlparse(link)
            site = parsedurl.netloc
            if site in sites:
                sites[site] = sites[site] + 1
            else:
                sites[site] = 1
        except ValueError as e:
            #skip any invalid URLs
            pass

    return {'tags': tags, 'sites': sites}


def strip_sig_footer(bodytext):
    no_footers = strip_footers(bodytext, False)

    #talon bruteforce technique to extract signature
    content, sig = extract_signature(no_footers)

    return content


def strip_footers(body, is_html):
    foot_len = 201
    if is_html == True:
        # longer length to compensate for html tags
        foot_len = 334

    workcopy = body

    #strip PGP sections from content
    try:
        pgp_sig_start = body.index('-----BEGIN PGP SIGNATURE-----')
        pgp_sig_end = body.index('-----END PGP SIGNATURE-----') + 27

        cleaned = body[:pgp_sig_start] + body[pgp_sig_end:]

        # if we find a public key block, then strip that out
        try:
            pgp_pk_start = cleaned.index('-----BEGIN PGP PUBLIC KEY BLOCK-----')
            pgp_pk_end = cleaned.index('-----END PGP PUBLIC KEY BLOCK-----') + 35
            cleaned = cleaned[:pgp_pk_start] + cleaned[pgp_pk_end:]
        except ValueError as ve:
            pass

        # finally, try to remove the signed message header
        pgp_msg = cleaned.index('-----BEGIN PGP SIGNED MESSAGE-----')
        pgp_hash = re.search('Hash:(.)+\n', cleaned)

        if pgp_hash is not None:
            first_hash = pgp_hash.span(0)
            if first_hash[0] == pgp_msg + 35:
                #if we found a hash designation immediately after the header, strip that too
                cleaned = cleaned[:pgp_msg] + cleaned[first_hash[1]:]
            else:
                #just strip the header
                cleaned = cleaned[:pgp_msg] + cleaned[pgp_msg + 34:]
        else:
            cleaned = cleaned[:pgp_msg] + cleaned[pgp_msg + 34:]

        workcopy = cleaned
    except ValueError as ve:
        pass

    # strip FullDisclosure footer from content; may have multiples if replying to thread
    footers = [m.start() for m in re.finditer('_{47}', workcopy)]
    for f in reversed(footers):
        possible = workcopy[f:f+190]
        lines = possible.splitlines()
        if(len(lines) == 4
            and lines[1][0:15] == 'Full-Disclosure'
            and lines[2][0:8] == 'Charter:'
            and lines[3][0:20] == 'Hosted and sponsored'):
            workcopy = workcopy[:f] + workcopy[f+213:]
            continue

        if(len(lines) == 4
            and lines[1][0:16] == 'Sent through the'
            and (lines[2][0:17] == 'https://nmap.org/' or lines[2][0:16] == 'http://nmap.org/')
            and lines[3][0:14] == 'Web Archives &'):
            workcopy = workcopy[:f] + workcopy[f+211:]
            continue


        possible = workcopy[f:f+146]
        lines = possible.splitlines()
        if(len(lines) == 3
            and lines[1][0:15] == 'Full-Disclosure'
            and lines[2][0:8] == 'Charter:'):
            workcopy = workcopy[:f] + workcopy[f+146:]
            continue

    return workcopy


def usage():
    print(main.__doc__)


def main(argv=None):
    """
    Args:
        -y <year>, parse entire year, e.g., -y ./2011
        -d <directory>, parse entire directory, e.g., -d ./2011_01
        -f <filename>, parse single raw file, e.g. -f ./2011_Jan_0.raw.html
    """
    if argv is None:
        argv = sys.argv

    try:
        opts, args = getopt.getopt(argv[1:], 'd:f:y:')
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
            if o in ('-y'):
                for subdir in os.listdir(a):
                    parse_month_folder(os.path.join(a,subdir))
                sys.exit(0)
            elif o in ('-d'):
                parse_month_folder(a)
                sys.exit(0)
            elif o == '-f':
                parse_reply(a)
        except Exception as e:
            print(e)
            usage()
            sys.exit(2)


if __name__ == "__main__":
    main()