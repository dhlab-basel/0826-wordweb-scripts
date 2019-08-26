# Regex library
import re

structure = {
    "Wo": {
        "value": "Wörtlich",
        "child": {
            "Mo": "word",
            "Ph": "Phrase (two words to two lines)",
            "Pa": "Passage (longer)"
        }
    },
    "Ve": {
        "value": "Verbal",
        "child": {
            "Kw": "Keywords",
            "Sn": "Snowclone",
            "Sp": "Setpiece (complete text)"
        }
    },
    "Na": {
        "value": "Name",
        "child": {
            "Ma": "Motif with name",
            "Hu": "Real person",
            "Ca": "Charactername",
            "Vn": "Venue or place",
            "Bo": "Booktitle"
        }
    },
    "Su": {
        "value": "Summarised",
        "child": {
            "Id": "Idea",
            "Me": "Plot element",
            "Mi": "Visual motif",
            "Pl": "Complete plot",
            "Sc": "Scene"
        }
    },
    "Cu": {
        "value": "Cluster",
        "child": {
            "Ti": "Tiger cluster",
            "Do": "Dog cluster",
            "Pi": "Pillow cluster",
            "Bt": "Blot cluster"
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
