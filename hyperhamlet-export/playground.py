import hashlib

obj = {
    "a": [1, 2, 3, 4, 5],
    1: ["Arianne", "Sarah", "Mara", "Alessandra", "Kim"]
}

authorIRI = {}
bookIRI = {}
editionIRI = {}
passageIRI = {}
contributorIRI = {}

print(obj["a"][2])

authorIRI[12] = "IRI12"

print(authorIRI[12])

authorIRI[13] = "IRI13"

print(authorIRI)

s = "bla"

# print(hashlib.sha256(s.encode('utf-8')).hexdigest())
print(int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16))
print(str(int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16))[:15])
# print(int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % (10 ** 10))

# key = "bla"
#
# print(abs(hash(key)))
# print(abs(hash(key)))
# print(hash(key))
# print(hash(key) % (10 ** 8))
# print(hash(key) % (10 ** 10))
