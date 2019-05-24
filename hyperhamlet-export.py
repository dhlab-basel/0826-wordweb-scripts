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

        birth = re.search("(?<=b\.\s)\d{4}", row["description"])
        death = re.search("(?<=d\.\s)\d{4}", row["description"])
        florid = re.search("(?<=fl\.\s)\d{4}", row["description"])

        if (birth):
            print("Birth!", birth.group(0), row)

        if (death):
            print("Death!", death.group(0), row)

        if (florid):
            print("Florid!", florid.group(0), row)

        # if birth and death:
        #     print("Same")

    conn.close()
    cursor.close()
except Exception as err:
    print(err)
