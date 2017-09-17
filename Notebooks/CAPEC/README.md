# CAPEC 

## Introduction

This folder presents current undergoing work in understanding, visualizing and exploring [CAPEC](http://capec.mitre.org/). 

There are current 3 main fronts in this area of the project:

1. Understanding the overall structure of CAPEC and it's various fields. (See [CAPEC Introduction Notebook](https://github.com/sailuh/perceive/tree/master/Notebooks/CAPEC/Introduction)). 
2. Visualizing previous year fields (See [CAPEC Visualization Notebook](https://github.com/sailuh/perceive/tree/master/Notebooks/CAPEC/Visualization)).
3. Visualizing how CAPEC structure changes over time. 

## CAPEC Fields

Undergoing Work. Please see the associated notebook for more details. 

## CAPEC Visualization  

The visualization component is mainly a interactive visualization of what is already provided by the View 'Mechanisms of Attack' on CAPEC website. However, such visualization is only available on the website for the more **curent version**. Old versions can only be seeing through XML files. The XML files, however, are not a single but 4 tree structures. 

To unify the different tables into 1 and provide an easy way to understand past mechanisms of attacks views as a single interactive tree, a script was created to ingest the .XML files as made available on CAPEC website for all versions, transform into JSON, and leverage [CarrotFoamtree JS](https://carrotsearch.com/foamtree/) visualization. 

For more details on how the visualization is constructed, see the associated notebook.

### How to run

The script is available in this folder as `capec_foamtree_view.py`. For example, to execute it:

``` 
capec_foamtree_view.py data/capec_v2.9.xml carrotsearch.foamtree.js
```

Replacing capec_v2.9.xml for any other XML file as available on [CAPEC Website](http://capec.mitre.org/data/) should result in the respective version foamtree.

The script is also able to export the json data output which is used by foamtree, as well as an edgelist representation of the hierarchy to plot in tools such as [Gephi](https://gephi.org/). Please see the script help page for more details (`capec_foamtree_view.py -h`). 

### Known limitations

Due to older versions of CAPEC using a different XML structure, `capec_foamtree_view.py` may be unable to extract the necessary content to generate the visualization.

## CAPEC Evolution

Undergoing work. See the [Difference Report](https://github.com/sailuh/perceive/tree/master/Notebooks/CAPEC/Difference_Report) Notebook for an early discussion.  
