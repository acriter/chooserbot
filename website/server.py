from flask import Flask
from flask import request
import chatbot as cb
app = Flask(__name__)

token = 'sohelk7b417cwnzxgt4eyux34r1wd9'

@app.route('/', methods=['GET','POST'])
def test():
    return 'got here'

@app.route('/join', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        bot = cb.TwitchBot('acriterdev', 'vr0zkeoavnuf7kxmunaezpjpz8zcag', token, request.form['username'])
        bot.start()
        #print("a", request.data)
        #print("b", request.form)
        #print("c", request.get_json())
        return request.form['username']
    else:
        return 'get'

if __name__ == "__main__":
    app.run()