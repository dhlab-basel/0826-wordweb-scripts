import os
from typing import List, Set, Dict, Tuple, Optional
from pprint import pprint
import argparse
import json
from jsonschema import validate
from knora import Knora, BulkImport
import requests


def test():
    try:
        with open('00_data_as_json/author.json') as authors_file:
            authors = json.load(authors_file)

            for author in authors:
                if "hasDescription" not in authors[author]:
                    print(authors[author])

    except Exception as err:
        print(err, "Import Fail")
        raise SystemExit(0)


def start():
    try:
        with open('00_data_as_json/author.json') as authors_file:
            authors = json.load(authors_file)

        with open('00_data_as_json/book.json') as books_file:
            books = json.load(books_file)

        with open('00_data_as_json/passage.json') as passages_file:
            passages = json.load(passages_file)

        with open('00_data_as_json/contributor.json') as contributors_file:
            contributors = json.load(contributors_file)

        with open('00_data_as_json/lexia.json') as lexias_files:
            lexias = json.load(lexias_files)

        with open('00_data_as_json/company.json') as company_files:
            companies = json.load(company_files)

        with open('00_data_as_json/venue.json') as venue_files:
            venues = json.load(venue_files)

    except Exception as err:
        print(err, "Import Fail")
        raise SystemExit(0)

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

    ww_bulk_xml = "./test-bulk-output.xml"
    ww_bulk_object = BulkImport(schema)

    for author in authors:
        ww_bulk_object.add_resource(
            "person",
            author,
            "{} {}".format(authors[author]["hasFirstName"], authors[author]["hasLastName"]),
            authors[author]
        )

    for contributor in contributors:
        ww_bulk_object.add_resource(
            "person",
            contributor,
            "{} {}".format(contributors[contributor]["hasFirstName"], contributors[contributor]["hasLastName"]),
            contributors[contributor]
        )

    for book in books:
        ww_bulk_object.add_resource(
            "book",
            book,
            books[book]["hasBookTitle"],
            books[book]
        )

    for passage in passages:
        ww_bulk_object.add_resource(
            "passage",
            passage,
            passages[passage]['hasPassageInternalId'],
            passages[passage]
        )

    for lexia in lexias:
        ww_bulk_object.add_resource(
            "lexia",
            lexia,
            lexias[lexia]["hasLexiaTitle"],
            lexias[lexia]
        )

    for company in companies:
        ww_bulk_object.add_resource(
            "company",
            company,
            companies[company]["hasCompanyTitle"],
            companies[company]
        )

    for venue in venues:
        ww_bulk_object.add_resource(
            "venue",
            venue,
            venues[venue]["hasPlaceVenue"],
            venues[venue]
        )

    BULKIMPORT_API_ENDPOINT="http://localhost:3333/v1/resources/xmlimport/http%3A%2F%2Frdfh.ch%2Fprojects%2F0826"
    headers = {"Content-Type": "application/xml"}

    ww_bulk_object.write_xml(ww_bulk_xml)
    ww_bulk_xml_string = open(ww_bulk_xml).read().encode("utf-8")
    r = requests.post(BULKIMPORT_API_ENDPOINT, data=ww_bulk_xml_string, headers=headers, auth=(args.user, args.password))
    pprint(r.json())
