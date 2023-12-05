import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="pjh",
    password="1234",
    database="shopping_db"
)

def fetch_from_db():
    cursor = db.cursor()
    sql = "SELECT * FROM images_table ORDER BY time DESC LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[1], result[0]
