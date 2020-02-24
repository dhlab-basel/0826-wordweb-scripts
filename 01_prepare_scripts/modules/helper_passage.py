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
