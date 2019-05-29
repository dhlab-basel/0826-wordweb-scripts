import pymysql
import re

try:
    conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # sql = "SELECT authors_citations.id, authors_citations.author_id, citations.title FROM authors_citations INNER JOIN citations ON authors_citations.citation_id = citations.id"
    sql = "SELECT authors.firstname, authors.lastname, citations.title FROM authors, authors_citations, citations WHERE authors.id = authors_citations.author_id AND citations.id = authors_citations.citation_id"

    cursor.execute(sql)

    results = cursor.fetchall()

    for row in results:
        print(row)

    conn.close()
    cursor.close()
except Exception as err:
    print(err)
