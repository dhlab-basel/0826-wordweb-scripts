import csv
import re
import pymysql

with open('export.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        # print(row[13])



        try:
            conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

            cursor = conn.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT id, name FROM linecategories WHERE name='" + row[13] + "'"

            cursor.execute(sql)

            results = cursor.fetchall()

            for rowLineCat in results:
                print(rowLineCat)

            conn.close()
            cursor.close()
        except Exception as err:
            print("Bye", err, row)





        if line_count != 0 and row[13] is not None:
            birth = re.search("(@\d{6})(.*)", row[13])
            # if birth is not None:
                # print(birth.groups())

        line_count += 1
    print("line count", line_count)