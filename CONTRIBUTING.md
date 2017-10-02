# For Contributors

We'd love your help! This doc covers how to become a contributor and submit code to the project.

## 1. Follow the coding style

We use Google Style Guide for our code, which is mainly in `Python` and `R`. The items below highlight some starting points, but you should ensure your code also comply to the associated coding style unless otherwise noted in **bold** below.

### [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

 - [The way you open and close data files.](https://google.github.io/styleguide/pyguide.html?showone=Naming#Files_and_Sockets)
 - [How you name variables, functions classes, methods, etc.](https://google.github.io/styleguide/pyguide.html?showone=Naming#Naming)
 - [Your code documentation, in particular functions.](https://google.github.io/styleguide/pyguide.html?showone=Comments#Comments)
 - [Modules and usage.](https://google.github.io/styleguide/pyguide.html?showone=Imports#Imports)
 - [Code identation.](https://google.github.io/styleguide/pyguide.html?showone=Indentation#Indentation)
 - [If you happen to be a Vim, Google also provide a settings file.](https://google.github.io/styleguide/google_python_style.vim)

### [Google R Style Guide](https://google.github.io/styleguide/Rguide.xml)

 - [File Names](https://google.github.io/styleguide/Rguide.xml#filenames)
 - [Function Definition](https://google.github.io/styleguide/Rguide.xml#functiondefinition)
 - [Function Documentation](https://google.github.io/styleguide/Rguide.xml#functiondocumentation)
 - **Identation**: Use 4 spaces, for consistency with Python style.
 - [Assignment](https://google.github.io/styleguide/Rguide.xml#assignment)
 - [Else](https://google.github.io/styleguide/Rguide.xml#else)
 - [Braces](https://google.github.io/styleguide/Rguide.xml#curlybraces)

## 2. Python and R Notebooks

Writing Python and R Notebooks is a different **program paradigm** than writing scripts, and borrows much from [**Literate Programming**](https://en.wikipedia.org/wiki/Literate_programming), introduced by [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth), being one of the most important distinctions as follows:

> A program is given as an explanation of the program logic in a natural language, such as English, interspersed with snippets of macros and traditional source code, from which a compilable source code can be generated.

Writing good Python and R notebooks have much more to do with writing good essays and storytelling than programming. If you are contributing to PERCEIVE code notebooks, we will not expect you to be proficient in doing so, but be eager to work with us to brush up your notebook, if necessary.

Some great examples of contributed notebooks to PERCEIVE to serve as inspiration are as follows:

 * [Full Disclosure Social Network Analysis](https://github.com/jeffgerhard), by [Jeff Gerhard](https://github.com/jeffgerhard).
 * [CAPEC Foaamtree Visualization -- With No Plots](https://github.com/sailuh/perceive/blob/master/Notebooks/CAPEC/Introduction/capec_introduction.ipynb) or [CAPEC Foamtree Visualization -- With Plots](http://nbviewer.jupyter.org/github/sailuh/perceive/blob/4bbdd6a74eb72f085ecd99c640f35d1735fa8108/Notebooks/CAPEC/Introduction/capec_introduction.ipynb), by [Vignesh Rajan](https://github.com/vigneshrajan94).
 * [Full Disclosure Word and Vocabulary Distributions](https://github.com/sailuh/perceive/blob/master/Notebooks/Full_Disclosure/full_disclosure_corpus_statistics.ipynb) or [Full Disclosure Word and Vocabulary Distributions - With Plots](http://nbviewer.jupyter.org/github/sailuh/perceive/blob/4bbdd6a74eb72f085ecd99c640f35d1735fa8108/Notebooks/Full_Disclosure/full_disclosure_corpus_statistics.ipynb), by [Shashank Kava](https://github.com/kavashashank).
 * And maybe in the future, yours!

Please note most of these Notebooks were semester-long contributions. Your initial Python Notebook can be a much smaller contribution, such as one section of the listed Notebooks. Afterall, it is ok to be simple as possible, not simpler! A future contributor will still need to see some basic structure and narrative in your code notebook to make sense of what you are trying to say.

## 3. Learn about the architecture

Most of PERCEIVE is currently organized in **Python Notebooks and R Notebooks**, as most of our code is experimental. Nonetheless, some fronts are well-defined:

 - [**Source Crawlers**](https://github.com/sailuh/perceive/tree/master/Data_Collection): Not all data sources are readily available for the source to be used in this project code. We currently have Crawlers for:
    - Mailing Lists: Seclists
    - Knowledge Sources: CAPEC, CWE, and CVE Details (CVE Mitre and NVD provide well-formatted XML representations of their Raw Data).
 - [**Database**](https://github.com/sailuh/perceive/tree/master/Database): It is currently undergoing work to define a schema for all the source, parsed and analyzed data of the project. Currently, the data lives in a private Mega Upload account. Note: Due to the nature of the data, Google Drive will (incorrectly) state the data has viruses. However, this is only true in the harmful sense if you intentionally execute the code.
 - [**CAPEC Foamtree Visualization**](https://github.com/sailuh/perceive/tree/master/Notebooks/CAPEC): Interactive visualization to explore older versions of Capec as a Tree.
 - [**Topic Models**](https://github.com/sailuh/perceive/tree/master/Notebooks/LDA): We currently have one implementation of LDA VEM, as proposed by Blei et al. (2003), and associated utility functions and visualizations to explore Topics in the Source Crawlers at a **specific point in time**.
 - [**Topic Flow**](https://github.com/sailuh/topicflow): Hosted as a separate project, we have a working version fork of Topic Flow. Our fork **includes** the data pipeline necessary to generate the visualizations in the forked tool, and is useful to observe topics **over time**.

## 4. Contributing code

We have a strict format to submit code (patches) to this project, including but not limited to submitting pull requests through branches, using a specific branch and commit labels.

If you wish to collaborate but do not have the time availability to learn about Git and Github, please open an issue and we can try to work it out.


If you are unsure on how to perform the below steps or are new to Git and Github, please see the **Learning Resources** (Section 5.) at the bottom of this document for some learning material, including free video lectures.

The step-by-step process is as follows:

1. Submit an issue describing your proposed change to the repo in question.
   1. Please make sure you understand and agree on **what** files will be submitted, **where** in the repository, and **on what file format** to use **before** submitting a Pull Request.
   1. It is ok to upload example files or images to clarify your point during an issue discussion, but it is **not** ok to submit entire datasets to either issue or as pull requests. Data should be hosted separately and discussed in the issue where it will be hosted in PERCEIVE, if necessary. Your code, if not requesting data directly from PERCEIVE database, should clearly indicate the **final** location where the data used for your analysis is located, so others can **reproduce your results by re-running your Notebook**.
1. The repo owner will respond to your issue promptly.
1. Fork the repo, develop and test your code changes.
   1. After cloning your fork, **before starting to modify any file**, please create a topic branch. A topic branch has the following format: `<issue-id>-<meaningful name associated to **what** you are trying to do>`.
      * Example: If the issue ID #27 is about creating histograms of full disclosure word counts, then your branch should be `27-full-disclosure-word-count-histogram` (note the # symbol is **not** included in the branch name).
   1.  Please **include the issue ID in all commits** (e.g. #27). Your commits should follow the format `<issue-id>-<meaningful commit name>`.
       * Example: Continuing the example above, as you work in branch 27-full-disclosure-word-count-histogram, one of your commits may be `#27 parse input data into data frames`, followed by `#27 plot and specify histogram ranges`. Notice that, different from topic branches, **the # symbol must be included** in all commit labels.
1. Ensure that your code adheres to the existing Google code style in the sample to which you are contributing (see Section **1.**).
1. Submit a pull request using the created topic branch in step 3.1.
   1. Git will prompt the commit message to be used as the title of your Pull Request. **Please remove the issue code from the pull request title**, as it becomes confusing to read with the Pull Request own number.
   1. Ensure that after clicking `New Pull Request` you select the correct branch of your fork. Ensure you are **not** using your fork's master branch, but instead the topic branch.
1. Please note the concept behind Github Pull Requests is synchronizing the branch from your fork to the Pull Request interface. As such, please refrain from making modifications to the associated topic branch after submitted. The repo owner will review your pull request and let you know if any further modifications are necessary.
   1. One common request is to `git squash` some of the commits, or `re-label` them.
   1. Please avoid **deleting your fork once a Pull Request is submitted**. Doing so will forcefully close the Pull Request, breaking the discussion about the same Pull Request in several different new ones. This makes it much more difficult in the future for new contributors to follow-up a related contribution discussion. If needed, please contact the repo owner in the associated issue if you need help instead of deleting it.

## 5. Learning Resources

The videos listed below are available for free by Udacity and may require an account to be created.

If you are completely new to Git, we recommend the [introdutory Git course](https://www.udacity.com/course/version-control-with-git--ud123) by Udacity first. This course will teach you how to use git on your computer, but not to contribute code to this repository.

If you are comfortable using git locally, but are new to Github, [we recommend the follow-up course by the same author, also from Udacity](https://www.udacity.com/course/github-collaboration--ud456).

Going through both courseworks should take less than a weekend if following only the videos, or no more than 1 week and a half if doing the homework of both courses and videos.

If you are used to Git and Github, but only need to brush up or review material as required, here are the relevant lecture pointers:

- [Create a Pull Request](https://classroom.udacity.com/courses/ud456/lessons/e295524f-87b6-4981-af74-6b20231dc7c1/concepts/9c0c0dd5-225e-44a4-9257-a584a7829207)
- [Stay in Sync with Code Repository](https://classroom.udacity.com/courses/ud456/lessons/e295524f-87b6-4981-af74-6b20231dc7c1/concepts/48825e17-72c6-4c3e-9c98-1add66bf1c86)
- [Commit Squash and Relabel](https://classroom.udacity.com/courses/ud456/lessons/e295524f-87b6-4981-af74-6b20231dc7c1/concepts/3d9fb9c8-47bc-4dbd-a6d3-09b006be24e4)


## 6. Troubleshooting

- If you are on Windows and having user authentication problems, [you may need to remove saved username and passwords to git from your Windows Keychain](https://stackoverflow.com/questions/17857283/permission-denied-error-on-github-push).


## 7. Useful Commands

- `git log --oneline --abbrev-commit --all --graph --decorate`
