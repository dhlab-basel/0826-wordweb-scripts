import csv
import re
import pymysql

with open('let-them-come.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    copied = 0
    names = []
    for row in csv_reader:

        names = row[2].split(" / ")
        print(names)
        # names = re.search("(.*)\s\/\s(.*)", row[2])

        # if names:
        #     print(names.groups())

        line_count += 1
    # print(names)
    print("line count", line_count)
