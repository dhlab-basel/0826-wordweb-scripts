import csv
import re
import pymysql

with open('let-them-come.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    copied = 0
    pi = {}
    for row in csv_reader:

        print(row[2])

        line_count += 1
    print("line count", line_count)
