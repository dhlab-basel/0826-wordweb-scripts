# Regex library
import re


def get_prefix_book(title, book):
    def_article = re.search("^([Tt]he)\s(.*)", title)
    undef_article = re.search("^([Aa]n?)\s(.*)", title)

    if def_article:
        book["hasPrefixBookTitle"] = def_article.group(1)
        book["hasBookTitle"] = def_article.group(2)
    elif undef_article:
        book["hasPrefixBookTitle"] = undef_article.group(1)
        book["hasBookTitle"] = undef_article.group(2)
    else:
        book["hasBookTitle"] = title

    return book


def get_prefix_passage(title, passage):
    def_article = re.search("^([Tt]he)\s(.*)", title)
    undef_article = re.search("^([Aa]n?)\s(.*)", title)

    if def_article:
        passage["hasPrefixDisplayedTitle"] = def_article.group(1)
        passage["hasDisplayedTitle"] = def_article.group(2)
    elif undef_article:
        passage["hasPrefixDisplayedTitle"] = undef_article.group(1)
        passage["hasDisplayedTitle"] = undef_article.group(2)
    else:
        passage["hasDisplayedTitle"] = title

    return passage
