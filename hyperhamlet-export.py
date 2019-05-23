import pymysql

try:
    conn = pymysql.connect(host='localhost', user='vitsch', password='test', database='HAMLET')

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM authors"

    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print(row["lastname"])
    conn.close()
    cursor.close()
except Exception as err:
    print(err)
