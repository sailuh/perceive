# R Full Disclosure Reply to Thread Aggregator 

TO-DO. Currently functional, but code contains multiple responsabilities. Header still needs to updated by head to serve as input to Python Full Disclosure to Thread Aggregator (below). Will be fixed on following commits.

# Python Full Disclosure Reply to Thread Aggregator 

The `fd_to_thread.py` script group the the collected e-mail replies by `fd_group_reply_by_thread.R` into thread files. The thread files are then used for similarity analysis, instead of the individual replies. The pre-processing is done to facilitate topic extraction, under the assumption that replies that share the same subject line (i.e. an e-mail thread) share the same discussion. 

## Other Important Notes

 
 - The header of the .csv file or order of columns is not important, provided a `threadID` and `reply_IDs` column exists. 
 
 - The script will assume the replies listed per thread on the .csv to be ordered by their ID (which in turn reflects the order of the replies) when grouping the reply body. `fd_group_reply_by_thread.R` already order the replies, so no further pre-processing is needed.

 - Currently, the generated files **do not** include the title of the threads e-mails. 

 - Originally, we grouped in threads replies for one year at a time, but this restriction is not imposed by the code.

## Dependencies

fd_group_reply_by_thread.R

## How to Use 

```
<folder with all .txt replies output from fd_group_reply_by_thread.R> <.csv file output from fd_group_reply_by_thread.R> <output folder>`
```
