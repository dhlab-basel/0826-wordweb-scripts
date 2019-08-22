import os
from typing import List, Set, Dict, Tuple, Optional
from pprint import pprint
import argparse
import json
from jsonschema import validate
from knora import KnoraError, Knora, BulkImport
import requests


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", type=str, default="http://0.0.0.0:3333", help="URL of the Knora server")
parser.add_argument("-u", "--user", default="root@example.com", help="Username for Knora")
parser.add_argument("-p", "--password", default="test", help="The password for login")
parser.add_argument("-P", "--projectcode", default="0826", help="Project short code")
parser.add_argument("-O", "--ontoname", default="teimww", help="Shortname of ontology")

args = parser.parse_args()


con = Knora(args.server)
con.login(args.user, args.password)
schema = con.create_schema(args.projectcode, args.ontoname)

#res_info1 = con.create_resource(schema, "book", "test-book", {
#    "title": "Romeo und Julia"
#})

#pprint(res_info1)
#
# res_info2 = con.create_resource(schema, "person", "test-person", {
#     "internalID": "&000001",
#     "firstName": "William",
#     "lastName": "Shakespeare",
#     "description": "English Dramatist",
#     "birthDate": "GREGORIAN:1564",
#     "deathDate": "GREGORIAN:1616",
#     "isAuthorOf": "http://rdfh.ch/0826/I2xQrsXYSnuDARYIH772Eg"
# })

#pprint(res_info2)
#
# res_info3 = con.create_resource(schema, "person", "test-person", {
#     "internalID": "@000001",
#     "firstName": "Regula",
#     "lastName": "Hohl",
# })
#
# pprint(res_info3)


ww_bulk_xml = "./test-bulk-output.xml"
ww_bulk_object = BulkImport(schema)

buch1 = {}
buch1["title"] = "Romeo und Julia"

buch2 = {}
buch2["title"] = "Hamlet"

person = {
    "internalID": "&000001",
    "firstName": "William",
    "lastName": "Shakespeare",
    "description": ["English Dramatist", "African Hero"],
    "birthDate": "GREGORIAN:1564",
    "deathDate": "GREGORIAN:1616",
    "isAuthorOf": ["B_01", "B_02"],
    "hasSex": "male"
}

ww_bulk_object.add_resource(
    "book",
    "B_01",
    "buch label",
    buch1
)

ww_bulk_object.add_resource(
    "book",
    "B_02",
    "buch label",
    buch2
)

ww_bulk_object.add_resource(
    "person",
    "P_01",
    "person label",
    person
)

# edition = {
#     "isEditionOf": "B_01",
#     "isWrittenIn": "L_01"
# }
#
# language = {
#     "languageName": "Deutsch"
# }
#
# ww_bulk_object.add_resource(
#     "language",
#     "L_01",
#     "sprache label",
#     language
# )
#
# ww_bulk_object.add_resource(
#     "edition",
#     "E_01",
#     "edition label",
#     edition
# )


BULKIMPORT_API_ENDPOINT="http://localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0826"
headers = {"Content-Type": "application/xml"}

ww_bulk_object.write_xml(ww_bulk_xml)
ww_bulk_xml_string = open(ww_bulk_xml).read().encode("utf-8")
r = requests.post(BULKIMPORT_API_ENDPOINT, data=ww_bulk_xml_string, headers=headers, auth=(args.user, args.password))
pprint(r.json())
