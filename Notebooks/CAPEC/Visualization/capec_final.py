import csv
import json
import xml.etree.ElementTree as ET
import sys
import os
import argparse

parser = argparse.ArgumentParser(description = 'CAPEC XML visualisation program.')
parser.add_argument('xml_filepath', help = 'path of the capec xml file')
parser.add_argument('javascript_filepath', help = 'path of the carrotsearch.foamtree.js file')
parser.add_argument("--json", help = "export .json file", action = "store_true")
parser.add_argument("--gephi", help = "export node and edge table for gephi visualisation", action = "store_true")
args = parser.parse_args()

filepath = args.xml_filepath
javascript_path = args.javascript_filepath

CAPEC_xml = filepath.split(os.sep)[-1]
CAPEC_version = CAPEC_xml[:-4]
CAPEC_json = CAPEC_version + ".json"
CAPEC_html = CAPEC_version + ".html"
CAPEC_csv_edgelist = CAPEC_version + " [Edges].csv"
CAPEC_csv_nodelist = CAPEC_version + " [Nodes].csv"
 
CAPEC_entries = list()

CAPEC_tree = ET.parse(filepath)
CAPEC_root = CAPEC_tree.getroot()

def remove_commas(string):
    comma_free_string = ''
    temp_string = string.split(',')
    for i in temp_string:
        comma_free_string+=i
    return comma_free_string

for attack_pattern in CAPEC_root[0][0]:
    for parameter in attack_pattern:
        if parameter.tag=="{http://capec.mitre.org/capec-2}Relationship":
            capec_id = parameter[3].text
            child_of = '1000'
            for category in CAPEC_root[1]:
                if category.attrib['ID']==capec_id:
                    capec_name = remove_commas(category.attrib['Name'])
                    temp_list = list()
                    temp_list.extend((capec_id,capec_name,child_of))
                    CAPEC_entries.append(temp_list)



for attack_pattern in CAPEC_root[1]:
    if attack_pattern.attrib['Status']!="Deprecated":
        for parameter in attack_pattern:
            if parameter.tag=="{http://capec.mitre.org/capec-2}Relationships":
                for relationship_parameter in parameter:
                    if relationship_parameter[2].text=="HasMember":
                        child_of = attack_pattern.attrib['ID']
                        capec_id= relationship_parameter[3].text
                        for attack_pattern_matcher in CAPEC_root[2]:
                            if attack_pattern_matcher.attrib['ID']==capec_id:
                                capec_name= remove_commas(attack_pattern_matcher.attrib['Name'])
                        temp_list = list()
                        temp_list.extend((capec_id,capec_name,child_of))
                        CAPEC_entries.append(temp_list)



#CAPEC_root[2] is used to select capec:Attack_Patterns
for attack_pattern in CAPEC_root[2]:
     if attack_pattern.attrib['Status']!="Deprecated":
        for parameter in attack_pattern:
            if parameter.tag=="{http://capec.mitre.org/capec-2}Related_Attack_Patterns":
                for related_attack_pattern_parameter in parameter:
                    if related_attack_pattern_parameter[2].text=="ChildOf":
                        capec_id= attack_pattern.attrib['ID']
                        capec_name= remove_commas(attack_pattern.attrib['Name'])
                        child_of= related_attack_pattern_parameter[3].text
                        temp_list = list()
                        temp_list.extend((capec_id,capec_name,child_of))
                        CAPEC_entries.append(temp_list)


def jsonify(number):
    main_list = list()
    for row in CAPEC_entries:
        parent_id = str(number)
        if row[2]==parent_id:
            member_dict = dict()
            member_dict["label"] = str(row[0]) + ' - ' + str(row[1])
            member_dict["weight"] = 1
            member_dict["groups"] = jsonify(row[0])
            main_list.append(member_dict)
        else:
            continue
    return main_list

def gephi_export(number): 
    fe = open(CAPEC_csv_edgelist, 'w')
    HEADe = "Source,Target,Type,id,label,timeset,weight\n"
    fe.write(HEADe)
    
    fn = open(CAPEC_csv_nodelist, 'w')
    HEADn = "Id,Label,timeset\n"
    fn.write(HEADn)

    capecid_id_dict = dict()
    capecid_id_dict[str(number)]='0'
    node = '{o1},{o2},{o3}\n'.format(o1='0',o2=number,o3='')
    fn.write(node)
    id_counter = 1
    for row in CAPEC_entries:
        node = '{o1},{o2},{o3}\n'.format(o1=id_counter,o2=row[0],o3='')
        fn.write(node)
        capecid_id_dict[row[0]]=id_counter
        id_counter+=1

    type_value = "Directed"
    edge_id_counter = 0
    for row in CAPEC_entries:
        if row[2] in capecid_id_dict:
            source_value = int(capecid_id_dict[row[2]])
            target_value = int(capecid_id_dict[row[0]])
            edge = '{o1},{o2},{o3},{o4},{o5},{o6},{o7}\n'.format(o1=source_value,o2=target_value,o3=type_value,o4=edge_id_counter,o5='',o6='',o7=1)
            fe.write(edge)
            edge_id_counter+=1

def createHTML():
    foamtreetemplate1 = '''<!DOCTYPE html>
    <html>
      <head>
        <title>FoamTree Quick Start</title>
        <meta charset="utf-8" />
      </head>

      <body>
        <div id="visualization" style="width: 800px; height: 600px"></div>

        <script src="'''+ javascript_path +'''"></script>
        <script>
          window.addEventListener("load", function() {
            var foamtree = new CarrotSearchFoamTree({
              id: "visualization",
              dataObject:'''

    foamtreetemplate2 = '''});
          });
        </script>
      </body>
    </html>'''

    with open(CAPEC_html,'w') as outputfile:
        outputfile.write(foamtreetemplate1)
        for line in open(CAPEC_json):
            outputfile.write(line)
        outputfile.write(foamtreetemplate2)

def createJSON():
    with open(CAPEC_json,'w') as jsonfile:
        json.dump(CAPEC_dict, jsonfile)
    jsonfile.close()

CAPEC_dict = dict()
CAPEC_dict["groups"]=jsonify(1000)
createJSON()
createHTML()

if args.gephi:
    gephi_export(1000)

if args.json == False:
    os.remove(CAPEC_json)
