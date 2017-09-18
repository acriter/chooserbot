from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/login', methods=['GET','POST'])
def result():
    if request.method == 'POST':
    	return('post was ' + request.form['foo'])
    else:
    	return 'get'

if __name__ == "__main__":
    app.run()