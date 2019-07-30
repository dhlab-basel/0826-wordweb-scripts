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

json_files = [
    "json/author.json",
    "json/book.json",
    "json/contributor.json"
]

csv_files = [
    "csv/export_1.csv",
    "csv/export_2.csv",
    "csv/export_3.csv",
    "csv/export_4.csv"
]


def create_book(id, data_row):
    book = {
        "internalID": allBooks[id]["internalID"],
        "title": allBooks[id]["title"],
        "createdDate": data_row[5],
        "publishDate": data_row[6],
        "licenseDate": data_row[7],
        "firstPerformanceDate": data_row[8]
    }

    books[id] = book


def create_author(id):
    # Object which will be added to Knora.
    # It contains all the information needed which was defined in the data_model_definition_authors
    person = {
        "firstName": allAuthors[id]["firstName"],
        "lastName": allAuthors[id]["lastName"],
        "hasSex": "male",
        "isAuthorOf": []
        # "isAuthorOf": allBooks[bookName]["id"]
    }

    if "description" in allAuthors[id]:
        person["description"] = allAuthors[id]["description"]

    if "birthExact" in allAuthors[id]:
        person["birthDate"] = "GREGORIAN:{}".format(allAuthors[id]["birthExact"])
    elif "birthSpanStart" in allAuthors[author_id]:
        person["birthDate"] = "GREGORIAN:{}:{}".format(allAuthors[id]["birthSpanStart"],
                                                       allAuthors[id]["birthSpanEnd"])

    if "deathExact" in allAuthors[id]:
        person["deathDate"] = "GREGORIAN:{}".format(allAuthors[id]["deathExact"])
    elif "deathSpanStart" in allAuthors[author_id]:
        person["deathDate"] = "GREGORIAN:{}:{}".format(allAuthors[id]["deathSpanStart"],
                                                       allAuthors[id]["deathSpanEnd"])

    if "floruitExact" in allAuthors[id]:
        person["activeDate"] = "GREGORIAN:{}".format(allAuthors[id]["floruitExact"])
    elif "floruitSpanStart" in allAuthors[id]:
        person["activeDate"] = "GREGORIAN:{}:{}".format(allAuthors[id]["floruitSpanStart"],
                                                        allAuthors[id]["floruitSpanEnd"])

    # Adding the new authors to the list of authors
    authors[id] = person


def update_author(auth_id, data_row):
    temp = set(authors[auth_id]["isAuthorOf"])
    book_key = id.generate(data_row[13])
    temp.add(book_key)
    authors[auth_id]["isAuthorOf"] = list(temp)


# Clears all json files
for file in json_files:
    json.clear(file)

# Prepare all authors
allAuthors = prep_authors.prepare()
allBooks = prep_books.prepare()
allContributors = prep_contributors.prepare()

# Loads the jsons and creates objects
authors = json.load(json_files[0])
books = json.load(json_files[1])

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

                        else:
                            update_author(author_id, row)

                line += 1

    except Exception as err:
        print(err)
        raise SystemExit(0)

# Saves the objects in to json files
json.save(json_files[0], authors)
json.save(json_files[1], books)
# json.save(json_files[2], allContributors)
