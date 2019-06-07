import pymysql
import re

try:
    conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # sql = "SELECT COUNT(*) FROM authors WHERE description LIKE '%b. %'"
    sql = "SELECT * FROM authors ORDER BY lastname"

    cursor.execute(sql)

    results = cursor.fetchall()

    count = 0

    for row in results:

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
                    print("Not Exact Birth", birth_span.groups(), row)
                else:
                    print("Exact Birth", birth_span.groups(), row)

            elif death:

                death_span = re.search("(\[(\d{4})-(\d{4})\]|(\d{4}))(.*)", death.group(2))

                if death_span.group(4) is None:
                    print("Not Exact Death", death_span.groups(), row)
                else:
                    print("Exact Death", death_span.groups(), row)

            elif floruit:

                floruit_span = re.search("((\d{4})-(\d{4})|(\d{4}))(.*)", floruit.group(2))

                if floruit_span is not None:

                    if floruit_span.group(4) is None:
                        print("Not Exact Floruit", floruit_span.groups(), row["description"])
                    else:
                        print("Exact Floruit", floruit_span.groups(), row["description"])

            elif birthDeath:

                if birthDeath.group(3):
                    # print("Span Birth: ", birthDeath.group(3), birthDeath.group(4), "Beginning: ", birthDeath.group(1), "Ending: ", birthDeath.group(10), row["description"])
                    print("Span Birth: ", birthDeath.groups(), row)
                else:
                    # print("Exact Birth: ", birthDeath.group(5), "Beginning: ", birthDeath.group(1), "Ending: ", birthDeath.group(10), row["description"])
                    print("Exact Birth in Span: ", birthDeath.groups(), row)

                if birthDeath.group(7):
                    # print("Span Death: ", birthDeath.group(7), birthDeath.group(8), "Beginning: ", birthDeath.group(1), "Ending: ", birthDeath.group(10), row["description"])
                    print("Span Death: ", birthDeath.groups(), row)
                else:
                    # print("Exact Death: ", birthDeath.group(9), "Beginning: ", birthDeath.group(1), "Ending: ", birthDeath.group(10), row["description"])
                    print("Exact Death in Span: ", birthDeath.groups(), row)


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

    conn.close()
    cursor.close()

except Exception as err:
    print(err)
