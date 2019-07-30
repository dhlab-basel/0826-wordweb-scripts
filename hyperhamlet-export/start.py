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


def create_author():
    print("")


def update_author():
    print("")


def create_book():
    print("")


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


# Clears all json files
for file in json_files:
    json.clear(file)


# Prepare all authors
allAuthors = prep_authors.prepare()
allBooks = prep_books.prepare()
allContributors = prep_contributors.prepare()

json.save(json_files[0], allAuthors)


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

                    book_id = id.generate(row[13])

                    # Checks if book_id is valid
                    if book_id not in allBooks:
                        print("FAIL Book", book_id)
                        raise SystemExit(0)

                    # Checks if book already exists
                    if book_id not in books:

                        # Create book resource
                        book = {
                            "internalID": allBooks[book_id]["internalID"],
                            "title": allBooks[book_id]["title"],
                            "createdDate": row[5],
                            "publishDate": row[6],
                            "licenseDate": row[7],
                            "firstPerformanceDate": row[8]
                        }

                        books[book_id] = book

                    # Multiple names of authors
                    names = row[2].split(" / ")

                    # Iterates through the names per entry
                    for name in names:

                        author_id = id.generate(name)

                        # Checks if author_id is valid
                        if author_id not in allAuthors:
                            print("FAIL Author", author_id)
                            raise SystemExit(0)

                        # Checks if author already exists
                        if author_id not in authors:

                            # create author resource
                            # Object which will be added to Knora.
                            # It contains all the information needed which was defined in the data_model_definition_authors
                            person = {
                                "firstName": allAuthors[author_id]["firstName"],
                                "lastName": allAuthors[author_id]["lastName"],
                                "hasSex": "male",
                                # "isAuthorOf": allBooks[bookName]["id"]
                            }

                            if "description" in allAuthors[author_id]:
                                person["description"] = allAuthors[author_id]["description"]

                            if "birthExact" in allAuthors[author_id]:
                                person["birthDate"] = "GREGORIAN:{}".format(allAuthors[author_id]["birthExact"])
                            elif "birthSpanStart" in allAuthors[author_id]:
                                person["birthDate"] = "GREGORIAN:{}:{}".format(allAuthors[author_id]["birthSpanStart"],
                                                                               allAuthors[author_id]["birthSpanEnd"])

                            if "deathExact" in allAuthors[author_id]:
                                person["deathDate"] = "GREGORIAN:{}".format(allAuthors[author_id]["deathExact"])
                            elif "deathSpanStart" in allAuthors[author_id]:
                                person["deathDate"] = "GREGORIAN:{}:{}".format(allAuthors[author_id]["deathSpanStart"],
                                                                               allAuthors[author_id]["deathSpanEnd"])

                            if "floruitExact" in allAuthors[author_id]:
                                person["activeDate"] = "GREGORIAN:{}".format(allAuthors[author_id]["floruitExact"])
                            elif "floruitSpanStart" in allAuthors[author_id]:
                                person["activeDate"] = "GREGORIAN:{}:{}".format(allAuthors[author_id]["floruitSpanStart"],
                                                                                allAuthors[author_id]["floruitSpanEnd"])

                            # Adding the new authors to the list of authors
                            authors[author_id] = person

                line += 1

    except Exception as err:
        print(err)
        raise SystemExit(0)


# Saves the objects in to json files
json.save(json_files[0], authors)
json.save(json_files[1], books)
# json.save(json_files[2], allContributors)
