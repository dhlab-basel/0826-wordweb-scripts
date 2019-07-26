# hash library
import hashlib


def generate(key):
    return str(hashlib.sha256(key.encode('utf-8')).hexdigest())[:16]
