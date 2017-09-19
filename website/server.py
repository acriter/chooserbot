from flask import Flask
from flask import request
import chatbot.py
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def test():
    return 'got here'

@app.route('/join', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        #print("a", request.data)
        #print("b", request.form)
        #print("c", request.get_json())
        return request.form['username']
    else:
        return 'get'

if __name__ == "__main__":
    app.run()