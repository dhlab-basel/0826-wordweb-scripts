# system library
import sys
# Regex library
import re


def info(text, line, csv_file):

    books = []

    first_line = re.search("(.+)\n", text)

    if first_line:
        infos = first_line.group(1).split("/")

        for info_1 in infos:
            id = re.search("(@\d{6})$", info_1)
            if not id:
                page = re.search("(@\d{6})-(.+)", info_1)
                if page:
                    book = {
                        "id": page.group(1),
                        "page": page.group(2)
                    }

                    books.append(book)
                else:
                    print(csv_file, line, text)
            else:
                book = {
                    "id": id.group(1),
                    "page": "no page"
                }

                books.append(book)

    else:
        infos = text.split("/")

        for info_2 in infos:
            id = re.search("(@\d{6})$", info_2)
            if not id:
                page = re.search("(@\d{6})-(.+)", info_2)
                if page:
                    book = {
                        "id": page.group(1),
                        "page": page.group(2)
                    }

                    books.append(book)
                else:
                    print(csv_file, line, text)
            else:
                book = {
                    "id": id.group(1),
                    "page": "no page"
                }
                books.append(book)

    return books
