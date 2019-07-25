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

    sql = "SELECT * FROM citations"

    cursor.execute(sql)

    results = cursor.fetchall()

    count = 0

    # Contains all the editions from hyperhamlet. Key of the edition object is {internalID title}?????
    allEditionOriginal = {}

    for row in results:

        pubInfo = re.search("(.+)\s\s(.+)", row["internal_comment"])

        if pubInfo:

            editionOriginal = {}

            bib = re.search("(.+)\s\s(.+)\s\s(.+)", row["internal_comment"])

            if bib:
                # print(bib.group(2))
                editionOriginal["pubInfo"] = bib.group(2)
            else:
                print("no double", row["id"], pubInfo.group(2))
            #     editionOriginal["pubInfo"] = pubInfo.group(2)

            # # Create a key which has the following format{internalID title}
            # key = edition["pubInfo"]
            #
            # # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
            # id = "edition_" + str(hashlib.sha256(key.encode('utf-8')).hexdigest())[:16]
            #
            # # Every book has an unique internal ID
            # edition["id"] = id
            #
            # # Adding ID of SQL table
            # edition["SQL"] = row["id"]
            #
            # # Adding the book to the allBooks object
            # allEditions[key] = edition

    conn.close()
    cursor.close()

    # Write all the editions into json
    # with open('json/edition_original.json', 'w') as outfile:
    #     json.dump(allEditionOriginal, outfile)

except Exception as err:
    print(err)

