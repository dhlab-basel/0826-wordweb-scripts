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

    sql = "SELECT * FROM modifications"

    cursor.execute(sql)

    results = cursor.fetchall()

    count = 0

    # Contains all the lexias from hyperhamlet. Key of the lexia object is {internalID title}
    allLexias = {}

    for row in results:

        lex = re.search("(#\d{6}a?)\s(.*)", row["name"])

        if lex:

            lexia = {}
            lexia["internalID"] = lex.group(1)
            lexia["title"] = lex.group(2)

            # Create a key which has the following format{internalID title}
            key = "{} {}".format(lexia["internalID"], lexia["title"])

            # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
            id = "lexia_" + str(hashlib.sha256(key.encode('utf-8')).hexdigest())[:16]

            # Every lexia has an unique internal ID
            lexia["id"] = id

            # Adding ID of SQL table
            lexia["SQL"] = row["id"]

            # Adding the lexia to the allLexia object
            allLexias[key] = lexia

    conn.close()
    cursor.close()

    # # Write all the lexias into json
    with open('json/lexia.json', 'w') as outfile:
        json.dump(allLexias, outfile)

except Exception as err:
    print(err)
