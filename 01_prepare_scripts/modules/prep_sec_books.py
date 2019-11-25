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

            books = re.search("(@\d{6}a?)\s(.*)", row["name"])

            if books:

                book = {}
                sec = re.search("SEC\s\-\s(.*)", books.group(2))

                if sec:
                    # id of the linecategory row in table
                    # print("SEC ID: " + books.group(1) + " | SEC TITLE: " + sec.group(1))
                    book["bookInternalId"] = books.group(1)
                    book["title"] = sec.group(1)

                    # Create a key which has the following format {internalID}
                    unique_key = book["bookInternalId"]

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
                if line is not 0:
                    sec_book = {}
                    # print(row[13], row[2])
                    sec_books = re.search("(@\d{6})\sSEC\s\-\s(.*)", row[13])
                    if sec_books:
                        sec_book["bookInternalId"] = sec_books.group(1)
                        sec_book["title"] = sec_books.group(2)

                        s = ed.info(row[4])

                        sec_book["pubInfo"] = s["pubInfo"]
                        sec_book["hasLanguage"] = row[9]

                        if "letter" in s:
                            sec_book["letter"] = s["letter"]

                        if row[5] and row[6]:
                            sec_book["createdDate"] = "GREGORIAN:{}:{}".format(row[5], row[6])
                            sec_book["publishDate"] = "GREGORIAN:{}:{}".format(row[5], row[6])

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
                        sec_book_id = id.generate(sec_book["bookInternalId"])

                        # Adding the book to the allBooks object
                        all_sec_books[sec_book_id] = sec_book
                    else:
                        print("FAIL prep_sec_books.py")
                        raise SystemExit(0)

                line += 1

        return all_sec_books

    except Exception as err:
        print("FAIL: prep_sec_books.py", err)
        raise SystemExit(0)
