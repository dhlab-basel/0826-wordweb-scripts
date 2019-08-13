# csv library
import csv
# system library
import sys
# random library
import random

# defining path for module imports
sys.path.append("modules/")

# helper for edition
import helper_edition as ed
# helper for secondary literature
import helper_secondary as sec
# my id generator
import id_generator as id
# my json handler
import json_handler as json
# preparation for authors
import prep_authors
# preparation for books
import prep_books
# preparation for contributors
import prep_contributors
# preparation for secondary books
import prep_sec_books
# preparation for lexias
import prep_lexias

json_files = [
    "../00_data_as_json/author.json",
    "../00_data_as_json/book.json",
    "../00_data_as_json/passage.json",
    "../00_data_as_json/contributor.json",
    "../00_data_as_json/lexia.json"
]

csv_files = [
    "csv/export_1.csv",
    "csv/export_2.csv",
    "csv/export_3.csv",
    "csv/export_4.csv",
    # "csv/export_5.csv"
]


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


def create_book(b_id, data_row, pub_info, pub_or_info):
    book = {
        "internalID": allBooks[b_id]["internalID"],
        "edition": pub_info["pubInfo"],
        "createdDate": data_row[5],
        "publishDate": data_row[6],
        "licenseDate": data_row[7],
        "firstPerformanceDate": data_row[8],
        "isWrittenBy": []
    }

    if "letter" in pub_info:
        book["title"] = pub_info["letter"]
    else:
        book["title"] = allBooks[b_id]["title"]

    if pub_or_info:
        book["editionOriginal"] = pub_or_info["pubInfo"]

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


def create_sec_book(sec_b_id, pub_info):
    book = {
        "internalID": allSecBooks[sec_b_id]["internalID"],
        "edition": pub_info["pubInfo"],
        "isWrittenBy": [],
        "isSecondary": True
    }

    if "letter" in pub_info:
        book["title"] = pub_info["letter"]
    else:
        book["title"] = allSecBooks[sec_b_id]["title"]

    books[sec_b_id] = book


def update_sec_book(sec_b_id, auth_names):
    # Iterates through the names per entry
    for auth_name in auth_names:

        # Generates author id
        auth_id = id.generate(auth_name)

        # Checks if author already exists
        if auth_id not in authors:
            create_author(auth_id)

        temp = set(books[sec_b_id]["isWrittenBy"])
        temp.add(auth_id)
        books[sec_b_id]["isWrittenBy"] = list(temp)


def create_passage(pa_id, text, text_or):
    passage = {
        "text": text,
        "occursIn": [],
        "isMentionedIn": []
    }

    if text_or:
        passage["textOriginal"] = text_or

    passages[pa_id] = passage


def update_passage(pa_id, bo_id, co_or_id, sec_pa_id):
    if bo_id:
        temp = set(passages[pa_id]["occursIn"])
        temp.add(bo_id)
        passages[pa_id]["occursIn"] = list(temp)

    if co_or_id:
        passages[pa_id]["wasContributedBy"] = co_or_id

    if sec_pa_id:
        temp = set(passages[pa_id]["isMentionedIn"])
        temp.add(sec_pa_id)
        passages[pa_id]["isMentionedIn"] = list(temp)


def create_sec_passage(sec_pa_id, pag):
    passage = {
        "page": pag,
        "occursIn": [],
        "isSecondaryPassage": True
    }

    passages[sec_pa_id] = passage


def update_sec_passage(sec_pa_id, sec_bo_id):
    if sec_bo_id:
        temp = set(passages[sec_pa_id]["occursIn"])
        temp.add(sec_bo_id)
        passages[sec_pa_id]["occursIn"] = list(temp)


def create_contributor(co_id):
    contributor = {
        "firstName": allContributors[co_id]["firstName"],
        "lastName": allContributors[co_id]["lastName"],
        "email": allContributors[co_id]["email"]
    }

    contributors[co_id] = contributor


# Clears all json files
for file in json_files:
    json.clear(file)

# Prepare all authors
allAuthors = prep_authors.prepare()
allBooks = prep_books.prepare()
allSecBooks = prep_sec_books.prepare_csv()
allContributors = prep_contributors.prepare()
allLexias = prep_lexias.prepare()

# Saves the complete objects into json files
json.save("all_data/all_authors.json", allAuthors)
json.save("all_data/all_books.json", allBooks)
json.save("all_data/all_sec_books.json", allSecBooks)

# Loads the jsons and creates objects
authors = {}
books = {}
contributors = {}
lexia = {}
passages = {}

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
                        print("FAIL Book", book_id, row[13], line, csv_file)
                        raise SystemExit(0)

                    publication = ed.info(row[4])
                    publication_original = ed.info(row[26])

                    # Creates the book and updates the author references
                    if book_id not in books:
                        create_book(book_id, row, publication, publication_original)
                        update_book(book_id, names)
                    else:
                        update_book(book_id, names)

                    # ------------- PASSAGE
                    # generates passage id
                    passage_id = id.generate(row[10])

                    # Creates the passage and updates the edition reference
                    if passage_id not in passages:
                        create_passage(passage_id, row[10], row[25])
                        update_passage(passage_id, book_id, None, None)
                    else:
                        update_passage(passage_id, book_id, None, None)

                    # ------------- CONTRIBUTOR
                    # generates contributor id
                    contributor_id = id.generate(row[27].strip())

                    # Checks if contributor_id is valid
                    if contributor_id not in allContributors:
                        print("FAIL Contributor", contributor_id, csv_file, line)
                        raise SystemExit(0)

                    # Creates the contributor and updates the passage reference
                    if contributor_id not in contributors:
                        create_contributor(contributor_id)
                        update_passage(passage_id, None, contributor_id, None)
                    else:
                        update_passage(passage_id, None, contributor_id, None)

                    # -------------- SECONDARY BOOK
                    sec_books = sec.info(row[24], line, csv_file)

                    for sec_book in sec_books:

                        sec_book_id = id.generate(sec_book["id"])

                        # Checks if sec book id is valid
                        if sec_book_id not in allSecBooks:
                            print("FAIL Secondary Book", sec_book["id"], csv_file, line, row[24])
                            raise SystemExit(0)

                        s_book = allSecBooks[sec_book_id]

                        if sec_book_id not in books:
                            create_sec_book(sec_book_id, s_book)
                            update_sec_book(sec_book_id, s_book["authors"])
                        else:
                            update_sec_book(sec_book_id, s_book["authors"])

                        if sec_book["page"] == "no page":
                            unique_key = random.randint(100000, 999999)
                        else:
                            unique_key = "{} {}".format(sec_book["id"], sec_book["page"])

                        sec_passage_id = id.generate(str(unique_key))
                        create_sec_passage(sec_passage_id, sec_book["page"])
                        update_sec_passage(sec_passage_id, sec_book_id)
                        update_passage(passage_id, None, None, sec_passage_id)

                line += 1

    except Exception as err:
        print("FAIL: start.py", err)
        raise SystemExit(0)

# Saves the objects which occurs in the csv files in to json files
json.save(json_files[0], authors)
json.save(json_files[1], books)
json.save(json_files[2], passages)
json.save(json_files[3], contributors)
json.save(json_files[4], lexia)
