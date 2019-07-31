# system library
import sys
# Regex library
import re


def info(text, id):

    edition = {}

    pubInfo = re.search("(.+)\s\s(.+)", text)

    if pubInfo:

        bib = re.search("(.+)\s\s(.+)\s\s(.+)", text)

        if bib:

            letter = re.search("\"(.+?)\"\s(.+)", bib.group(2))

            if letter:
                edition["letter"] = letter.group(1)
                edition["pubInfo"] = letter.group(2)
            else:
                edition["pubInfo"] = bib.group(2)
        else:

            letter = re.search("\"(.+?)\"\s(.+)", pubInfo.group(2))

            if letter:
                edition["letter"] = letter.group(1)
                edition["pubInfo"] = letter.group(2)
            else:
                edition["pubInfo"] = pubInfo.group(2)

        if id:
            edition["sql"] = id
    # else:
    #     print("empty", id)

    return edition
