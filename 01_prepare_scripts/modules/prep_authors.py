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

        sql = "SELECT * FROM authors ORDER BY lastname"

        cursor.execute(sql)

        results = cursor.fetchall()

        # Contains all the authors from hyperhamlet. Key of the author object is {firstName lastName}
        all_authors = {}

        for row in results:

            author = {
                "hasFirstName": row["firstname"],
                "hasLastName": row["lastname"]
            }

            # Start with empty description
            description = ""

            if row["description"]:

                # ignore description if there is exclamation mark
                stop = re.search("!(.*)", row["description"])
                # birth date
                birth = re.search("(.*)b\.\s(.*)", row["description"])
                # death date
                death = re.search("(.*)d\.\s(.*)", row["description"])
                # florouit date
                floruit = re.search("(.*)fl\.\s(.*)", row["description"])
                # birth date as span
                birthDeath = re.search("(.*?)(\[(\d{1,4})-(\d{1,4})\]|(\d{1,4}))-(\[(\d{1,4})-(\d{1,4})\]|(\d{1,4}))(.*)", row["description"])
                # female authors
                female = re.search("(\*)(.*)", row["description"])

                if stop:
                    # dates are saved in the description
                    description = stop.group(1)

                elif birth:

                    birth_span = re.search("(\[(\d{1,4})-(\d{1,4})\]|(\d{1,4}))(.*)", birth.group(2))

                    if birth_span.group(4) is None:
                        author["birthStart"] = birth_span.group(2)
                        author["birthEnd"] = birth_span.group(3)
                        # print("Not Exact Birth", birth_span.groups(), row)
                    else:
                        author["birthExact"]= birth_span.group(1)
                        # print("Exact Birth", birth_span.groups(), row)

                    # add description
                    description = birth.group(1) + birth_span.group(5)

                elif death:

                    death_span = re.search("(\[(\d{1,4})-(\d{1,4})\]|(\d{1,4}))(.*)", death.group(2))

                    if death_span.group(4) is None:
                        author["deathStart"] = death_span.group(2)
                        author["deathEnd"] = death_span.group(3)
                        # print("Not Exact Death", death_span.groups(), row)
                    else:
                        author["deathExact"] = death_span.group(1)
                        # print("Exact Death", death_span.groups(), row)

                    # add description
                    description = death.group(1) + death_span.group(5)

                elif floruit:

                    floruit_span = re.search("((\d{1,4})-(\d{1,4})|(\d{1,4}))(.*)", floruit.group(2))

                    if floruit_span is not None:

                        # print(floruit_span.groups())

                        if floruit_span.group(4) is None:
                            author["activeStart"] = floruit_span.group(2)
                            author["activeEnd"] = floruit_span.group(3)
                            # print("Not Exact Floruit", floruit_span.groups(), row["description"])
                        else:
                            author["activeExact"] = floruit_span.group(1)
                            # print("Exact Floruit", floruit_span.groups(), row["description"])

                        # add description
                        description = floruit.group(1) + floruit_span.group(5)

                elif birthDeath:

                    if birthDeath.group(3):
                        author["birthStart"] = birthDeath.group(3)
                        author["birthEnd"] = birthDeath.group(4)
                        # print("Span Birth: ", birthDeath.groups(), row)
                    else:
                        author["birthExact"] = birthDeath.group(5)
                        # print("Exact Birth in Span: ", birthDeath.groups(), row)

                    if birthDeath.group(7):
                        author["deathStart"] = birthDeath.group(7)
                        author["deathEnd"] = birthDeath.group(8)
                        # print("Span Death: ", birthDeath.groups(), row)
                    else:
                        author["deathExact"] = birthDeath.group(9)
                        # print("Exact Death in Span: ", birthDeath.groups(), row)

                    # add description
                    description = birthDeath.group(1) + birthDeath.group(10)
                # all other descriptions which does not follow the defined rules
                else:
                    description = row["description"]

                # checks if there are only whitespaces or empty strings (excluding year numbers)
                if description.strip():
                    # add description to author after it has trimmed the string
                    author["hasDescription"] = description.rstrip()
                    # add sex of author
                    if female:
                        author["hasGender"] = "female"
                    else:
                        author["hasGender"] = "male"

            # Create a key which has the following format{firstName lastName}
            unique_key = "{} {}".format(author["hasFirstName"], author["hasLastName"])

            # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
            author_id = id.generate(unique_key)

            # Adding ID of SQL table
            author["sql"] = row["id"]

            # Adding the author to the all_author object
            all_authors[author_id] = author

        conn.close()
        cursor.close()

        return all_authors

    except Exception as err:
        print(err)
        raise SystemExit(0)
