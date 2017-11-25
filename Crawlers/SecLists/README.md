# seclists_crawler_raw.py

Downloads raw html files from seclists.org, by year, month, or individual id.

## Args:

    Required: 
    -l <listname>, e.g., fulldisclosure, bugtraq
    
    Pick one of:     
    -y <year>, download entire year, e.g., -y 2011

    -m <yearmonth>, download specific month, e.g. -m 201101 for Jan. 2011

    -i <yearmonth-id>, download specific message, e.g., -i 201101-0

Example usage: `$ python seclists_crawler_raw.py -l fulldisclosure -y 2017`

## Library
For more flexiblity, import this library, and use the following functions:

#### `dl_index(year, month, path)`

Download month's index file.

Args:
* year: str, e.g. "2017"
* month: str, e.g., "Jan"
* path: str

Returns:
str: filename that contents were written into


#### `dl_message(year, month, id, path)`

Download individual message.

Args: 
* year: str, e.g. "2017"
* month: str, e.g., "Jan"
* id: str, e.g., "0"
path: str


#### `dl_month(year, month)`

Download entire raw html contents of month.
Contents will be written to subdir, e.g. ./2017_01

Args: 
* year: int
* month: int (Jan = 1)

#### `dl_range(year_start, month_start, year_end, month_end)`

Download multiple months, using start & end year/months.
See dl_month for contents.

Args:
* year_start: int
* month_start: int (Jan = 1)
* year_end: int
* month_end: int (Jan = 1)

