from flask import Flask, render_template, redirect, url_for
import mysql.connector
import cv2
import time
from gpiozero import MotionSensor
import base64

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
    return result[1], result[0]   # 1: 이미지 데이터, 0: 시간

app = Flask(__name__)

# OpenCV를 사용하여 웹 카메라 영상을 표시하는 함수
def show_camera():
    # 카메라에 접근하기 위해 VideoCapture 객체 생성
    cap = cv2.VideoCapture(0)

    # 카메라 캡처 설정 (해상도, 프레임 속도 등)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # 영상을 연속적으로 표시하기 위해 반복문 사용
    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        # 프레임 읽기에 실패한 경우 반복문 종료
        if not ret:
            break

        # 프레임 표시
        cv2.imshow('Camera', frame)

        # 'q' 키를 누르면 반복문 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 사용이 끝난 자원 해제
    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/move', methods=['POST'])
def move():
    return redirect(url_for('main'))

@app.route('/display')
def display():
    # 이미지, 시간 정보 db에서 검색
    img_data, capture_time = fetch_from_db()
    encoded_img_data = base64.b64encode(img_data).decode('utf-8')
    return render_template('main.html', db_data=[{'order': 1, 'time': capture_time, 'img_data': encoded_img_data}])


@app.route('/get_data', methods=['GET'])
def get_data():
    img_data, capture_time = fetch_from_db()
    encoded_img_data = base64.b64encode(img_data).decode('utf-8')
    return {"img_data": encoded_img_data, "capture_time": capture_time}

@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/detect_and_save')
def web_detect_and_save():
    detect_and_save()
    return redirect(url_for('main'))

def detect_and_save():
    def capture_frame():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 440)

        ret, frame = cap.read()  # 캡처
        cap.release()
        cv2.destroyAllWindows()

        return ret, frame
    
    pin = MotionSensor(7)  # 센서의 GPIO 번호

    if pin.motion_detected:
        print("!!!!!!!")
        ret, frame = capture_frame()

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
    # 웹 카메라 영상을 표시하는 스레드 시작
    import threading
    camera_thread = threading.Thread(target=show_camera)
    camera_thread.start()

    app.run(host='0.0.0.0')
