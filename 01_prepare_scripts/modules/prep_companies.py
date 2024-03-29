# mySQL library
import pymysql
# Regex library
import re
# JSON library
import json

# my id generator
import id_generator as id
# Root node "Name (Company)"
root_node_id = 4


def prepare():
    try:
        conn = pymysql.connect(host='localhost', port=8889, user='vitsch', password='test', database='HAMLET')

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sql = "SELECT * FROM generals"

        cursor.execute(sql)

        results = cursor.fetchall()

        # Contains all the books from hyperhamlet. Key of the book object is {internalID title}
        all_companies = {}

        for row in results:
            if row["parent"] == root_node_id:

                companies = re.search("^(#\d{6})\s(.*)", row["name"])

                company = {}

                if companies:
                    company["hasCompanyInternalId"] = companies.group(1)
                    company["hasCompanyTitle"] = companies.group(2)

                    # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
                    company_id = id.generate(company["hasCompanyInternalId"])

                    # Adding the book to the allBooks object
                    all_companies[company_id] = company

        conn.close()
        cursor.close()

        return all_companies

    except Exception as err:
        print(err)
