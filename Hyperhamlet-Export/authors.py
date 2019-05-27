import pymysql
import re

try:
    conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT * FROM authors"

    cursor.execute(sql)

    results = cursor.fetchall()

    for row in results:

        if row["description"]:

            birth = re.search("(?<=b\.\s)\d{4}(.*)", row["description"])
            death = re.search("(?<=d\.\s)\d{4}(.*)", row["description"])
            florid = re.search("(?<=fl\.\s)\d{4}(?!\-)(.*)", row["description"])
            birthDeath = re.search("(.*)(\d{4})-(\d{4})(.*)", row["description"])

            # if (birth):
            #     print("Only Birth: " + birth.group(0), row, birth.group(1))

            # if (death):
            #     print("Only Death: " + death.group(0), row, death.group(1))

            # if (florid):
            #     print("Florid - ", florid.group(1), florid.group(1), row)

            # if (birthDeath):
            #     florid_span = re.search("(.*)(fl\.\s)", birthDeath.group(1))
            #     if (florid_span):
            #         print("Floridspan - " + "Birth: " + birthDeath.group(2) + " | Death: " + birthDeath.group(3) + " || " + florid_span.group(1) + "::" + birthDeath.group(4), row)
            #     else:
            #         print("Normalspan - " + "Birth: " + birthDeath.group(2) + " | Death: " + birthDeath.group(3) + " || " + birthDeath.group(1) + "::" + birthDeath.group(4), row)


            # Test if all are not the same
            # if (birth and death):
            #     print("Birth and Death")
            # elif (birth and florid):
            #     print("Birth and Flourid", row["description"], florid)
            # elif (death and florid):
            #     print("Death and Flourid")
            # elif (birth and birthDeath):
            #     print("Birth and BirthDeath")
            # elif (death and birthDeath):
            #     print("Death and BirthDeath")
            # elif (florid and birthDeath):
            #     print("Flourid and BirthDeath", row["description"], florid)
            # else:
            #     print("Not Same")

    conn.close()
    cursor.close()
except Exception as err:
    print(err)
