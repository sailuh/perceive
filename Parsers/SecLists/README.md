# seclists_reply_parse.py

Parses seclists.org raw.html files into the following subfiles:
* .reply.body.txt

    Full content of reply (without seclists.org wrapper page html)
* .reply.title_body.txt

    Title of reply + full content of reply
* .reply.body_no_signature.txt

    Full content of reply, with attempt to strip out signature
* .reply.title_body_no_signature.txt

    Title of reply + above
* .reply.body_tags.txt

    File containing analysis of tags in raw.html file. Content is in JSON format.
        
        * tags: html tag types found in reply, along with count
        * sites: domains of sites referenced in reply, along with count
        
    Example: `{"tags": {"pre": 2, "a": 1}, "sites": {"pentestmag.com": 1}}`

## Args

    -d <directory>, parse entire directory, e.g., -d ./2011_01

    -f <filename>, parse single raw file, e.g. -f ./2011_Jan_0.raw.html

Example usage: `$ python seclists_reply_parse.py -d ./2011_01`

## Library
For more flexiblity, import this library, and use the following functions:

#### `parse_month_folder(path)`

Parse .raw.html files

Args:
* path: str, directory containing .raw.html files


#### `parse_reply(filename)`

Parse individual message.

Args: 
* filename: str

# seclists_index_parse.py
Parses month index raw.html into csv file. This also pulls data from the referenced replies, to obtain full date and author information.

## CSV Format
The CSV file contains five columns:

* id
* title: Subject of reply
* date: e.g. 2005-01-05T00:53:02+00:00 format
* author: Name and email, as supplied by author
* parent: the id of the parent thread email; blank if this is a parent thread

## Args

    -f <filename>, parse single raw file, e.g. -f ./2011_Jan_0.raw.html

Example usage: `$ python seclists_index_parse.py -f ./2011_Jan_0.raw.html`
