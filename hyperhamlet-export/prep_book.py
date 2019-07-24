# mySQL library
import pymysql
# Regex library
import re
# JSON library
import json
# hash library
import hashlib

try:
    conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Test Inner JOIN
    # sql = "SELECT authors_citations.id, authors_citations.author_id, citations.title FROM authors_citations INNER JOIN citations ON authors_citations.citation_id = citations.id"

    # Test Double Inner JOIN -> Verbindungstabelle auflösen
    # sql = "SELECT citations.title FROM citations_textuals INNER JOIN textuals ON textuals.id=citations_textuals.textual_id INNER JOIN citations ON citations_textuals.citation_id = citations.id GROUP BY citations.title"


    sql = "SELECT * FROM linecategories"

    cursor.execute(sql)

    results = cursor.fetchall()

    count = 0

    # Contains all the books from hyperhamlet. Key of the book object is {internalID title}
    allBooks = {}

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
                book["secondary"] = "true"
            else:
                # print("ID: " + books.group(1) + " | TITLE: " + books.group(2))
                book["internalID"] = books.group(1)
                book["title"] = books.group(2)

            # Create a key which has the following format{internalID title}
            key = "{} {}".format(book["internalID"], book["title"])

            # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
            id = "book_" + str(hashlib.sha256(key.encode('utf-8')).hexdigest())[:16]

            # Every book has an unique internal ID
            book["id"] = id

            # Adding ID of SQL table
            book["SQL"] = row["id"]

            # Adding the book to the allBooks object
            allBooks[key] = book

    conn.close()
    cursor.close()

    # Write all the books into json
    with open('json/book.json', 'w') as outfile:
        json.dump(allBooks, outfile)

except Exception as err:
    print(err)
