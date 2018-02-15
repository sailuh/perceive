# PERCEIVE

PERCEIVE is a project incubator inspired by [Apache Incubator](http://incubator.apache.org/) and [Stack Exchange's Area 51](https://area51.stackexchange.com/). It serves as a **staging zone** repository for the project early ideas, most of which done in either Python or R Notebooks by one of the project's [contributors](https://github.com/sailuh/perceive/graphs/contributors). All projects share the common goal to support the identification of software vulnerabilities in the "wild," and function as different components of a single system to achieve this goal. 

## Project List 

| Project                     | Description                                                                                                   | Dependencies               | Contributors                                  | Reviewer       | Semesters of Activity                          |
|-----------------------------|---------------------------------------------------------------------------------------------------------------|----------------------------|-----------------------------------------------|----------------|------------------------------------------------|
| Crawlers and Corpus Parsers | A set of crawlers for data acquisition and parsers for different corpus setups intended for topic modelling.  | None                       | Pal Doshi, Karthik Jallawaram, Jarret Lee, Shashank Kava     | Carlos Paradis | Fall 2016, Fall 2017                           |
| Graph Parsers               | Scripts to parse corpus and ontologies into graphs for network analysis                                       | Crawler and Corpus Parsers | Jeff Gerhard, Vignesh Rajan, Vaishnavi Vel    | Carlos Paradis | Spring 2017, Fall 2017                         |
| Logger Website              | Website to survey and log user interaction of software vulnerabilities evaluation.                            | Crawler and Corpus Parsers | Karishma Ghiya                                | Carlos Paradis | Spring 2017                                    |
| Data Storage                | Relational Data Models of Mitre's Software Vulnerabilities Ontologies, and Hadoop Ecosystem Case Study        | Crawler and Corpus Parsers | Kanoe Dudoit, Vinicius Gesteira, Yue Liu      | Carlos Paradis | Spring 2017, Fall 2017                         |
| Topic Flow                  | Pipeline for topic modeling, and topic flow                                                                   | Crawler and Corpus Parsers | Carlos Paradis                                | Rick Kazman    | Fall 2016, Spring 2017, Summer 2017, Fall 2017 |
| Topic Viz                   | Fork of LDAvis R Package to visualize topics from LDA.                                                        | Topic Flow                 | Carlos Paradis                                | Rick Kazman    | Fall 2017                                      |
| Topic Flow Viz              | Fork of Topic Flow Viz to visualize topic flows.                                                              | Topic Flow                 | Freddie Zhang                                 | Carlos Paradis | Fall 2017                                      |
| Ontology Viz                | Foamtree Parser to visualize older XML versions of CWE and CAPEC.                                             | Crawler and Corpus Parsers | Akshaya Jayaram, Vignesh Rajan, Vaishnavi Vel | Carlos Paradis | Spring 2017, Fall 2017                         |

## Usage and Documentation

For usage instructions, please refer to the project README or Python/R Notebook. We are in the process of moving some of the graduated projects into a separate GitHub project under `sailuh` to facilitate usage and documentation.

## Known Issues

Please see the list of issues on this project for known bugs and new feature requests.

## Contributing

If you would like to contribute (thanks!), we recommend you first open an issue to discuss the contribution, and we will get back to you ASAP! By contributing to this project, you agree that your contributions will be licensed under the project's license. For more details, see CONTRIBUTING.md for code style guide, branching and pull requests format.

## License

Feel free to use this project code. Code dependencies are still being assessed to decide on a license.

## How to cite 

If you are using perceive, please cite our [paper](https://scholarspace.manoa.hawaii.edu/bitstream/10125/41885/1/paper0736.pdf):

```
@inproceedings{DBLP:conf/hicss/ChenKMW17,
  author    = {Hong{-}Mei Chen and
               Rick Kazman and
               Ira Monarch and
               Ping Wang},
  title     = {Can Cybersecurity Be Proactive? {A} Big Data Approach and Challenges},
  booktitle = {50th Hawaii International Conference on System Sciences, {HICSS} 2017,
               Hilton Waikoloa Village, Hawaii, USA, January 4-7, 2017},
  year      = {2017},
  crossref  = {DBLP:conf/hicss/2017},
  url       = {http://aisel.aisnet.org/hicss-50/st/cybersecurity_and_sw_assurance/4},
  timestamp = {Fri, 10 Mar 2017 15:08:28 +0100},
  biburl    = {http://dblp.org/rec/bib/conf/hicss/ChenKMW17},
  bibsource = {dblp computer science bibliography, http://dblp.org}
}
```
