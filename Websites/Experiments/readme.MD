# Survey-Logger

## Webapp

This webapp was created to collect opinion on e-mail threads being or not
about cybersecurity attacks using known cybersecurity knowledge sources.

The interface was designed as to present 3 types of contents:

- One e-mail thread possible related to a cybersecurity attack from a mailing list.
- One entry from a Knowledge Source ontology about one general category of cyber security attack.
- A set of 4 questions overall assessing if the sampled e-mail thread and knowledge source entry relate or not.

The interface of the webapp is designed such that for both the randomly chosen e-mail thread and knowledge source users must:

- Click e-mail replies of the one chosen thread for reading them.
- Resize the e-mail reply box to facilitate reading the necessary content for comparison.
- Scroll content as needed.

## Post-Analysis

The set of actions above are unobtrusively logged as the user perform these actions,
and later used to infer what content the user deemed relevant to answer the survey.
The relevant content, in turn, is used to score word weights for tunning the topic
models used by PERCEIVE.

# Getting Started

Current stage of this project is, very roughly, a prototype implemented using
`Django` and `sqlite3`.

After installing both dependencies:

1. Git clone PERCEIVE
2. From the top folder: `cd perceive/Websites/Experiments`
3. Run `python manage.py runserver` to execute on localhost.
4. Copy and paste the localhost IP on your preferred browser.
