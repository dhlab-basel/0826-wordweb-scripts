# system library
import sys
# defining path for module imports
sys.path.append("modules/")

# mySQL library
import pymysql
# Regex library
import re
# JSON library
import json

# my id generator
import id_generator as id
# my edition helper
import helper_edition as ed


def prepare():
    try:
        conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT * FROM citations"

        cursor.execute(sql)

        results = cursor.fetchall()

        # Contains all the editions from hyperhamlet. Key of the edition object is {internalID title}?????
        all_editions = {}

        for row in results:

            # Extracts publication info, letter, sql info of edition
            # If given text is invalid empty object will be returned
            edition = ed.info(row["bibliography"], row["id"])

            if len(edition) is not 0:
                # Create a key which has the following format{internalID title}
                unique_key = edition["pubInfo"]

                # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
                edition_id = id.generate(unique_key)

                # Adding ID of SQL table
                edition["sql"] = row["id"]

                # Adding the book to the allBooks object
                all_editions[edition_id] = edition

        conn.close()
        cursor.close()

        return all_editions

    except Exception as err:
        print(err)
