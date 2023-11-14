from flask import Flask, render_template, redirect, url_for
import mysql.connector
import cv2
import time
from gpiozero import MotionSensor

def fetch_from_db():
    db = mysql.connector.connect(
        host="localhost",
        user="ubuntu",
        password="1234567890",
        database="shopping_db"
    )
    cursor = db.cursor()
    sql = "SELECT * FROM yourtable ORDER BY time DESC LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[1], result[0]   # 1: 이미지 데이터, 0: 시간

app = Flask(__name__)

@app.route('/')
def home():
    # 인체감지코드 실행 / db 저장
    detect_and_save()
    return render_template('home.html')

@app.route('/move', methods=['POST'])
def move():
    return redirect(url_for('display'))

@app.route('/display')
def display():
    # 이미지, 시간 정보 db에서 검색
    img_data, capture_time = fetch_from_db()
    img_url = url_for('static', filename='capture.jpg')
    return render_template('display.html', img_data=img_data, capture_time=capture_time)

if __name__ == "__main__":
    app.run(debug=True)

def detect_and_save():
    pin = MotionSensor(7) # 센서의 GPIO 번호

    db = mysql.connector.connect(
        host="localhost",
        user="ubuntu",
        password="1234567890",
        database="shopping_db"
    )
    while True:
        if pin.motion_detected:
            print("!!!!!!!")
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 440)

            ret, frame = cap.read() # 캡쳐
            cap.release()
            cv2.destroyAllWindows()

            if ret:
                cv2.imwrite('capture.jpg', frame)
                with open('capture.jpg', 'rb') as f:
                    binary_data = f.read()
                current_time = time.strftime('%Y-%m-%d %H:%M:%S')
                cursor = db.cursor()
                sql = "INSERT INTO yourtable (current_time, image) VALUES (%s, %s)"
                val = (current_time, binary_data)
                cursor.execute(sql, val)
                db.commit()
