from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/move', methods=['POST'])
def move():
    return redirect(url_for('display'))

@app.route('/display')
def display():
    # 여기서 DB에서 이미지와 시간 정보를 가져옵니다.
    img_data, capture_time = fetch_from_db()
    return render_template('display.html', img_data=img_data, capture_time=capture_time)

if __name__ == "__main__":
    app.run(debug=True)
