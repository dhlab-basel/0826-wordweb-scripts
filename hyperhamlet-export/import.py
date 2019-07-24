# JSON library
import json

# Gets authors data from json
with open('json/author.json', 'r') as a:
    authors = json.load(a)

# Gets books data from json
with open('json/book.json', 'r') as b:
    books = json.load(b)
