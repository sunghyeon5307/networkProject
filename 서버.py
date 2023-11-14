from flask import Flask, render_template, send_from_directory
import os

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory(os.path.join("..","path","to","images"), filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')