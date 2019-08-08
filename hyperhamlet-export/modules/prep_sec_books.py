# mySQL library
import pymysql
# Regex library
import re
# JSON library
import json

# my id generator
import id_generator as id


def prepare():
    try:
        conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

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
                    book["internalID"] = books.group(1)
                    book["title"] = sec.group(1)

                    # Create a key which has the following format {internalID}
                    unique_key = book["internalID"]

                    # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
                    book_id = id.generate(unique_key)

                    # Adding ID of SQL table
                    book["sql"] = row["id"]

                    # Adding the book to the allBooks object
                    all_sec_books[book_id] = book

        conn.close()
        cursor.close()

        return all_sec_books

    except Exception as err:
        print(err)
