import csv
import re
import pymysql
import pandas

with open('export.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    copied = 0
    pi = {}
    data = []
    for row in csv_reader:

        publicationInfo = re.search("(.+)\s\s(.+)\s\s(.+)", row[4])
        if publicationInfo:
            # print(line_count, publicationInfo.groups())
            letterName = re.search("\"(.+)\"\s(.*)", publicationInfo.group(2))
            if letterName:
                data.append([line_count, publicationInfo.group(1), letterName.group(1), letterName.group(2), publicationInfo.group(3)])
                # print(line_count, "author: " + publicationInfo.group(1) + " | lettername: " + letterName.group(1) + " | pubInfo: " + letterName.group(2) + " | page: " + publicationInfo.group(3))
            else:
                data.append([line_count, publicationInfo.group(1), None, publicationInfo.group(2), publicationInfo.group(3)])
                # print(line_count, "author: " + publicationInfo.group(1) + " | pubInfo: " + publicationInfo.group(2) + " | page: " + publicationInfo.group(3))
            # if publicationInfo.group(2) in pi:
            #     cla = 0
            # else:
            #     copied +=1
            #     pi[publicationInfo.group(2)] = row[1]
            #
            # if publicationInfo.group(2) in pi:
            #     cla = 0
            # else:
            #     print(" 2 not here")
        else:
            onlyPubInfo = re.search("(.+)\s\s(.+)", row[4])
            if onlyPubInfo:
                lName = re.search("\"(.+)\"\s(.*)", onlyPubInfo.group(2))
                if lName:
                    data.append([line_count, onlyPubInfo.group(1), lName.group(1), lName.group(2), None])
                    # print(line_count, "author: " + onlyPubInfo.group(1) + " | lettername: " + lName.group(1) + " | pubInfo: " + lName.group(2))
                else:
                    data.append([line_count, onlyPubInfo.group(1), None, onlyPubInfo.group(2), None])
                    # print(line_count, "author: " + onlyPubInfo.group(1) + " | pubInfo: " + onlyPubInfo.group(2))
            else:
                print(line_count, "FAIL")
        line_count += 1
    print("line count", line_count)

    df = pandas.DataFrame(data, columns=['Number', 'Author', 'LetterName', 'PubInfo', 'Page'])
    pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_colwidth', 100)

    print(df)

    # Print all the values in the object
    # for b in pi:
    #     print(b)


# Output file
# with open('bla.csv', mode='w') as write_file:
#     writer = csv.writer(write_file, delimiter=';')
#     for b in pi:
#         writer.writerow([b])


# Check each character of string
# user_score = 0
# simon_pattern = "RRGBRYYBGY"
# user_pattern  = "RRGBBRYBGY"
#
# for i in range(len(user_pattern)):
#     if user_pattern[i] is simon_pattern[i]:
#        user_score += 1
#
# print("User score:", user_score, len(simon_pattern))