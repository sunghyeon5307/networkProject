from db_connect import connect_db

def fetch_from_db():
    cursor = db.cursor()
    sql = "SELECT * FROM images_table ORDER BY time DESC LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[1], result[0]   # 1: 이미지 데이터, 0: 시간
