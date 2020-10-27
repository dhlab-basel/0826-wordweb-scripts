# Regex library
import re


def get_marking(text):

    marking_leaf = []

    markings = text.split(" / ")

    for marking in markings:

        m1 = re.search("MQ_(.+)", marking)

        if m1:
            m2 = re.search("_(.+)", m1.group(1))

            if m2:
                marking_leaf.append(m2.group(1))
            else:
                marking_leaf.append(m1.group(1))

    return marking_leaf


def get_prefix(title):
    passage = {}
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
