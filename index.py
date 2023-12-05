from flask import Flask, render_template, redirect, url_for
import mysql.connector
import cv2
import time
from gpiozero import MotionSensor
import base64
from db_utils import fetch_from_db
from capture_utils import detect_and_save

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/move', methods=['POST'])
def move():
    return redirect(url_for('display'))

@app.route('/display')
def display():
    img_data, capture_time = fetch_from_db()
    encoded_img_data = base64.b64encode(img_data).decode('utf-8')
    return render_template('display.html', img_data=encoded_img_data, capture_time=capture_time)

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
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0' )
