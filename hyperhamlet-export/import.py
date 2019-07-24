import os
from typing import List, Set, Dict, Tuple, Optional
from pprint import pprint
import argparse
import json
from jsonschema import validate
from knora import KnoraError, knora, BulkImport
import requests

# Regex library
import re
# csv library
import csv
# JSON library
import json

# Gets authors data from json
with open('json/author.json', 'r') as a:
    allAuthors = json.load(a)

# Gets books data from json
with open('json/book.json', 'r') as b:
    allBooks = json.load(b)

####################

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", type=str, default="http://0.0.0.0:3333", help="URL of the Knora server")
parser.add_argument("-u", "--user", default="root@example.com", help="Username for Knora")
parser.add_argument("-p", "--password", default="test", help="The password for login")
parser.add_argument("-P", "--projectcode", default="0826", help="Project short code")
parser.add_argument("-O", "--ontoname", default="teimww", help="Shortname of ontology")

args = parser.parse_args()

con = knora(args.server, args.user, args.password)
schema = con.create_schema(args.projectcode, args.ontoname)

ww_bulk_xml = "./bulk-output.xml"
ww_bulk_object = BulkImport(schema)


# Open csv sheet with the entries
with open('let-them-come.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    names = []
    createdAuthors = {}
    line = 0

    for row in csv_reader:

        # Skip first row because of column title in excel sheet
        if line is not 0:
            names = row[2].split(" / ")

            # Iterates through the names per entry
            for name in names:

                if name in createdAuthors:
                    print("doublication")
                else:
                    # CREATE RESOURCE
                    line += 1

                    key = "{} {}".format(allAuthors[name]["firstName"], allAuthors[name]["lastName"])

                    # Object which will be added to Knora.
                    # It contains all the information needed which was defined in the data_model_definition_authors
                    person = {
                        "firstName": allAuthors[name]["firstName"],
                        "lastName": allAuthors[name]["lastName"],
                        "hasSex": "male"
                    }

                    if "description" in allAuthors[name]:
                        person["description"] = allAuthors[name]["description"]

                    if "birthExact" in allAuthors[name]:
                        person["birthDate"] = "GREGORIAN:{}".format(allAuthors[name]["birthExact"])
                    elif "birthSpanStart" in allAuthors[name]:
                        person["birthDate"] = "GREGORIAN:{}:{}".format(allAuthors[name]["birthSpanStart"],
                                                                       allAuthors[name]["birthSpanEnd"])

                    if "deathExact" in allAuthors[name]:
                        person["deathDate"] = "GREGORIAN:{}".format(allAuthors[name]["deathExact"])
                    elif "deathSpanStart" in allAuthors[name]:
                        person["deathDate"] = "GREGORIAN:{}:{}".format(allAuthors[name]["deathSpanStart"],
                                                                       allAuthors[name]["deathSpanEnd"])

                    if "floruitExact" in allAuthors[name]:
                        person["activeDate"] = "GREGORIAN:{}".format(allAuthors[name]["floruitExact"])
                    elif "floruitSpanStart" in allAuthors[name]:
                        person["activeDate"] = "GREGORIAN:{}:{}".format(allAuthors[name]["floruitSpanStart"],
                                                                        allAuthors[name]["floruitSpanEnd"])

                    ww_bulk_object.add_resource(
                        "person",
                        allAuthors[name]["id"],
                        "person label",
                        person
                    )

                    createdAuthors[key] = allAuthors[name]

                # if name in allAuthors:
                #     print(allAuthors[name])
                # else:
                #     print("NO", "|" + name + "|")
        else:
            line += 1

    # countOfAuthors = 1
    # for author in createdAuthors:
    #     print(createdAuthors[author], countOfAuthors)
    #     countOfAuthors += 1

print("END")

BULKIMPORT_API_ENDPOINT = "http://localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0826"
headers = {"Content-Type": "application/xml"}

ww_bulk_object.write_xml(ww_bulk_xml)
ww_bulk_xml_string = open(ww_bulk_xml).read().encode("utf-8")
r = requests.post(BULKIMPORT_API_ENDPOINT, data=ww_bulk_xml_string, headers=headers, auth=(args.user, args.password))
pprint(r.json())
