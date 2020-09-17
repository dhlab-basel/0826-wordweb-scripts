# Regex library
import re

formClass_structure = {
    "Wo": {
        "value": "Verbal",
        "child": {
            "Mo": "Word",
            "To": "Two-word item",
            "Ph": "Phrase",
            "Pa": "Passage",
            "Pu": "Pun",
            "Sn": "Snowclone",
            "Kw": "Keywords",
            "Sp": "Setpiece"
        }
    },
    "Na": {
        "value": "Name",
        "child": {
            "Ma": "Motif with name",
            "Hu": "Name of real person",
            "Ep": "Epithet for real person",
            "Ca": "Name of fictional character",
            "Vn": "Venue or place",
            "Bo": "Book title",
            "Co": "Company"
        }
    },
    "Su": {
        "value": "Paraphrased",
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
            "Bt": "Blot cluster",
            "Ki": "Kite cluster",
            "Wa": "Wax cluster"
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
            "Foo": "Food",
            "Clo": "clothes, hair, cosmetics",
            "Med": "medicine"
        }
    },
    "Gen": {
        "value": "Gender",
        "child": {
            "Wom": "Women",
            "Men": "Men",
            "Mar": "Marriage"
        }
    },
    "New": {
        "value": "News",
        "child": {
            "Cur": "Other Current events",
            "Per": "Persons",
            "Ven": "Venues",
            "Com": "companies",
            "Wot": "War of the Theatres"
        }
    },
    "Cul": {
        "value": "Culture",
        "child": {
            "War": "war, combat",
            "Cou": "Court, monarchy",
            "Mus": "Music, dance, song",
            "Rel": "religion",
            "The": "Theatre",
            "Edu": "education"
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
            "hasLexiaInternalId": lexia_info.group(4),
            "hasLexiaTitle": lexia_info.group(6)
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

                # Creates displayed title (= Hashtag)
                disTitle = lexia_info.group(6).replace(" ", "_")
                # Adds prefix for passage
                if lexia["hasFormalClass"] == "Passage":
                    disTitle = "PASSAGE_" + disTitle
                lexia["hasLexiaDisplayedTitle"] = "#" + disTitle

    return lexia
