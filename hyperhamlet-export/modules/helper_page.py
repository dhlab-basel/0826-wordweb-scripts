# system library
import sys
# Regex library
import re


def info(text):

    page_info = None

    bib = re.search("(.+)\s\s(.+)\s\s(.+)", text)

    if bib:
        page_info = bib.group(3)

    return page_info
