# import hashlib

import random

import sys
# defining path for module imports
sys.path.append("modules/")
# preparation for lexias
# import prep_lexias



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
print(random.randint(7000, 7999))
