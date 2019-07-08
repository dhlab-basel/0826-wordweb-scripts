import pymysql
import re
import csv

try:
    conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # sql = "SELECT COUNT(*) FROM authors WHERE description LIKE '%b. %'"
    sql = "SELECT * FROM authors ORDER BY lastname"

    cursor.execute(sql)

    results = cursor.fetchall()

    count = 0
    authors = {}

    for row in results:

        # Example of author object
        # author = {
        #     "firstName": "William",
        #     "lastName": "Shakespeare",
        #     "description": "English Dramatist",
        #     "birthExact": "",
        #     "birthSpanStart": "",
        #     "birthSpanEnd": "",
        #     "deathExact": "",
        #     "deathSpanStart": "",
        #     "deathSpanEnd": "",
        #     "floruitExact": "",
        #     "floruitSpanStart": "",
        #     "floruitSpanEnd": ""
        # }

        author = {'firstName': row['firstname'], "lastName": row["lastname"]}

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

            elif death:

                death_span = re.search("(\[(\d{4})-(\d{4})\]|(\d{4}))(.*)", death.group(2))

                if death_span.group(4) is None:
                    author["deathSpanStart"] = death_span.group(2)
                    author["deathSpanEnd"] = death_span.group(3)
                    # print("Not Exact Death", death_span.groups(), row)
                else:
                    author["deathExact"] = death_span.group(1)
                    # print("Exact Death", death_span.groups(), row)

            elif floruit:

                floruit_span = re.search("((\d{4})-(\d{4})|(\d{4}))(.*)", floruit.group(2))

                if floruit_span is not None:

                    if floruit_span.group(4) is None:
                        author["floruitSpanStart"] = floruit_span.group(2)
                        author["floruitSpanEnd"] = floruit_span.group(3)
                        # print("Not Exact Floruit", floruit_span.groups(), row["description"])
                    else:
                        author["floruitExact"] = floruit_span.group(1)
                        # print("Exact Floruit", floruit_span.groups(), row["description"])

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


            # Test if all are not the same
            # if (birth and death):
            #     print("Birth and Death")
            # elif (birth and floruit):
            #     print("Birth and Flourid", row["description"], floruit)
            # elif (death and floruit):
            #     print("Death and Flourid")
            # elif (birth and birthDeath):
            #     print("Birth and BirthDeath")
            # elif (death and birthDeath):
            #     print("Death and BirthDeath")
            # elif (floruit and birthDeath):
            #     print("Flourid and BirthDeath", row["description"], floruit)
            # else:
            #     print("Not Same")

        # Add the author to the key value object
        if author["firstName"] and author["lastName"]:
            # print("full name", author["firstName"] + " " + author["lastName"])
            authors[author["firstName"] + " " + author["lastName"]] = author
        elif not author["firstName"] and author["lastName"]:
            # print("last name", author["lastName"])
            authors[author["lastName"]] = author
        elif not author["lastName"] and author["firstName"]:
            # print("first name", author["firstName"])
            authors[author["firstName"]] = author
        else:
            print("FAIL")

    conn.close()
    cursor.close()

    # Print all the values in the object
    # for author in authors:
    #     print(author, authors[author])

except Exception as err:
    print(err)
