from flask import Flask

from app.liveCheck.route import liveCheck

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object("config.ProductionConfig")

app.register_blueprint(liveCheck, url_prefix="/live-check")

@app.route("/")
def home():    
    return "Hello World!!"
