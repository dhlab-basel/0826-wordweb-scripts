# csv library
import csv
# system library
import sys
# random library
import random

# helper for edition
import helper_edition as ed
# helper for secondary literature
import helper_secondary as sec
# helper for lexia
import helper_lexia as lex
# helper for company and venue
import helper_comp_venue as comp_ven
# helper for passage
import helper_passage as pas
# helper for comments
import helper_comment as comment
# prefix of title
import helper_prefix as pref
# my id generator
import id_generator as id
# my json handler
import json_handler as json
# preparation for authors
import prep_authors
# preparation for books
import prep_books
# preparation for contributors
import prep_contributors
# preparation for secondary books
import prep_sec_books
# preparation for lexias
import prep_lexias
# preparation for companies
import prep_companies
# preparation for venues
import prep_venues

# Files with data from HyperHamlet that should be imported
# export_1.csv is from Act 4, Scene 6, line "Let them come in."
# export_2.csv is from Act 4, Scene 6, line "I do not know from what part of the world"
# export_3.csv is from Act 4, Scene 6, line "I should be greeted, if not from Lord Hamlet."
# export_4.csv is from Act 4, Scene 6, line "Let him bless thee too."
# export_5.csv is from Act 4, Scene 6, line "He shall, sir, an't please him. There's a letter"
# export_6.csv is from Act 4, Scene 6, line "you, sir; it comes from the ambassador that was"
# export_7.csv is from Act 4, Scene 6, line "bound for England; if your name be Horatio, as I am"
# export_8.csv is from Act 4, Scene 6, line "let to know it is."
# export_9.csv is from Act 4, Scene 6, line "[Reads] 'Horatio, when thou shalt have overlooked."
# export_10.csv is from Act 4, Scene 6, line "this, give these fellows some means to the king:"
csv_files = [
    "01_prepare_scripts/csv/export_1.csv",
    "01_prepare_scripts/csv/export_2.csv",
    "01_prepare_scripts/csv/export_3.csv",
    "01_prepare_scripts/csv/export_4.csv",
    "01_prepare_scripts/csv/export_5.csv",
    "01_prepare_scripts/csv/export_6.csv",
    "01_prepare_scripts/csv/export_7.csv",
    "01_prepare_scripts/csv/export_8.csv",
    "01_prepare_scripts/csv/export_9.csv",
    "01_prepare_scripts/csv/export_10.csv"
]

# Every object contains all the resources of the same type which occurs in HyperHamlet.
allAuthors = prep_authors.prepare()
allBooks = prep_books.prepare()
allSecBooks = prep_sec_books.prepare_csv()
allContributors = prep_contributors.prepare()
allLexias = prep_lexias.prepare()
allCompanies = prep_companies.prepare()
allVenues = prep_venues.prepare()

# Saves all data the into json files
json.save("01_prepare_scripts/all_data/all_authors.json", allAuthors)
json.save("01_prepare_scripts/all_data/all_books.json", allBooks)
json.save("01_prepare_scripts/all_data/all_sec_books.json", allSecBooks)
json.save("01_prepare_scripts/all_data/all_contributors.json", allContributors)
json.save("01_prepare_scripts/all_data/all_lexias.json", allLexias)
json.save("01_prepare_scripts/all_data/all_companies.json", allCompanies)
json.save("01_prepare_scripts/all_data/all_venues.json", allVenues)

json_files = [
    "00_data_as_json/author.json",
    "00_data_as_json/book.json",
    "00_data_as_json/passage.json",
    "00_data_as_json/contributor.json",
    "00_data_as_json/lexia.json",
    "00_data_as_json/company.json",
    "00_data_as_json/venue.json"
]

# File with non-authors without entries
non_authors = "01_prepare_scripts/csv/non_authors.csv"

# File with non-theatre venues entries
non_venues = "01_prepare_scripts/csv/non_venues.csv"

# File where human-to-company information are listed
human_company = "01_prepare_scripts/csv/human_company.csv"

# Clears all json files
for file in json_files:
    json.clear(file)

# Loads the jsons and creates objects
authors = {}
books = {}
contributors = {}
lexias = {}
passages = {}
companies = {}
venues = {}

person_id_start = 7100


def create_author(auth_id):
    global person_id_start
    person_id_start = person_id_start + 1

    # Author with all the properties defined in the data_model_definition.json
    person = {
        "hasFirstName": allAuthors[auth_id]["hasFirstName"],
        "hasLastName": allAuthors[auth_id]["hasLastName"],
        "hasGender": allAuthors[auth_id]["hasGender"],
        "hasPersonInternalId": "#00" + str(person_id_start)
    }

    if "hasDescription" in allAuthors[auth_id]:
        person["hasDescription"] = allAuthors[auth_id]["hasDescription"]

    if "birthExact" in allAuthors[auth_id]:
        person["hasBirthDate"] = "GREGORIAN:{}".format(allAuthors[auth_id]["birthExact"])
    elif "birthStart" in allAuthors[auth_id]:
        person["hasBirthDate"] = "GREGORIAN:{}:{}".format(allAuthors[auth_id]["birthStart"],
                                                          allAuthors[auth_id]["birthEnd"])

    if "deathExact" in allAuthors[auth_id]:
        person["hasDeathDate"] = "GREGORIAN:{}".format(allAuthors[auth_id]["deathExact"])
    elif "deathStart" in allAuthors[auth_id]:
        person["hasDeathDate"] = "GREGORIAN:{}:{}".format(allAuthors[auth_id]["deathStart"],
                                                          allAuthors[auth_id]["deathEnd"])

    if "activeExact" in allAuthors[auth_id]:
        person["hasActiveDate"] = "GREGORIAN:{}".format(allAuthors[auth_id]["activeExact"])
    elif "activeStart" in allAuthors[auth_id]:
        person["hasActiveDate"] = "GREGORIAN:{}:{}".format(allAuthors[auth_id]["activeStart"],
                                                        allAuthors[auth_id]["activeEnd"])

    # Adding the new author to the list of authors
    authors[auth_id] = person


def update_author(auth_id, auth_int_id, lex_id):
    if auth_int_id:
        authors[auth_id]["hasPersonInternalId"] = auth_int_id

    if lex_id:
        authors[auth_id]["isLexiaPerson"] = lex_id


def update_actor(act_id, book_id):
    if act_id not in authors:
        create_author(act_id)

    if "performedByActor" not in books[book_id]:
        books[book_id]["performedByActor"] = []

    temp = set(books[book_id]["performedByActor"])
    temp.add(act_id)
    books[book_id]["performedByActor"] = list(temp)


def create_book(b_id, data_row, pub_info, pub_or_info, dates):
    book = {
        "hasBookInternalId": allBooks[b_id]["hasBookInternalId"],
        "hasBookTitle": allBooks[b_id]["hasBookTitle"],
        "isWrittenBy": [],
        "hasLanguage": data_row[9]
    }

    if "hasPrefixBookTitle" in allBooks[b_id]:
        book["hasPrefixBookTitle"] = allBooks[b_id]["hasPrefixBookTitle"]

    if data_row[5] and data_row[6]:
        if int(data_row[5]) < 1000:
            book["hasCreationDate"] = "GREGORIAN:1000:1000"
            book["hasBookExtraInfo"] = "Creation Date 1: {} | Creation Date 2: {}".format(data_row[5], data_row[6])
        else:
            book["hasCreationDate"] = "GREGORIAN:{}:{}".format(data_row[5], data_row[6])

    if "firstPerformanceExact" in dates:
        book["hasFirstPerformanceDate"] = "GREGORIAN:{}".format(dates["firstPerformanceExact"])
    elif "firstPerformanceStart" in dates:
        book["hasFirstPerformanceDate"] = "GREGORIAN:{}:{}".format(dates["firstPerformanceStart"],
                                                                   dates["firstPerformanceEnd"])

    if "publicationExact" in dates:
        book["hasPublicationDate"] = "GREGORIAN:{}".format(dates["publicationExact"])
    elif "publicationStart" in dates:
        book["hasPublicationDate"] = "GREGORIAN:{}:{}".format(dates["publicationStart"], dates["publicationEnd"])

    if "pubInfo" in pub_info:
        book["hasEdition"] = pub_info["pubInfo"]

    if "pubInfo" in pub_or_info:
        book["hasEditionHist"] = pub_or_info["pubInfo"]

    books[b_id] = book


def update_book(b_id, auth_names, pub_info, ven_id, comp_id, gen, sub, lex_id, com):
    if auth_names:
        # Iterates through the names per entry
        for auth_name in auth_names:

            # Generates author id
            auth_id = id.generate(auth_name)

            # Checks if author already exists
            if auth_id not in authors:
                print("Strange UPDATE BOOK")
                create_author(auth_id)
            else:
                temp = set(books[b_id]["isWrittenBy"])
                temp.add(auth_id)
                books[b_id]["isWrittenBy"] = list(temp)

    if pub_info:
        if "pubInfo" in pub_info and not "hasEdition" in books[b_id]:
            books[b_id]["hasEdition"] = pub_info["pubInfo"]

    if ven_id:
        if "performedIn" not in books[b_id]:
            books[b_id]["performedIn"] = []

        temp = set(books[b_id]["performedIn"])
        temp.add(ven_id)
        books[b_id]["performedIn"] = list(temp)

    if comp_id:
        if "performedBy" not in books[b_id]:
            books[b_id]["performedBy"] = []

        temp = set(books[b_id]["performedBy"])
        temp.add(comp_id)
        books[b_id]["performedBy"] = list(temp)

    if gen:
        if gen != "Theatre":
            if "hasGenre" not in books[b_id]:
                books[b_id]["hasGenre"] = []

            temp = set(books[b_id]["hasGenre"])
            temp.add(gen)
            books[b_id]["hasGenre"] = list(temp)

    if sub:
        if "hasSubject" not in books[b_id]:
            books[b_id]["hasSubject"] = []

        temp = set(books[b_id]["hasSubject"])
        temp.add(sub)
        books[b_id]["hasSubject"] = list(temp)

    if lex_id:
        books[b_id]["isLexiaBook"] = lex_id

    if com:
        if "hasBookComment" in com and "hasBookComment" not in books[b_id]:
            books[b_id]["hasBookComment"] = com["hasBookComment"]


def create_sec_book(sec_b_id, pub_info):
    book = {
        "hasBookInternalId": allSecBooks[sec_b_id]["hasBookInternalId"],
        "hasBookTitle": allSecBooks[sec_b_id]["hasBookTitle"],
        "hasEdition": pub_info["pubInfo"],
        "isWrittenBy": [],
        "hasLanguage": pub_info["hasLanguage"]
    }

    if "hasPrefixBookTitle" in allSecBooks[sec_b_id]:
        book["hasPrefixBookTitle"] = allSecBooks[sec_b_id]["hasPrefixBookTitle"]

    if "hasCreationDate" in pub_info and "hasPublicationDate" in pub_info:
        book["hasCreationDate"] = pub_info["hasCreationDate"]
        book["hasPublicationDate"] = pub_info["hasPublicationDate"]

    if "hasGenre" in pub_info:
        book["hasGenre"] = pub_info["hasGenre"]

    if "hasSubject" in pub_info:
        book["hasSubject"] = pub_info["hasSubject"]

    books[sec_b_id] = book


def update_sec_book(sec_b_id, auth_names):
    # Iterates through the names per entry
    for auth_name in auth_names:

        # Generates author id
        auth_id = id.generate(auth_name)

        # Checks if author already exists
        if auth_id not in authors:
            create_author(auth_id)

        temp = set(books[sec_b_id]["isWrittenBy"])
        temp.add(auth_id)
        books[sec_b_id]["isWrittenBy"] = list(temp)


def create_passage(pa_id, dis_tit, text, text_or, pub, pub_or):
    passage = {
        "hasText": text,
        "occursIn": [],
        "contains": [],
        "hasFunctionVoice": [],
        "hasStatus": "public"
    }

    if dis_tit:
        passage["hasDisplayedTitle"] = dis_tit["hasDisplayedTitle"]

        if "hasPrefixDisplayedTitle" in dis_tit:
            passage["hasPrefixDisplayedTitle"] = dis_tit["hasPrefixDisplayedTitle"]

    if text_or:
        passage["hasTextHist"] = text_or

    if "page" in pub:
        passage["hasPage"] = pub["page"]

    if "page" in pub_or:
        passage["hasPageHist"] = pub_or["page"]

    passages[pa_id] = passage


def update_passage(pa_id, bo_id, co_or_id, sec_pa_id, lex_id, res_fi, fc_vo, mark, com):
    if bo_id:
        passages[pa_id]["occursIn"] = bo_id

    if co_or_id:
        passages[pa_id]["wasContributedBy"] = co_or_id

    if sec_pa_id:
        if "isMentionedIn" not in passages[pa_id]:
            passages[pa_id]["isMentionedIn"] = []

        temp = set(passages[pa_id]["isMentionedIn"])
        temp.add(sec_pa_id)
        passages[pa_id]["isMentionedIn"] = list(temp)

    if lex_id:
        temp = set(passages[pa_id]["contains"])
        temp.add(lex_id)
        passages[pa_id]["contains"] = list(temp)

    if res_fi:
        passages[pa_id]["hasResearchField"] = res_fi

    if fc_vo:
        temp = set(passages[pa_id]["hasFunctionVoice"])
        temp.add(fc_vo)
        passages[pa_id]["hasFunctionVoice"] = list(temp)

    if mark:
        if "hasMarking" not in passages[pa_id]:
            passages[pa_id]["hasMarking"] = []

        temp = set(passages[pa_id]["hasMarking"])
        temp.add(mark)
        passages[pa_id]["hasMarking"] = list(temp)

    if com:
        if "hasPassageComment" in com:
            passages[pa_id]["hasPassageComment"] = com["hasPassageComment"]


def create_sec_passage(sec_pa_id, pag, sec_bo):
    passage = {
        "hasText": "-",
        "hasDisplayedTitle": sec_bo["hasDisplayedTitle"],
        "hasResearchField": ["Reading"],
        "hasFunctionVoice": ["Not defined"],
        "hasMarking": ["Unmarked"],
        "hasStatus": "public",
        "occursIn": []
    }

    if pag:
        passage["hasPage"] = pag

    if "hasPrefixDisplayedTitle" in sec_bo:
        passage["hasPrefixDisplayedTitle"] = sec_bo["hasPrefixDisplayedTitle"]

    # Set Regula Hohl Trillini as default contributor
    id_rh = id.generate("Hohl-Trillini Regula")
    if id_rh in allContributors:
        passage["wasContributedBy"] = id_rh

    passages[sec_pa_id] = passage


def update_sec_passage(sec_pa_id, sec_bo_id):
    if sec_bo_id:
        temp = set(passages[sec_pa_id]["occursIn"])
        temp.add(sec_bo_id)
        passages[sec_pa_id]["occursIn"] = list(temp)


def create_contributor(co_id):
    global person_id_start
    person_id_start = person_id_start + 1

    contributor = {
        "hasFirstName": allContributors[co_id]["hasFirstName"],
        "hasLastName": allContributors[co_id]["hasLastName"],
        "hasPersonInternalId": "#00" + str(person_id_start),
        "hasGender": allContributors[co_id]["hasGender"]
    }

    if "hasDescription" in allContributors[co_id]:
        contributor["hasDescription"] = allContributors[co_id]["hasDescription"]

    contributors[co_id] = contributor


def create_lexia(lex_id, le):
    lexias[lex_id] = le


def create_company(comp_id, comp):
    companies[comp_id] = comp


def update_company(comp_id, lex_id, human_id):
    if lex_id:
        companies[comp_id]["isLexiaCompany"] = lex_id

    if human_id:
        if "hasMember" not in companies[comp_id]:
            companies[comp_id]["hasMember"] = []

        temp = set(companies[comp_id]["hasMember"])
        temp.add(human_id)
        companies[comp_id]["hasMember"] = list(temp)


def create_venue(ven_id, ven):
    venues[ven_id] = ven


def update_venue(ven_id, lex_id):
    venues[ven_id]["isLexiaVenue"] = lex_id


def check_persons():
    # Checks if there are authors without internal id or last name
    for p in authors:
        if not "hasPersonInternalId" in authors[p]:
            print("Fail - Author without person internal ID: ", p, authors[p])
            raise SystemExit(0)

        if not "hasLastName" in authors[p]:
            print("Fail - Author without last name: ", p, authors[p])
            raise SystemExit(0)

    # Checks if there are contributors without internal id or last name
    for p in contributors:
        if not "hasPersonInternalId" in contributors[p]:
            print("Fail - Contributor without person internal ID: ", p, contributors[p])
            raise SystemExit(0)

        if not "hasLastName" in contributors[p]:
            print("Fail - Contributor without last name: ", p, contributors[p])
            raise SystemExit(0)


def check_books():
    book_check_successful = True
    for b in books:

        # Checks if there are books without internal id
        if not "hasBookInternalId" in books[b]:
            print("Fail - Book without book internal ID: ", b, books[b])
            raise SystemExit(0)

        # Checks if there are books without title
        if not "hasBookTitle" in books[b]:
            print("Fail - Book without book title: ", b, books[b])
            raise SystemExit(0)

        # Checks if there are books without edition
        if not "hasEdition" in books[b]:
            print("Fail - Book without edition: ", b, books[b])
            raise SystemExit(0)

        # Checks if there are books without language
        if not "hasLanguage" in books[b]:
            print("Fail - Book without language: ", b, books[b])
            raise SystemExit(0)

        # Checks if there are books without genre
        if not "hasGenre" in books[b]:
            print("Fail - Book without genre: ", b, books[b])
            raise SystemExit(0)
        elif len(books[b]["hasGenre"]) == 0:
            print("Fail - Book with empty Array hasGenre", b, books[b])
            book_check_successful = False

        # Checks if there are books without creation date
        if not "hasCreationDate" in books[b]:
            print("Fail - Book without creation date: ", b, books[b])
            raise SystemExit(0)

        # Checks if there are books without authors
        if not "isWrittenBy" in books[b]:
            print("Fail - Book without authors: ", b, books[b])
            raise SystemExit(0)
        elif len(books[b]["isWrittenBy"]) == 0:
            print("Fail - Book with empty Array isWrittenBy", b, books[b])
            book_check_successful = False

    if not book_check_successful:
        raise SystemExit(0)


def check_passages():
    passage_check_successful = True
    for p in passages:

        # Checks if there are passages without text
        if not "hasText" in passages[p]:
            print("Fail - Passage without edition: ", p, passages[p])
            raise SystemExit(0)

        # Checks if there are passages without displayed title
        if not "hasDisplayedTitle" in passages[p]:
            print("Fail - Passage without displayed title: ", p, passages[p])
            raise SystemExit(0)

        # Checks if there are passages without research field
        if not "hasResearchField" in passages[p]:
            print("Fail - Passage without research field: ", p, passages[p])
            raise SystemExit(0)

        # Checks if there are passages without function voice
        if not "hasFunctionVoice" in passages[p]:
            print("Fail - Passage without function voice: ", p, passages[p])
            raise SystemExit(0)
        elif len(passages[p]["hasFunctionVoice"]) == 0:
            print("Fail - Passage with empty Array hasFunctionVoice", p, passages[p])
            passage_check_successful = False

        # Checks if there are passages without markings
        if not "hasMarking" in passages[p]:
            print("Fail - Passage without marking: ", p, passages[p])
            raise SystemExit(0)
        elif len(passages[p]["hasMarking"]) == 0:
            print("Fail - Passage with empty Array hasMarking", p, passages[p])
            passage_check_successful = False

        # Checks if there are passages without status
        if not "hasStatus" in passages[p]:
            print("Fail - Passage without status: ", p, passages[p])
            raise SystemExit(0)
        elif len(passages[p]["hasStatus"]) == 0:
            print("Fail - Passage with empty Array hasStatus", p, passages[p])
            passage_check_successful = False

        # Checks if there are passages not occurring in a book
        if not "occursIn" in passages[p]:
            print("Fail - Passage not occurring in a book: ", p, passages[p])
            raise SystemExit(0)
        elif len(passages[p]["occursIn"]) == 0:
            print("Fail - Passage with empty Array occursIn", p, passages[p])
            passage_check_successful = False

        # Checks if there are passages without contributor
        if not "wasContributedBy" in passages[p]:
            print("Fail - Passage without contributor: ", p, passages[p])
            raise SystemExit(0)
        elif len(passages[p]["wasContributedBy"]) == 0:
            print("Fail - Passage with empty Array wasContributedBy", p, passages[p])
            passage_check_successful = False

    if not passage_check_successful:
        raise SystemExit(0)


def check_lexias():
    lexia_check_successful = True
    for l in lexias:

        # Checks if there are lexias without internal id
        if not "hasLexiaInternalId" in lexias[l]:
            print("Fail - Lexia without lexia internal ID: ", l, lexias[l])
            raise SystemExit(0)

        # Checks if there are lexias without title
        if not "hasLexiaTitle" in lexias[l]:
            print("Fail - Lexia without lexia title: ", l, lexias[l])
            raise SystemExit(0)

        # Checks if there are lexias without formal classes
        if not "hasFormalClass" in lexias[l]:
            print("Fail - Lexia without formal class: ", l, lexias[l])
            raise SystemExit(0)
        elif len(lexias[l]["hasFormalClass"]) == 0:
            print("Fail - Lexia with empty Array hasFormalClass", l, lexias[l])
            lexia_check_successful = False

        # Checks if there are lexias without displayed title
        if not "hasLexiaDisplayedTitle" in lexias[l]:
            print("Fail - Lexia without displayed lexia title: ", l, lexias[l])
            raise SystemExit(0)

    if not lexia_check_successful:
        raise SystemExit(0)


def check_companies():
    for c in companies:

        # Checks if there are company without internal id
        if not "hasCompanyInternalId" in companies[c]:
            print("Fail - Company without company internal ID: ", c, companies[c])
            raise SystemExit(0)

        # Checks if there are company without title
        if not "hasCompanyTitle" in companies[c]:
            print("Fail - Company without company title: ", c, companies[c])
            raise SystemExit(0)


def check_venues():
    for v in venues:

        # Checks if there are venue without internal id
        if not "hasVenueInternalId" in venues[v]:
            print("Fail - Venue without venue internal ID: ", v, venues[v])
            raise SystemExit(0)

        # Checks if there are venue without place venue
        if not "hasPlaceVenue" in venues[v]:
            print("Fail - Venue without place venue: ", v, venues[v])
            raise SystemExit(0)


def start():
    # Reads the csv files
    for csv_file in csv_files:

        try:
            with open(csv_file) as f:
                csv_reader = csv.reader(f, delimiter=';')

                # line number in csv file
                line = 0

                for row in csv_reader:

                    # Skip first row with column title
                    if line != 0:

                        # ---------- AUTHOR
                        # Multiple names of authors
                        names = row[2].split(" / ")

                        # Iterates through the names per entry
                        for name in names:

                            # Generates author id
                            author_id = id.generate(name)

                            # Checks if author_id is valid
                            if author_id not in allAuthors:
                                print("FAIL Author", author_id, line, csv_file)
                                raise SystemExit(0)

                            # Creates author if it does not exist
                            if author_id not in authors:
                                create_author(author_id)

                        # ---------- BOOK
                        # Extracts internal id and title
                        key_id, key_title = prep_books.get_key_for_id(row[13])

                        # Generates book id
                        if key_id and key_title:
                            book_id = id.generate("{} {}".format(key_id, key_title))
                        else:
                            print("FAIL Book Title & ID", row[13], line, csv_file)
                            raise SystemExit(0)

                        # Checks if book_id is valid
                        if book_id not in allBooks:
                            print("FAIL Book", book_id, row[13], line, csv_file)
                            raise SystemExit(0)

                        publication = ed.info(row[4])
                        publication_original = ed.info(row[26])

                        # Creates the book if its new
                        if book_id not in books:
                            create_book(book_id, row, publication, publication_original, allBooks[book_id])

                        # Comments
                        comments = comment.info(row[11])

                        # Updates the author references, genre and comment
                        update_book(book_id, names, publication, None, None, row[18], None, None, comments)

                        # ------------- PASSAGE

                        # ##### Variant 1 (old) #####
                        # Generates passage id
                        # passage_id = id.generate(row[10])

                        # ##### Variant 2 (new) #####
                        # Generates passage id with random generator
                        unique_key = random.randint(1000000, 9999999)
                        passage_id = id.generate(str(unique_key))

                        # Extracts displayed title and prefix
                        pass_title = pref.get_prefix_passage(row[3], {})

                        # Creates the passage and updates the edition reference
                        if passage_id not in passages:
                            create_passage(passage_id, pass_title, row[10], row[25], publication, publication_original)

                        # Updates the book reference and passage comment
                        update_passage(passage_id, book_id, None, None, None, None, None, None, comments)

                        # Multiple subjects
                        subjects = row[19].split(" / ")

                        for subject in subjects:
                            update_book(book_id, None, None, None, None, None, subject, None, None)

                        # Function voice
                        f_voices = row[21].split(" / ")

                        for f_voice in f_voices:

                            if f_voice == "BODY OF TEXT" and row[20]:
                                narratives = row[20].split(" / ")

                                for narrative in narratives:
                                    update_passage(passage_id, None, None, None, None, None, narrative, None, None)
                            elif f_voice == "BODY OF TEXT" and not row[20]:
                                update_passage(passage_id, None, None, None, None, None, "Not defined", None, None)
                            elif not f_voice and row[20]:
                                print("FAIL - No function but narrative", row[20], csv_file, line)
                                raise SystemExit(0)
                            else:
                                update_passage(passage_id, None, None, None, None, None, f_voice, None, None)

                        # Evaluates markings
                        # Checks if column is empty and sets unmarked
                        work_value = "Work unmarked" if not row[16] else row[16]
                        author_value = "Author unmarked" if not row[17] else row[17]

                        if (work_value == "Work unmarked" and author_value == "Author unmarked" and not row[22]) or (
                                work_value == "Work unmarked" and author_value == "Author unmarked" and
                                row[22] == "Local reference"):
                            update_passage(passage_id, None, None, None, None, None, None, "Unmarked", None)
                        else:

                            if work_value != "Work unmarked":
                                # Checks if work marking has multiple values
                                if " / " in work_value:
                                    work_marked = row[16].split(" / ")

                                    for w_m in work_marked:
                                        update_passage(passage_id, None, None, None, None, None, None, w_m, None)
                                else:
                                    update_passage(passage_id, None, None, None, None, None, None, work_value,
                                                   None)

                            if author_value != "Author unmarked":
                                update_passage(passage_id, None, None, None, None, None, None, author_value, None)

                            if row[22]:
                                for marking in pas.get_marking(row[22]):
                                    update_passage(passage_id, None, None, None, None, None, None, marking, None)

                        # ------------- CONTRIBUTOR
                        # Generates contributor id
                        contributor_id = id.generate(row[27].strip())

                        # Checks if contributor_id is valid
                        if contributor_id not in allContributors:
                            print("FAIL Contributor", contributor_id, csv_file, line)
                            raise SystemExit(0)

                        # Creates the contributor and updates the passage reference
                        if contributor_id not in contributors:
                            create_contributor(contributor_id)

                        # Updates the contributor reference
                        update_passage(passage_id, None, contributor_id, None, None, None, None, None, None)

                        # -------------- SECONDARY BOOK
                        sec_books = sec.info(row[24], line, csv_file)

                        # Sets the research field "Reading" when there is no sec books
                        if len(sec_books) == 0:
                            update_passage(passage_id, None, None, None, None, "Reading", None, None, None)

                        for sec_book in sec_books:

                            sec_book_id = id.generate(sec_book["id"])

                            # Checks if sec book id is valid
                            if sec_book_id not in allSecBooks:
                                print("FAIL Secondary Book", sec_book["id"], csv_file, line, row[24])
                                raise SystemExit(0)

                            s_book = allSecBooks[sec_book_id]

                            if sec_book_id not in books:
                                create_sec_book(sec_book_id, s_book)

                            # Sets the default research field
                            if "Fulltext database" in s_book["hasGenre"]:
                                update_passage(passage_id, None, None, None, None, "Electronic Search", None, None, None)

                            # Sets the research field
                            if not "Fulltext database" in s_book["hasGenre"]:
                                update_passage(passage_id, None, None, None, None, "Previous Research", None, None, None)

                            # Updates the authors reference
                            update_sec_book(sec_book_id, s_book["authors"])

                            # Creates sec passage id with random generator
                            unique_key = random.randint(100000, 999999)
                            sec_passage_id = id.generate(str(unique_key))

                            create_sec_passage(sec_passage_id, sec_book["page"], s_book)
                            update_sec_passage(sec_passage_id, sec_book_id)
                            update_passage(passage_id, None, None, sec_passage_id, None, None, None, None, None)

                        # --------------- COMPANY & VENUES
                        if row[12]:
                            comp_ven_names = row[12].split(" / ")

                            for comp_ven_name in comp_ven_names:
                                comp_ven_data, type_1 = comp_ven.info(comp_ven_name, line, csv_file)

                                if type_1 == "venue":
                                    unique_key = "{} {}".format(comp_ven_data["hasVenueInternalId"],
                                                                comp_ven_data["hasPlaceVenue"])

                                    venue_id = id.generate(unique_key)

                                    if venue_id not in allVenues:
                                        print("FAIL Venue", venue_id, line, csv_file)

                                    if venue_id not in venues:
                                        create_venue(venue_id, comp_ven_data)

                                    # Updates the venue reference
                                    update_book(book_id, None, None, venue_id, None, None, None, None, None)

                                elif type_1 == "company":
                                    company_id = id.generate(comp_ven_data["hasCompanyInternalId"])

                                    if company_id not in allCompanies:
                                        print("FAIL Company", company_id, line, csv_file)

                                    if company_id not in companies:
                                        create_company(company_id, comp_ven_data)

                                    # Updates the company reference
                                    update_book(book_id, None, None, None, company_id, None, None, None, None)

                        # --------------- LEXIA
                        # Multiple names of authors
                        lex_names = row[15].split(" / ")

                        for lex_name in lex_names:
                            le = lex.info(lex_name, line, csv_file)

                            # Creates a key which has the following format {title internalID}.
                            # {internalID title} will cause error later because it already exists
                            unique_key = "{} {}".format(le["hasLexiaTitle"], le["hasLexiaInternalId"])

                            lexia_id = id.generate(unique_key)

                            if lexia_id not in allLexias:
                                print("FAIL Lexia", lexia_id, le, line, csv_file)
                                raise SystemExit(0)

                            if lexia_id not in lexias:
                                create_lexia(lexia_id, le)

                            # Updates the lexia reference
                            update_passage(passage_id, None, None, None, lexia_id, None, None, None, None)

                            isLexiaAuthor = id.generate(le["hasLexiaTitle"])
                            if isLexiaAuthor in authors:
                                # Internal ID of author must be overwritten because it is generated
                                # from incrementation and in this case the ID comes from the user
                                update_author(isLexiaAuthor, le["hasLexiaInternalId"], lexia_id)

                            key = "{} {}".format(le["hasLexiaInternalId"], le["hasLexiaTitle"])
                            isLexiaBookVenue = id.generate(key)

                            if isLexiaBookVenue in books:
                                update_book(isLexiaBookVenue, None, None, None, None, None, None, lexia_id, None)

                            if isLexiaBookVenue in venues:
                                update_venue(isLexiaBookVenue, lexia_id)

                            isLexiaCompany = id.generate(le["hasLexiaInternalId"])
                            if isLexiaCompany in companies:
                                update_company(isLexiaCompany, lexia_id, None)

                        # --------------- ACTORS
                        if row[14]:
                            actors = row[14].split(" / ")

                            for actor in actors:

                                # Generates author id
                                actor_id = id.generate(actor)

                                # Checks if author_id is valid
                                if actor_id in allAuthors:
                                    update_actor(actor_id, book_id)

                    line += 1

        except Exception as err:
            print("FAIL: start.py", err, line, csv_file)
            raise SystemExit(0)

    # ------------------------------------------
    # Adds non-authors which do not have entries
    try:
        with open(non_authors) as a:

            csv_reader = csv.reader(a, delimiter=";")

            # line number in csv file
            line2 = 0

            for row in csv_reader:

                # Skip first row with column title
                if line2 != 0:

                    # Multiple names of authors
                    names = row[2].split(" / ")

                    # Iterates through the names per entry
                    for name in names:

                        # Generates author id
                        author_id = id.generate(name)

                        # Checks if author_id is valid
                        if author_id not in allAuthors:
                            print("FAIL Non-Author", author_id, line2, non_authors)
                            raise SystemExit(0)

                        # Creates author if it does not exist
                        if author_id not in authors:
                            create_author(author_id)

                line2 += 1

    except Exception as err:
        print("FAIL: non_authors.csv")
        raise SystemExit(0)

    # ------------------------------------------
    # Adds non-venues which are not linked in the regular entries
    try:
        with open(non_venues) as v:

            csv_reader = csv.reader(v, delimiter=";")

            # line number in csv file
            line3 = 0

            for row in csv_reader:

                # Skip first row with column title
                if line3 != 0:

                    ven_names = row[12].split(" / ")

                    for ven_name in ven_names:
                        ven_data, type_2 = comp_ven.info(ven_name, line3, non_venues)

                        if type_2 == "venue":
                            unique_key = "{} {}".format(ven_data["hasVenueInternalId"],
                                                        ven_data["hasPlaceVenue"])

                            venue_id = id.generate(unique_key)

                            if venue_id not in allVenues:
                                print("FAIL Non-Venues", venue_id, line3, non_venues)
                                raise SystemExit(0)

                            if venue_id not in venues:
                                create_venue(venue_id, ven_data)

                line3 += 1

    except Exception as err:
        print("FAIL: non_venues.csv")
        raise SystemExit(0)

    # ------------------------------------------
    # Sets relation between human and company
    try:
        with open(human_company) as h:

            csv_reader = csv.reader(h, delimiter=';')

            # line number in csv file
            line4 = 0

            for row in csv_reader:

                # Skip first row with column title
                if line4 != 0:

                    # Generates id for human
                    human_id = id.generate(row[2])

                    # Checks if author_id is valid
                    if human_id not in allAuthors:
                        print("FAIL human_company -> human", author_id, line4, human_company)
                        raise SystemExit(0)

                    comp_names = row[12].split(" / ")

                    for comp_name in comp_names:
                        comp_data, type_3 = comp_ven.info(comp_name, line, human_company)

                        if type_3 == "company":

                            # Generates id for company
                            company_id = id.generate(comp_data["hasCompanyInternalId"])

                            # Checks if company_id is valid
                            if company_id not in allCompanies:
                                print("FAIL human_company -> company", company_id, line, human_company)
                                raise SystemExit(0)

                            # Creates company if it does not exist
                            if company_id not in companies:
                                create_company(company_id, comp_data)

                            # Creates author if it does not exist
                            if human_id not in authors:
                                create_author(human_id)

                            # Adds the human to the company
                            update_company(company_id, None, human_id)

                line4 += 1

    except Exception as err:
        print("FAIL: human_company.csv")
        raise SystemExit(0)

    # ------------------------------------------
    # Saves the objects which occurs in the csv files in to json files
    json.save(json_files[0], authors)
    json.save(json_files[1], books)
    json.save(json_files[2], passages)
    json.save(json_files[3], contributors)
    json.save(json_files[4], lexias)
    json.save(json_files[5], companies)
    json.save(json_files[6], venues)

    # Checks all the cardinality
    check_persons()
    check_books()
    check_passages()
    check_lexias()
    check_companies()
    check_venues()
