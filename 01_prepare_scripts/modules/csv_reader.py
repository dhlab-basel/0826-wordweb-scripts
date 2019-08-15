# csv library
import csv


# Loading files
def read(file_name):
    try:
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line = 0
            for row in csv_reader:
                # print(row[2])
                line += 1

    except Exception as err:
        print(err, file_name)
        raise SystemExit(0)
