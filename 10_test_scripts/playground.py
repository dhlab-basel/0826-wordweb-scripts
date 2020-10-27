# import hashlib

import random
import re
# import sys
# defining path for module imports
# sys.path.append("modules/")
# preparation for lexias
# import prep_lexias

# import sys
# sys.path.append("01_prepare_scripts/modules/")
# import json_handler as json

# import prep_edition

# -------------- Access objects and list
# obj = {
#     "a": [1, 2, 3, 4, 5],
#     1: ["Arianne", "Sarah", "Mara", "Alessandra", "Kim"]
# }
#
# authorIRI = {}
# bookIRI = {}
# editionIRI = {}
# passageIRI = {}
# contributorIRI = {}
#
# print(obj["a"][2])
#
# authorIRI[12] = "IRI12"
#
# print(authorIRI[12])
#
# authorIRI[13] = "IRI13"
#
# print(authorIRI)

# -------------- Unique identifier
# s = "bla"
#
# print(hashlib.sha256(s.encode('utf-8')).hexdigest())
# print(int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16))
# print(str(int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16))[:15])
# print(int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % (10 ** 10))
#
# key = "bla"
#
# print(abs(hash(key)))
# print(abs(hash(key)))
# print(hash(key))
# print(hash(key) % (10 ** 8))
# print(hash(key) % (10 ** 10))

# -------------- List with no duplicates
# gustav = []
#
# bla = set(gustav)
# bla.add("3")
# gustav = list(bla)
# print(gustav)
#
#
# bla = set(gustav)
# bla.add("-3")
# gustav = list(bla)
# print(gustav)
#
#
# bla = set(gustav)
# bla.add("3")
# gustav = list(bla)
# print(gustav)

# --------------- Test editions

# prep_editions.prepare()

# print(editions["ww_878987dd1466a525"]["sql"])

# for ed in editions:
#     print(ed)

# ----------------- Random Number
# print(random.randint(100000, 999999))

# allLexias = prep_lexias.prepare()

# -----------------
# print(random.randint(7000, 7999))


# -----------------
# test = "Roman politician 0-0 100 BC-44 BC #007001"
# test = "! fl. 2222-3333"
#
# stop = re.search("!(.*)", test)
#
# birth = re.search("(.*)b\.\s(.*)", test)
# death = re.search("(.*)d\.\s(.*)", test)
# floruit = re.search("(.*)fl\.\s(.*)", test)
# birthDeath = re.search("(.*?)(\[(\d{1,4})-(\d{1,4})\]|(\d{1,4}))-(\[(\d{1,4})-(\d{1,4})\]|(\d{1,4}))(.*)", test)
#
# if stop:
#     print("stop")
# elif birth:
#
#     birth_span = re.search("(\[(\d{1,4})-(\d{1,4})\]|(\d{1,4}))(.*)", birth.group(2))
#
#     print("1", birth.groups(), birth_span.groups())
#
# elif death:
#
#     death_span = re.search("(\[(\d{1,4})-(\d{1,4})\]|(\d{1,4}))(.*)", death.group(2))
#
#     print("2", death.groups(), death_span.groups())
#
#
# elif floruit:
#
#     floruit_span = re.search("((\d{1,4})-(\d{1,4})|(\d{1,4}))(.*)", floruit.group(2))
#
#     print("3", floruit.groups(), floruit_span.groups())
#
# elif birthDeath:
#     print("4", birthDeath.groups())
#
# else:
#     print("nothing")

# -----------------

# start = 7100
#
# id = "&00" + str(start + 1)
#
# print(id, type(id), type(start))

# ----------------- Search for passages with more than one lexia

# allPassages = {}
# allLexias = {}
#
# passages = []
#
# try:
#     with open('../00_data_as_json/passage.json') as passages_file:
#         allPassages = json.load(passages_file)
#
#     with open('../00_data_as_json/lexia.json') as lexias_file:
#         allLexias = json.load(lexias_file)
#
#     counter = 0
#     for passage_id in allPassages:
#         if "contains" in allPassages[passage_id]:
#             # print(passages[passage_id]["contains"])
#             if len(allPassages[passage_id]["contains"]) > 1:
#                 passage = {}
#                 print(allPassages[passage_id]["hasText"])
#                 counter = counter + 1
#                 passage["text"] = allPassages[passage_id]["hasText"]
#
#                 passages.append(passage)
#
#                 json.save("passages_with_lexias.json", passages)
#
#     print(counter)
#
# except Exception as err:
#     print(err, "Import Fail")
#     raise SystemExit(0)

# -----------------
word = "the name"
def_article = re.search("^([Tt]he)\s(.*)", word)
undef_article = re.search("^([Aa])\s(.*)", word)

if def_article:
    print(def_article.group(1), def_article.group(2))
elif undef_article:
    print(undef_article.group(1), undef_article.group(2))
else:
    print("NOT FOUND")
