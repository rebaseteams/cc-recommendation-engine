from flask import Flask
from app.serverDevelopment import DevelopmentServer
from app.liveCheck.route import liveCheck
from app.artistRecommendation.route import ArtistRecommendationRoute
from app.serverProduction import ProductionServer 
from os import environ
from app.utils.retrieveMessages import retrieveMessages
from apscheduler.schedulers.background import BackgroundScheduler

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

if (environ.get('FLASK_ENV') == "production"):
    server = ProductionServer()
    app.config.from_object("config.ProductionConfig")
else: 
    server = DevelopmentServer()
    app.config.from_object("config.DevelopmentConfig")

services = server.config["services"]

app.register_blueprint(liveCheck, url_prefix="/reco-engine/live_check")
app.register_blueprint(
    ArtistRecommendationRoute(services["artistRecommendationService"]).blueprint, 
    url_prefix="/reco-engine/artist-recommendation")    

scheduler = BackgroundScheduler()
scheduler.add_job(func=retrieveMessages, args=[services["artistRecommendationService"]], trigger="interval", seconds=10)
scheduler.start()

@app.route("/")
def home():  
    return "Hello World!!"
