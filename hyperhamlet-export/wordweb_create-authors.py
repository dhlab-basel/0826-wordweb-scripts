import os
from typing import List, Set, Dict, Tuple, Optional
from pprint import pprint
import argparse
import json
from jsonschema import validate
from knora import KnoraError, knora, BulkImport
import requests

##### AUTHOR IMPORTS
import pymysql
import re
import csv

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

ww_bulk_xml = "./test-bulk-output.xml"
ww_bulk_object = BulkImport(schema)

#####################

try:
    conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # sql = "SELECT COUNT(*) FROM authors WHERE description LIKE '%b. %'"
    sql = "SELECT * FROM authors ORDER BY lastname"

    cursor.execute(sql)

    results = cursor.fetchall()

    count = 0
    allAuthors = {}

    for row in results:

        author = {'firstName': row['firstname'], "lastName": row["lastname"]}

        # Start with empty description
        description = ""

        if row["description"]:

            # birth = re.search("(?<=b\.\s)\d{4}(.*)", row["description"])
            birth = re.search("(.*)b\.\s(.*)", row["description"])
            # death = re.search("(?<=d\.\s)\d{4}(.*)", row["description"])
            death = re.search("(.*)d\.\s(.*)", row["description"])
            # floruit = re.search("(?<=fl\.\s)\d{4}(?!\-)(.*)", row["description"])
            floruit = re.search("(.*)fl\.\s(.*)", row["description"])
            # birthDeath = re.search("(.*)(\d{4})-(\d{4})(.*)", row["description"])
            birthDeath = re.search("(.*?)(\[(\d{4})-(\d{4})\]|(\d{4}))-(\[(\d{4})-(\d{4})\]|(\d{4}))(.*)", row["description"])

            if birth:

                birth_span = re.search("(\[(\d{4})-(\d{4})\]|(\d{4}))(.*)", birth.group(2))

                if birth_span.group(4) is None:
                    author["birthSpanStart"] = birth_span.group(2)
                    author["birthSpanEnd"] = birth_span.group(3)
                    # print("Not Exact Birth", birth_span.groups(), row)
                else:
                    author["birthExact"]= birth_span.group(1)
                    # print("Exact Birth", birth_span.groups(), row)

                # add description
                description = birth.group(1) + birth_span.group(5)

            elif death:

                death_span = re.search("(\[(\d{4})-(\d{4})\]|(\d{4}))(.*)", death.group(2))

                if death_span.group(4) is None:
                    author["deathSpanStart"] = death_span.group(2)
                    author["deathSpanEnd"] = death_span.group(3)
                    # print("Not Exact Death", death_span.groups(), row)
                else:
                    author["deathExact"] = death_span.group(1)
                    # print("Exact Death", death_span.groups(), row)

                # add description
                description = death.group(1) + death_span.group(5)

            elif floruit:

                floruit_span = re.search("((\d{4})-(\d{4})|(\d{4}))(.*)", floruit.group(2))

                if floruit_span is not None:

                    # print(floruit_span.groups())

                    if floruit_span.group(4) is None:
                        author["floruitSpanStart"] = floruit_span.group(2)
                        author["floruitSpanEnd"] = floruit_span.group(3)
                        # print("Not Exact Floruit", floruit_span.groups(), row["description"])
                    else:
                        author["floruitExact"] = floruit_span.group(1)
                        # print("Exact Floruit", floruit_span.groups(), row["description"])

                    # add description
                    description = floruit.group(1) + floruit_span.group(5)

            elif birthDeath:

                if birthDeath.group(3):
                    author["birthSpanStart"] = birthDeath.group(3)
                    author["birthSpanEnd"] = birthDeath.group(4)
                    # print("Span Birth: ", birthDeath.groups(), row)
                else:
                    author["birthExact"] = birthDeath.group(5)
                    # print("Exact Birth in Span: ", birthDeath.groups(), row)

                if birthDeath.group(7):
                    author["deathSpanStart"] = birthDeath.group(7)
                    author["deathSpanEnd"] = birthDeath.group(8)
                    # print("Span Death: ", birthDeath.groups(), row)
                else:
                    author["deathExact"] = birthDeath.group(9)
                    # print("Exact Death in Span: ", birthDeath.groups(), row)

                # add description
                description = birthDeath.group(1) + birthDeath.group(10)

            # add description to author after it has trimmed the string
            author["description"] = description.rstrip()

        # Create a key and add the author to the object
        key = "{} {}".format(author["firstName"], author["lastName"])
        allAuthors[key] = author

    conn.close()
    cursor.close()

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
                        blabla = {}
                    else:
                        # CREATE RESOURCE
                        line += 1

                        key = "{} {}".format(allAuthors[name]["firstName"], allAuthors[name]["lastName"])

                        person = {
                            "firstName": allAuthors[name]["firstName"],
                            "lastName": allAuthors[name]["lastName"]
                        }

                        if "description" in allAuthors[name]:
                            person["description"] = allAuthors[name]["description"]

                        if "birthExact" in allAuthors[name]:
                            person["birthDate"] = "GREGORIAN:{}".format(allAuthors[name]["birthExact"])
                        elif "birthSpanStart" in allAuthors[name]:
                            person["birthDate"] = "GREGORIAN:{}:{}".format(allAuthors[name]["birthSpanStart"], allAuthors[name]["birthSpanEnd"])

                        if "deathExact" in allAuthors[name]:
                            person["deathDate"] = "GREGORIAN:{}".format(allAuthors[name]["deathExact"])
                        elif "deathSpanStart" in allAuthors[name]:
                            person["deathDate"] = "GREGORIAN:{}:{}".format(allAuthors[name]["deathSpanStart"], allAuthors[name]["deathSpanEnd"])

                        if "floruitExact" in allAuthors[name]:
                            person["activeDate"] = "GREGORIAN:{}".format(allAuthors[name]["floruitExact"])
                        elif "floruitSpanStart" in allAuthors[name]:
                            person["activeDate"] = "GREGORIAN:{}:{}".format(allAuthors[name]["floruitSpanStart"], allAuthors[name]["floruitSpanEnd"])

                        ww_bulk_object.add_resource(
                            "person",
                            "P01_" + str(line),
                            "person label",
                            person
                        )

                        print("EifelTurm", person)

                        createdAuthors[key] = allAuthors[name]

                    # if name in allAuthors:
                    #     print(allAuthors[name])
                    # else:
                    #     print("NO", "|" + name + "|")
            else:
                print("erste Zeile")
                line += 1

        # countOfAuthors = 1
        # for author in createdAuthors:
        #     print(createdAuthors[author], countOfAuthors)
        #     countOfAuthors += 1

    print("bear")

    BULKIMPORT_API_ENDPOINT = "http://localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0826"
    headers = {"Content-Type": "application/xml"}

    ww_bulk_object.write_xml(ww_bulk_xml)
    ww_bulk_xml_string = open(ww_bulk_xml).read().encode("utf-8")
    r = requests.post(BULKIMPORT_API_ENDPOINT, data=ww_bulk_xml_string, headers=headers, auth=(args.user, args.password))
    pprint(r.json())

except Exception as err:
    print("turtles", err)

#####################
