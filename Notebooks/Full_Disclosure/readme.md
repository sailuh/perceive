# Overview of files and supplementary materials

## 1. Files hosted in this github folder

This notebook includes a _data_ folder for sample files. In the [data/input](data/input) folder, the 2008 author and node lists are included. These lists are used in notebook section **2.4** to generate the 2008 network graph. The [data/output](data/output) folder contains the graph exported in section **5.2.2** of the notebook.

The _img_ folder includes graphics used in the notebook. These include the organized [Full Disclosure over time](img/network_over_time) images used in section **3.1** and the [blob subgraphs](img/blob_subgraphs) from section **5.4.1**.

## 2. Supplementary materials

### 2.1 Edge and node lists

The original **edge and node lists** used to generate the Full Disclosure graphs are [available on mega](https://mega.nz/#F!CUEByR5I!GY56GzTpYz68IlTqj4aQNQ!fR8jFLxL) originally used to generate all the networks.

### 2.2 Zip file

A zip file of supplementary material is also [available on mega](https://mega.nz/#!egFlzQ4A!Wf_V4UnyfoCNCE_ltT9F4veR-B8ep2uSmsOB-Z-K9tA). 

The following contents are included:

* _presentation_video_ folder includes a video of the presentation describing this project and the powerpoint slides used for the presentation.
* _images_ folder includes an animated GIF version of the Full Disclosure network for the years 2002-2016. Images were generated in Gephi from edge and node lists provided at https://mega.nz/#F!CUEByR5I!GY56GzTpYz68IlTqj4aQNQ!fR8jFLxL
* _images/igraph_image_output_ folder includes sample images plotted in igraph; subgraphs 0-5 of the 2008 "blob" show a different rendering from the approach finally used in the notebook, with 6 subcommunities generated rather than 8. Each variation in the specific number of subcommunities has similar results.
* _graphml/gephi_generated_ folder includes graphml files after the original node and edge lists were loaded into Gephi, analyzed manually, and then exported. These provide a potential shortcut for analysis in igraph or elsewhere, but were eventually dropped from my final work.
* _graphml/igraph-generated_ folder includes graph data for subcommunities of the "blob" as developed in igraph and described in notebook section **5.4**. These graphs were used in Gephi to create images as seen in the notebook and to do manual textual analysis.

