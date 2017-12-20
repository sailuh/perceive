
# CWE 

**Introduction**

This folder presents current undergoing work in understanding, visualizing and exploring CWE.

There are current 3 main fronts in this area of the project:

Understanding the overall structure of CWE and it's various fields [CWE Introduction](https://github.com/sailuh/perceive/blob/master/Notebooks/CWE/cwe_introduction.ipynb).
Visualizing previous year fields (See CWE Visualization Notebook).
Visualizing how CWE structure changes over time.

**CWE Fields**

Undergoing Work. Please see the associated notebook for more details.

**CWE Visualization**

The visualization component is mainly a interactive visualization of what is already provided by the View 'Research Concepts' on CWE website. However, such visualization is only available on the website for the more curent version. Old versions can only be seeing through XML files. The XML files, however, are not a single but 4 tree structures.

To unify the different tables into 1 and provide an easy way to understand past mechanisms of attacks views as a single interactive tree, a script was created to ingest the .XML files as made available on CWE website for all versions, transform into JSON, and leverage CarrotFoamtree JS visualization.

For more details on how the visualization is constructed, see the associated notebook.

**How to run**

The script is available in this folder as cwe_final.py. For example, to execute it:
cwe_final.py cwec_v2.10.xml  carrotsearch.foamtree-new.js
Replacing cwec_v2.10.xml for any other XML file as available on CWE Website should result in the respective version foamtree.

**Known Limitations**

Due to a different XML structure in cwec_v3.0.xml, cwe_final.py is unable to extract the necessary content to generate the visualization.
Also, since attributes in CWE have mutiple parent nodes, it is difficult to create a edge and node list.

**CWE Evolution**

Undergoing work. See the Difference Report Notebook for an early discussion.
