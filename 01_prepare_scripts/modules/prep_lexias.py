# mySQL library
import pymysql
# Regex library
import re
# JSON library
import json

# my id generator
import id_generator as id

structure = {
    "Wo": {
        "value": "Woertlich",
        "child": {
            "Mo": "Word",
            "Ph": "Phrase or sentence",
            "Sn": "Snowclone",
            "Pa": "Passage"
        }
    },
    "Ve": {
        "value": "Verbal",
        "child": {
            "Kw": "Keywords",
            "Sp": "Setpiece"
        }
    },
    "Na": {
        "value": "Name",
        "child": {
            "Mo": "Motif with Name",
            "Hu": "Human",
            "Ca": "Character",
            "Ve": "Venue or place",
            "Bo": "Book"
        }
    },
    "Su": {
        "value": "Summarised",
        "child": {
            "Id": "Idea",
            "Mo": "Motif",
            "Pl": "Plot",
            "Sc": "Scene"
        }}
}


def prepare():
    try:
        conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sql = 'SELECT * FROM modifications'

        cursor.execute(sql)

        results = cursor.fetchall()

        # Contains all the lexias from hyperhamlet. Key of the lexia object is {internalID title}
        all_lexia = {}

        for row in results:
            lexias = re.search('(\w\w)(\w\w)#(\d{6})\s(.*)', row['name'])

            # if lexias:
            #
            #     print(structure.get(lexias.group(1), "fail " + lexias.group(1)))

        conn.close()
        cursor.close()

        return all_lexia

    except Exception as err:
        print(err)
