import pymysql
import re

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

    for row in results:
        # print(row["name"])

        books = re.search("(@\d{6}a?)\s(.*)", row["name"])

        if books:

            sec = re.search("SEC\s\-\s(.*)", books.group(2))

            if sec:
                # id of the linecategory row in table
                print("SEC ID: " + books.group(1) + " | SEC TITLE: " + sec.group(1))
            else:
                print("ID: " + books.group(1) + " | TITLE: " + books.group(2))





    conn.close()
    cursor.close()
except Exception as err:
    print(err)
