# csv library
import csv
# system library
import sys
# defining path for module imports
sys.path.append("modules/")

# my json handler
import json_handler as json
# my id generator
import id_generator as id
# preparation for authors
import prep_authors
# preparation for books
import prep_books
# preparation for contributors
import prep_contributors
# preparation for editions
import prep_editions
# preparation for editions original
import prep_editions_original
# helper for edition
import helper_edition as ed


json_files = [
    "json/author.json",
    "json/book.json",
    "json/edition.json",
    "json/edition_original.json",
    "json/passage.json",
    "json/passage_original.json",
    "json/contributor.json"
]

csv_files = [
    "csv/export_1.csv",
    "csv/export_2.csv",
    "csv/export_3.csv",
    "csv/export_4.csv"
]


def create_contributor(co_id):
    contributor = {
        "firstName": allContributors[co_id]["firstName"],
        "lastName": allContributors[co_id]["lastName"],
        "email": allContributors[co_id]["email"]
    }

    contributors[co_id] = contributor


def create_passage_original(pa_or_id, text):
    passage_or = {
        "text": text,
        "occursIn": []
    }

    passagesOriginal[pa_or_id] = passage_or


def update_passage_original(pa_or_id, ed_or_id):
    # Checks if editionOriginal id is not None
    if ed_or_id:
        temp = set(passagesOriginal[pa_or_id]["occursIn"])
        temp.add(ed_or_id)
        passagesOriginal[pa_or_id]["occursIn"] = list(temp)


def create_passage(pa_id, text):
    passage = {
        "text": text,
        "occursIn": []
    }

    passages[pa_id] = passage


def update_passage(pa_id, ed_id, co_or_id, pa_or_id):
    if ed_id:
        temp = set(passages[pa_id]["occursIn"])
        temp.add(ed_id)
        passages[pa_id]["occursIn"] = list(temp)

    if co_or_id:
        passages[pa_id]["wasContributedBy"] = co_or_id

    if pa_or_id:
        passages[pa_id]["isNormalisedVersionOf"] = pa_or_id


def create_edition_original(ed_or_id, edition_original_data):
    edition_original_data["isFirstEditionOf"] = []
    editionsOriginal[ed_or_id] = edition_original_data


def update_edition_original(ed_or_id, b_id):
    temp = set(editionsOriginal[ed_or_id]["isFirstEditionOf"])
    temp.add(b_id)
    editionsOriginal[ed_or_id]["isFirstEditionOf"] = list(temp)


def create_edition(ed_id, edition_data):
    edition_data["isEditionOf"] = []
    editions[ed_id] = edition_data


def update_edition(ed_id, b_id):
    temp = set(editions[ed_id]["isEditionOf"])
    temp.add(b_id)
    editions[ed_id]["isEditionOf"] = list(temp)


def create_book(b_id, data_row):
    book = {
        "internalID": allBooks[b_id]["internalID"],
        "title": allBooks[b_id]["title"],
        "createdDate": data_row[5],
        "publishDate": data_row[6],
        "licenseDate": data_row[7],
        "firstPerformanceDate": data_row[8],
        "isWrittenBy": []
    }

    books[b_id] = book


def update_book(b_id, auth_names):
    # Iterates through the names per entry
    for auth_name in auth_names:

        # Generates author id
        auth_id = id.generate(auth_name)

        # Checks if author already exists
        if auth_id not in authors:
            print("Strange UPDATE BOOK")
            create_author(auth_id)
        else:
            temp = set(books[b_id]["isWrittenBy"])
            temp.add(auth_id)
            books[b_id]["isWrittenBy"] = list(temp)


def create_author(auth_id):
    # Object which will be added to Knora.
    # It contains all the information needed which was defined in the data_model_definition_authors
    person = {
        "firstName": allAuthors[auth_id]["firstName"],
        "lastName": allAuthors[auth_id]["lastName"],
        "hasSex": "male"
    }

    if "description" in allAuthors[auth_id]:
        person["description"] = allAuthors[auth_id]["description"]

    if "birthExact" in allAuthors[auth_id]:
        person["birthDate"] = "GREGORIAN:{}".format(allAuthors[auth_id]["birthExact"])
    elif "birthSpanStart" in allAuthors[auth_id]:
        person["birthDate"] = "GREGORIAN:{}:{}".format(allAuthors[auth_id]["birthSpanStart"],
                                                       allAuthors[auth_id]["birthSpanEnd"])

    if "deathExact" in allAuthors[auth_id]:
        person["deathDate"] = "GREGORIAN:{}".format(allAuthors[auth_id]["deathExact"])
    elif "deathSpanStart" in allAuthors[auth_id]:
        person["deathDate"] = "GREGORIAN:{}:{}".format(allAuthors[auth_id]["deathSpanStart"],
                                                       allAuthors[auth_id]["deathSpanEnd"])

    if "floruitExact" in allAuthors[auth_id]:
        person["activeDate"] = "GREGORIAN:{}".format(allAuthors[auth_id]["floruitExact"])
    elif "floruitSpanStart" in allAuthors[auth_id]:
        person["activeDate"] = "GREGORIAN:{}:{}".format(allAuthors[auth_id]["floruitSpanStart"],
                                                        allAuthors[auth_id]["floruitSpanEnd"])

    # Adding the new authors to the list of authors
    authors[auth_id] = person


# Clears all json files
for file in json_files:
    json.clear(file)

# Prepare all authors
allAuthors = prep_authors.prepare()
allBooks = prep_books.prepare()
allEditions = prep_editions.prepare()
allEditionsOriginal = prep_editions_original.prepare()
allContributors = prep_contributors.prepare()

# Loads the jsons and creates objects
authors = {}
books = {}
editions = {}
editionsOriginal = {}
passages = {}
passagesOriginal = {}
contributors = {}

# Reads the csv files
for csv_file in csv_files:

    try:
        with open(csv_file) as f:
            csv_reader = csv.reader(f, delimiter=';')

            # line number in csv file
            line = 0

            for row in csv_reader:

                # Skip first row with column title
                if line is not 0:

                    # ---------- AUTHOR

                    # Multiple names of authors
                    names = row[2].split(" / ")

                    # Iterates through the names per entry
                    for name in names:

                        # Generates author id
                        author_id = id.generate(name)

                        # Checks if author_id is valid
                        if author_id not in allAuthors:
                            print("FAIL Author", author_id)
                            raise SystemExit(0)

                        # Checks if author already exists
                        if author_id not in authors:
                            create_author(author_id)

                    # ---------- BOOK
                    # generates book id
                    book_id = id.generate(row[13])

                    # Checks if book_id is valid
                    if book_id not in allBooks:
                        print("FAIL Book", book_id)
                        raise SystemExit(0)

                    # Checks if book already exists
                    if book_id not in books:
                        create_book(book_id, row)
                        update_book(book_id, names)
                    else:
                        update_book(book_id, names)

                    # ---------- EDITION
                    edition = ed.info(row[4], None)
                    edition_id = id.generate(edition["pubInfo"])

                    # Checks if edition_id is valid
                    if edition_id not in allEditions:
                        print("FAIL Edition", edition_id, edition, csv_file)
                        raise SystemExit(0)

                    # Checks if edition already exists
                    if edition_id not in editions:
                        create_edition(edition_id, edition)
                        update_edition(edition_id, book_id)
                    else:
                        update_edition(edition_id, book_id)

                    # ----------- EDITION ORIGINAL
                    edition_original = ed.info(row[26], None)
                    edition_original_id = None
                    if edition_original:
                        edition_original_id = id.generate(edition_original["pubInfo"])

                        # Checks if edition_id is valid
                        if edition_original_id not in allEditionsOriginal:
                            print("FAIL Edition Original", edition_original_id, edition_original, csv_file, line)
                            raise SystemExit(0)

                        if edition_original_id not in edition_original:
                            create_edition_original(edition_original_id, edition_original)
                            update_edition_original(edition_original_id, book_id)
                        else:
                            update_edition_original(edition_original_id, book_id)

                    # ------------- PASSAGE
                    # generates passage id
                    passage_id = id.generate(row[10])

                    if passage_id not in passages:
                        create_passage(passage_id, row[10])
                        update_passage(passage_id, edition_id, None, None)
                    else:
                        update_passage(passage_id, edition_id, None, None)

                    # ------------- PASSAGE ORIGINAL
                    # Checks if there is a passage original
                    if row[25]:
                        passage_original_id = id.generate(row[25])

                        if passage_original_id not in passagesOriginal:
                            create_passage_original(passage_original_id, row[25])
                            update_passage_original(passage_original_id, edition_original_id)
                            update_passage(passage_id, None, None, passage_original_id)
                        else:
                            update_passage_original(passage_original_id, edition_original_id)
                            update_passage(passage_id, None, None, passage_original_id)

                    # ------------- CONTRIBUTOR
                    # generates contributor id
                    contributor_id = id.generate(row[27].strip())

                    # Checks if contributor_id is valid
                    if contributor_id not in allContributors:
                        print("FAIL Contributor", contributor_id, csv_file, line)
                        raise SystemExit(0)

                    if contributor_id not in contributors:
                        create_contributor(contributor_id)
                        update_passage(passage_id, None, contributor_id, None)
                    else:
                        update_passage(passage_id, None, contributor_id, None)

                line += 1

    except Exception as err:
        print("FAIL: start.py", err)
        raise SystemExit(0)

# Saves the objects in to json files
json.save(json_files[0], authors)
json.save(json_files[1], books)
json.save(json_files[2], editions)
json.save(json_files[3], editionsOriginal)
json.save(json_files[4], passages)
json.save(json_files[5], passagesOriginal)
json.save(json_files[6], contributors)
