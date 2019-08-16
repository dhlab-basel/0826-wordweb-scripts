# Regex library
import re

structure = {
    "Wo": {
        "value": "Wörtlich",
        "child": {
            "Mo": "Word",
            "Ph": "Phrase or sentence",
            "Pa": "Passage"
        }
    },
    "Ve": {
        "value": "Verbal",
        "child": {
            "Kw": "Keywords",
            "Sn": "Snowclone",
            "Sp": "Setpiece"
        }
    },
    "Na": {
        "value": "Name",
        "child": {
            "Ma": "Motif with Name",
            "Hu": "Human",
            "Ca": "Character",
            "Vn": "Venue or place",
            "Bo": "Book"
        }
    },
    "Su": {
        "value": "Summarised",
        "child": {
            "Id": "Idea",
            "Me": "Motif (plot element)",
            "Mi": "Motif (visual image, needn't be a metaphor)",
            "Pl": "Plot (complete action)",
            "Sc": "Scene"
        }
    },
    "Cu": {
        "value": "Cluster",
        "child": {
            "Ti": "Tiger",
            "Do": "Dog",
            "Pi": "Pillow",
            "Bt": "Blot"
        }
    }
}


def info(text, line, csv_file):

    lexia = {}

    lexia_info = re.search("^(\w\w)(\w\w)((#|@)\d{6})\s(.*)", text)

    if lexia_info:

        lexia = {
            "lexiaInternalId": lexia_info.group(3),
            "lexiaTitle": lexia_info.group(5)
        }

        if structure.get(lexia_info.group(1)):
            if structure.get(lexia_info.group(1))["child"].get(lexia_info.group(2)):
                lexia["formalClass"] = structure.get(lexia_info.group(1))["child"].get(lexia_info.group(2))
                # print(structure.get(lexias.group(1), "fail " + lexias.group(1)))

    return lexia
