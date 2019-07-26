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

    sql = "SELECT * FROM contributors"

    cursor.execute(sql)

    results = cursor.fetchall()

    count = 0

    # Contains all the contributors from hyperhamlet. Key of the contributor object is {firstname lastname}
    allContributors = {}

    for row in results:

        contributor = {}

        contributor["firstname"] = row["firstname"].strip()
        contributor["lastname"] = row["lastname"].strip()
        contributor["email"] = row["email"]

        # Create a key which has the following format{internalID title}
        key = "{} {}".format(contributor["firstname"], contributor["lastname"])

        # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
        id = "contributor_" + str(hashlib.sha256(key.encode('utf-8')).hexdigest())[:16]

        # Every book has an unique internal ID
        contributor["id"] = id

        # Adding ID of SQL table
        contributor["SQL"] = row["id"]

        # Adding the book to the allBooks object
        allContributors[key] = contributor

    conn.close()
    cursor.close()

    # Write all the editions into json
    with open('json/contributors.json', 'w') as outfile:
        json.dump(allContributors, outfile)

except Exception as err:
    print(err)
