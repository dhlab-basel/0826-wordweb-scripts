# Regex library
import re


def info(text):

    edition = {}

    pubInfo = re.search("(.+)\s\s(.+)", text)

    if pubInfo:

        bib = re.search("(.+)\s\s(.+)\s\s(.+)", text)

        if bib:

            edition["page"] = bib.group(3).strip()

            letter = re.search("\"(.+?)\.?\"\s(.+)", bib.group(2))

            if letter:
                # print("mar", letter.groups(), line)
                edition["letter"] = letter.group(1)
                edition["pubInfo"] = letter.group(2)
            else:
                edition["pubInfo"] = bib.group(2)
        else:

            letter = re.search("\"(.+?)\.?\"\s(.+)", pubInfo.group(2))

            if letter:
                edition["letter"] = letter.group(1)
                edition["pubInfo"] = letter.group(2)
            else:
                edition["pubInfo"] = pubInfo.group(2)

    else:
        if text:
            edition["page"] = text

    return edition
