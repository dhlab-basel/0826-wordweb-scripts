# JSON library
import json
# operating system library
import os


def clear(file_name):
    if not os.path.isfile(file_name):
        print("[ERROR] No existing file: " + file_name)
        raise SystemExit(0)
    else:
        try:
            # Write all the authors into json
            with open(file_name, 'w') as outfile:
                json.dump({}, outfile)
        except Exception as err:
            print(err, file_name)
            raise SystemExit(0)


def load(file_name):
    try:
        # Gets editions data from json
        with open(file_name, 'r') as e:
            return json.load(e)
    except Exception as err:
        print(err, file_name)
        raise SystemExit(0)


def save(file_name, data):
    try:
        # Write all the authors into json
        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)
    except Exception as err:
        print(err, file_name)
        raise SystemExit(0)
