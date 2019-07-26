import sys
sys.path.append("modules/")
import csv_reader as csv
import json_handler as json
import id_generator as id
import prep_authors


def start_doing():
    print("Doing it")


json_files = [
    "json/author.json",
    "json/book.json"
]

csv_files = [
    "csv/export_1.csv",
    "csv/export_2.csv",
    "csv/export_3.csv",
    "csv/export_4.csv"
]


# Clears all json files
for file in json_files:
    json.clear(file)


# Prepare all authors
allAuthors = prep_authors.prepare()


# Loads the jsons and creates objects
authors = json.load(json_files[0])
books = json.load(json_files[1])


# Reads the csv files
for file in csv_files:
    csv.read(file)
    start_doing()


# Saves the objects in to json files
json.save(json_files[0], allAuthors)
json.save(json_files[1], books)
