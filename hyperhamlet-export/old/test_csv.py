import csv
import re
import pymysql

# Regex library
import re
# csv library
import csv
# JSON library
import json

# Gets authors data from json
with open('json/author.json', 'r') as a:
    allAuthors = json.load(a)

# Gets books data from json
with open('json/book.json', 'r') as b:
    allBooks = json.load(b)

with open('let-them-come.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line = 0
    copied = 0
    names = []
    for row in csv_reader:

        # Skip first row because of column title in excel sheet
        if line is not 0:

            # print(row[5], row[6], row[7], row[8], row[13])

            if row[13] in allBooks:
                print("found")
            else:
                print("not found")

            line += 1

        else:
            line += 1

    print("line", line)
