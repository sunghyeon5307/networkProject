import cv2
import time
import mysql.connector
from gpiozero import MotionSensor

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
            time = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor = db.cursor()
            sql = "INSERT INTO yourtable (time, image) VALUES (%s, %s)"
            val = (binary_data)
            cursor.execute(sql, val)
            db.commit()