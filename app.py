
from flask import Flask
app = Flask(__name__)

@app.route('/live_check')
def hello_world():
    return 'ok'

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)
