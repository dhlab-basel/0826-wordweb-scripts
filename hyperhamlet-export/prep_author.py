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

    # sql = "SELECT COUNT(*) FROM authors WHERE description LIKE '%b. %'"
    sql = "SELECT * FROM authors ORDER BY lastname"

    cursor.execute(sql)

    results = cursor.fetchall()

    count = 0

    # Contains all the authors from hyperhamlet. Key of the author object is {firstName lastName}
    allAuthors = {}

    for row in results:

        author = {'firstName': row['firstname'], "lastName": row["lastname"]}

        # Start with empty description
        description = ""

        if row["description"]:

            # birth = re.search("(?<=b\.\s)\d{4}(.*)", row["description"])
            birth = re.search("(.*)b\.\s(.*)", row["description"])
            # death = re.search("(?<=d\.\s)\d{4}(.*)", row["description"])
            death = re.search("(.*)d\.\s(.*)", row["description"])
            # floruit = re.search("(?<=fl\.\s)\d{4}(?!\-)(.*)", row["description"])
            floruit = re.search("(.*)fl\.\s(.*)", row["description"])
            # birthDeath = re.search("(.*)(\d{4})-(\d{4})(.*)", row["description"])
            birthDeath = re.search("(.*?)(\[(\d{4})-(\d{4})\]|(\d{4}))-(\[(\d{4})-(\d{4})\]|(\d{4}))(.*)", row["description"])

            if birth:

                birth_span = re.search("(\[(\d{4})-(\d{4})\]|(\d{4}))(.*)", birth.group(2))

                if birth_span.group(4) is None:
                    author["birthSpanStart"] = birth_span.group(2)
                    author["birthSpanEnd"] = birth_span.group(3)
                    # print("Not Exact Birth", birth_span.groups(), row)
                else:
                    author["birthExact"]= birth_span.group(1)
                    # print("Exact Birth", birth_span.groups(), row)

                # add description
                description = birth.group(1) + birth_span.group(5)

            elif death:

                death_span = re.search("(\[(\d{4})-(\d{4})\]|(\d{4}))(.*)", death.group(2))

                if death_span.group(4) is None:
                    author["deathSpanStart"] = death_span.group(2)
                    author["deathSpanEnd"] = death_span.group(3)
                    # print("Not Exact Death", death_span.groups(), row)
                else:
                    author["deathExact"] = death_span.group(1)
                    # print("Exact Death", death_span.groups(), row)

                # add description
                description = death.group(1) + death_span.group(5)

            elif floruit:

                floruit_span = re.search("((\d{4})-(\d{4})|(\d{4}))(.*)", floruit.group(2))

                if floruit_span is not None:

                    # print(floruit_span.groups())

                    if floruit_span.group(4) is None:
                        author["floruitSpanStart"] = floruit_span.group(2)
                        author["floruitSpanEnd"] = floruit_span.group(3)
                        # print("Not Exact Floruit", floruit_span.groups(), row["description"])
                    else:
                        author["floruitExact"] = floruit_span.group(1)
                        # print("Exact Floruit", floruit_span.groups(), row["description"])

                    # add description
                    description = floruit.group(1) + floruit_span.group(5)

            elif birthDeath:

                if birthDeath.group(3):
                    author["birthSpanStart"] = birthDeath.group(3)
                    author["birthSpanEnd"] = birthDeath.group(4)
                    # print("Span Birth: ", birthDeath.groups(), row)
                else:
                    author["birthExact"] = birthDeath.group(5)
                    # print("Exact Birth in Span: ", birthDeath.groups(), row)

                if birthDeath.group(7):
                    author["deathSpanStart"] = birthDeath.group(7)
                    author["deathSpanEnd"] = birthDeath.group(8)
                    # print("Span Death: ", birthDeath.groups(), row)
                else:
                    author["deathExact"] = birthDeath.group(9)
                    # print("Exact Death in Span: ", birthDeath.groups(), row)

                # add description
                description = birthDeath.group(1) + birthDeath.group(10)

            # add description to author after it has trimmed the string
            author["description"] = description.rstrip()

        # Create a key which has the following format{firstName lastName}
        key = "{} {}".format(author["firstName"], author["lastName"])

        # Creates id with the key from above. ID contains prefix and a hash which is a hexadecimal with 16 characters
        id = "person_" + str(hashlib.sha256(key.encode('utf-8')).hexdigest())[:16]

        # Every author has an unique internal ID
        author["id"] = id

        # Adding the author to the allAuthor object
        allAuthors[key] = author

    conn.close()
    cursor.close()

    # Write all the authors into json
    with open('json/author.json', 'w') as outfile:
        json.dump(allAuthors, outfile)

except Exception as err:
    print("turtles", err)

