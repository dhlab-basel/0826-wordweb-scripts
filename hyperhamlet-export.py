import pymysql
import re

try:
    conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT * FROM authors"

    cursor.execute(sql)

    results = cursor.fetchall()

    for row in results:
        # print(row["description"])

        x = re.search("(?<=b\.\s)\d{4}", row["description"])
        y = re.search("(?<=d\.\s)\d{4}", row["description"])

        if (x):
            print("Birth!", x.group(0), row)
        # else:
        #     print("No match")

        if (y):
            print("Death!", y.group(0), row)

        if (x and y)
            print()

    conn.close()
    cursor.close()
except Exception as err:
    print(err)
