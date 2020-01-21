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

        sql = "SELECT * FROM generals"

        cursor.execute(sql)

        results = cursor.fetchall()

        # Contains all the books from hyperhamlet. Key of the book object is {internalID title}
        all_venues = {}

        for row in results:
            # Making sure all the nodes are venues by checking the parent with the ID 182 (look up in the database)
            if row["parent"] is 182:

                venues = re.search("^(#\d{6})\s(.*)_(.*)", row["name"])

                venue = {}

                if venues:
                    venue["venueInternalId"] = venues.group(1)
                    venue["hasVenuePlace"] = venues.group(3)

                    # Create a key which has the following format{venueInternalId venueTitle}
                    unique_key = "{} {}".format(venue["venueInternalId"], venue["hasVenuePlace"])

                    # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
                    venue_id = id.generate(unique_key)

                    # Adding the book to the allBooks object
                    all_venues[venue_id] = venue

        conn.close()
        cursor.close()

        return all_venues

    except Exception as err:
        print(err)
