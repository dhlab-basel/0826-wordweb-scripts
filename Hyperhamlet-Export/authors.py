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

        birth = re.search("(?<=b\.\s)\d{4}(.*)", row["description"])
        death = re.search("(?<=d\.\s)\d{4}(.*)", row["description"])
        florid = re.search("(?<=fl\.\s)\d{4}(?!\-)(.*)", row["description"])

        # if (birth):
        #     print("Only Birth: " + birth.group(0), row, birth.group(1))

        # if (death):
        #     print("Only Death: " + death.group(0), row, death.group(1))

        birdDeath = re.search("(.*)(\d{4})-(\d{4})(.*)", row["description"])

        if (birdDeath):
            florid_span = re.search("(.*)(fl\.\s)", birdDeath.group(1))
            if (florid_span):
                print("Floridspan - " + "Birth: " + birdDeath.group(2) + " | Death: " + birdDeath.group(3) + " || " + florid_span.group(1) + "::" + birdDeath.group(4), row)
            else:
                print("Normalspan - " + "Birth: " + birdDeath.group(2) + " | Death: " + birdDeath.group(3) + " || " + birdDeath.group(1) + "::" + birdDeath.group(4), row)

        # if (florid):
        #     print("Florid - ", florid.group(1), florid.group(1), row)

        # if birth and death:
        #     print("Same")

    conn.close()
    cursor.close()
except Exception as err:
    print(err)
