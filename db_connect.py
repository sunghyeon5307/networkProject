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
