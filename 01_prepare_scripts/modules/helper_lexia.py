# Regex library
import re

formClass_structure = {
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

images_structure = {
    "Nat": {
        "value": "Nature",
        "child": {
            "Pla": "Plants",
            "Bir": "Birds",
            "Ani": "Animals",
            "Lan": "Landscape",
            "Sky": "Sky and wether"
        }
    },
    "Rea": {
        "value": "Daily reality",
        "child": {
            "Cur": "Current events",
            "Foo": "Food",
            "Clo": "clothes, hair, cosmetics",
            "Med": "medicine"
        }
    },
    "Cul": {
        "value": "Culture",
        "child": {
            "War": "war, combat",
            "Cou": "Court, monarchy",
            "Mus": "Music, dance song",
            "Rel": "religion"
        }
    },
    "Abs": {
        "value": "Abstract ideas",
        "child": {
            "Tim": "Time",
            "Dea": "Death",
            "Lov": "Love"
        }
    }
}


def info(text, line, csv_file):

    lexia = {}

    # lexia_info = re.search("^(\w\w)(\w\w)((#|@)\d{6})\s(.*)", text)
    lexia_info = re.search("^(\w\w)(\w\w)(.*)((#|@)\d{6})\s(.*)", text)

    if lexia_info:

        lexia = {
            "lexiaInternalId": lexia_info.group(4),
            "lexiaTitle": lexia_info.group(6)
        }

        images_infos = re.findall("_\w\w\w\w\w\w", lexia_info.group(3))

        for images_info in images_infos:
            images_levels = re.search("^_(\w\w\w)(\w\w\w)", images_info)

            if images_levels:
                if images_structure.get(images_levels.group(1)):
                    if images_structure.get(images_levels.group(1))["child"].get(images_levels.group(2)):
                        if "hasImage" not in lexia:
                            lexia["hasImage"] = []

                        temp = set(lexia["hasImage"])
                        temp.add(images_structure.get(images_levels.group(1))["child"].get(images_levels.group(2)))
                        lexia["hasImage"] = list(temp)

        if formClass_structure.get(lexia_info.group(1)):
            if formClass_structure.get(lexia_info.group(1))["child"].get(lexia_info.group(2)):
                lexia["hasFormalClass"] = formClass_structure.get(lexia_info.group(1))["child"].get(lexia_info.group(2))
                # print(structure.get(lexias.group(1), "fail " + lexias.group(1)))

    return lexia
