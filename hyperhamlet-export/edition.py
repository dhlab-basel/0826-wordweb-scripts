import csv
import re
import pymysql

with open('export.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    copied = 0
    pi = {}
    for row in csv_reader:

        publicationInfo = re.search("(.*)\s\s(.*)\s\s(.*)", row[4])
        if publicationInfo:
            # print(publicationInfo.group(2))
            if publicationInfo.group(2) in pi:
                print("here")
            else:
                print("not here")
                copied +=1
                pi[publicationInfo.group(2)] = row[1]

            if publicationInfo.group(2) in pi:
                print("2 here")
            else:
                print(" 2 not here")

        line_count += 1
    print("line count", line_count)
    print("copied", copied)

    for b in pi:
        print(b)