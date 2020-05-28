# Regex library
import re


def info(text):

    comment = {}

    pass_comment = re.search("\*\s(.+)", text)

    if pass_comment:

        book_comment = re.search("\*\*\s(.+)", text)

        if book_comment:
            comment["hasBookComment"] = book_comment.group(1)
        else:
            comment["hasPassageComment"] = pass_comment.group(1)

    return comment
