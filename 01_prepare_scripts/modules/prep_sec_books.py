# mySQL library
import pymysql
# Regex library
import re
# csv library
import csv

# helper for edition
import helper_edition as ed
# my id generator
import id_generator as id
# prefix of title
import helper_prefix as pref


def prepare():
    try:
        conn = pymysql.connect(host='localhost', port=8889, user='vitsch', password='test', database='HAMLET')

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT * FROM linecategories"

        cursor.execute(sql)

        results = cursor.fetchall()

        # Contains all the secondary books from hyperhamlet. Key of the book object is {internalID}
        all_sec_books = {}

        for row in results:

            books = re.search("(@\d{6})\s(.*)", row["name"])

            if books:

                book = {}
                sec = re.search("SEC\s\-\s(.*)", books.group(2))

                if sec:
                    # id of the linecategory row in table
                    # print("SEC ID: " + books.group(1) + " | SEC TITLE: " + sec.group(1))
                    book["hasBookInternalId"] = books.group(1)
                    book = pref.get_prefix_book(sec.group(1), book)

                    # Create a key which has the following format {internalID}
                    unique_key = book["hasBookInternalId"]

                    # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
                    book_id = id.generate(unique_key)

                    # Adding ID of SQL table
                    # book["sql"] = row["id"]

                    # Adding the book to the allBooks object
                    all_sec_books[book_id] = book

        conn.close()
        cursor.close()

        return all_sec_books

    except Exception as err:
        print(err)


def prepare_csv():
    try:
        with open("01_prepare_scripts/csv/sec.csv") as f:
            csv_reader = csv.reader(f, delimiter=';')

            # line number in csv file
            line = 0

            # Contains all the secondary books from hyperhamlet. Key of the book object is {internalID}
            all_sec_books = {}

            for row in csv_reader:

                # Skip first row with column title
                if line != 0:
                    sec_book = {}

                    sec_books = re.search("(@\d{6})\sSEC\s\-\s(.*)", row[13])
                    if sec_books:
                        sec_book["hasBookInternalId"] = sec_books.group(1)
                        sec_book["hasLanguage"] = row[9]
                        # Gets book title and its prefix
                        sec_book = pref.get_prefix_book(sec_books.group(2), sec_book)
                        # Gets displayed title and its prefix (-> for all the sec passages the same)
                        sec_book = pref.get_prefix_passage(row[3], sec_book)

                        s = ed.info(row[4])
                        sec_book["pubInfo"] = s["pubInfo"]

                        if row[5] and row[6]:
                            sec_book["hasCreationDate"] = "GREGORIAN:{}:{}".format(row[5], row[6])
                            sec_book["hasPublicationDate"] = "GREGORIAN:{}:{}".format(row[5], row[6])

                        if row[18]:
                            sec_book["hasGenre"] = []
                            sec_book["hasGenre"].append(row[18])

                        # Multiple subjects
                        if row[19]:
                            sec_book["hasSubject"] = row[19].split(" / ")

                        # ---------- AUTHOR
                        # Multiple names of authors
                        names = row[2].split(" / ")

                        authors = []

                        # Iterates through the names per row/ entry
                        for name in names:

                            # Checks if author name is invalid
                            if not name:
                                print("FAIL Author in SEC", line)
                                raise SystemExit(0)

                            authors.append(name.strip())

                        sec_book["authors"] = authors

                        # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
                        sec_book_id = id.generate(sec_book["hasBookInternalId"])

                        # Adding the book to the allBooks object
                        all_sec_books[sec_book_id] = sec_book
                    else:
                        print("FAIL prep_sec_books.py", line, row[13])
                        raise SystemExit(0)

                line += 1

        return all_sec_books

    except Exception as err:
        print("FAIL: prep_sec_books.py", err, row[13])
        raise SystemExit(0)
