# mySQL library
import pymysql
# Regex library
import re
# JSON library
import json

# my id generator
import id_generator as id


def prepare():
    try:
        conn = pymysql.connect(host='localhost', port=8889, user='vitsch', password='test', database='HAMLET')

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT * FROM contributors"

        cursor.execute(sql)

        results = cursor.fetchall()

        # Contains all the contributors from hyperhamlet. Key of the contributor object is {firstname lastname}
        all_contributors = {}

        for row in results:

            contributor = {
                "hasFirstName": row["firstname"].strip(),
                "hasLastName": row["lastname"].strip(),
            }

            if row["email"]:
                contributor["hasEmail"] = row["email"]

            # Create a key which has the following format{firstName lastName}
            unique_key = "{} {}".format(contributor["hasLastName"], contributor["hasFirstName"])

            # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
            contributor_id = id.generate(unique_key)

            # Adding ID of SQL table
            contributor["sql"] = row["id"]

            # Adding the author to the all_author object
            all_contributors[contributor_id] = contributor

        conn.close()
        cursor.close()

        return all_contributors

    except Exception as err:
        print(err)
