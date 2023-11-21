from flask import Flask, render_template, redirect, url_for
import mysql.connector
import cv2
import time
from gpiozero import MotionSensor
import base64

db = mysql.connector.connect(
    host="localhost",
    user="ubuntu",
    password="1234567890",
    database="shopping_db"
)

def fetch_from_db():
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
    # img_url = url_for('static', filename='capture.jpg')
    encoded_img_data = base64.b64encode(img_data).decode('utf-8')
    return render_template('display.html', img_data=encoded_img_data, capture_time=capture_time)

# @app.route('/next')
# def next_page():
#     return render_template('next.html')

# @app.route('/main')   
# def main_page():
#     return render_template('main.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    img_data, capture_time = fetch_from_db()
    encoded_img_data = base64.b64encode(img_data).decode('utf-8')
    return {"img_data": encoded_img_data, "capture_time": capture_time}

@app.route('/main')
def main_page():
    return render_template('main.html')


def detect_and_save():
    pin = MotionSensor(22) # 센서의 GPIO 번호

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
                sql = "INSERT INTO images_table (current_time, image) VALUES (%s, %s)"
                val = (current_time, binary_data)
                cursor.execute(sql, val)
                db.commit()

if __name__ == "__main__":
    detect_and_save()   
    app.run(debug=True)

