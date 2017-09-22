from flask import Flask
from flask import request
from flask import render_template

import chatbot as cb
app = Flask(__name__)

token = 'sohelk7b417cwnzxgt4eyux34r1wd9'
bot = None

@app.route('/', methods=['GET','POST'])
def index():
    return 'got here'

@app.route('/dashboard/', methods=['GET'])
@app.route('/dashboard/<name>', methods=['GET'])
def dashboard(name=None):
    return render_template('dashboard.html', name=name)

@app.route('/join', methods=['POST'])
def join():
    if not bot is None:
        bot = cb.TwitchBot('acriterdev', 'vr0zkeoavnuf7kxmunaezpjpz8zcag', token, request.form['username'])
        bot.start()
    return request.form['username']

@app.route('/setquestion', methods=['POST'])
def setQuestion():
    if not bot is None:
        bot.set_question(None, request.form['question'])
    return request.form['question']

if __name__ == "__main__":
    app.run()