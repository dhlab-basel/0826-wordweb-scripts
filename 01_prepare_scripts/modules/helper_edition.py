# Regex library
import re


def info(text):

    edition = {}

    pubInfo = re.search("(.+)\s\s(.+)", text)

    if pubInfo:

        bib = re.search("(.+)\s\s(.+)\s\s(.+)", text)

        if bib:
            edition["page"] = bib.group(3).strip()
            edition["pubInfo"] = bib.group(2)
        else:
            edition["pubInfo"] = pubInfo.group(2)

    else:
        if text:
            edition["page"] = text

    return edition
