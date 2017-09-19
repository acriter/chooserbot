from flask import Flask
from flask import request
from flask import render_template

import chatbot as cb
app = Flask(__name__)

token = 'sohelk7b417cwnzxgt4eyux34r1wd9'

@app.route('/', methods=['GET','POST'])
def index():
    return 'got here'

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/join', methods=['POST'])
def join():
    bot = cb.TwitchBot('acriterdev', 'vr0zkeoavnuf7kxmunaezpjpz8zcag', token, request.form['username'])
    bot.start()
    return request.form['username']

if __name__ == "__main__":
    app.run()