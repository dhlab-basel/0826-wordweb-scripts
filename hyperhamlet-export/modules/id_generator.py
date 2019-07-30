# hash library
import hashlib


def generate(key):
    return "ww_" + str(hashlib.sha256(key.encode('utf-8')).hexdigest())[:16]
