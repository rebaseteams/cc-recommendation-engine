import pandas as pd
import json
import threading
from flask import Flask
from app.serverDevelopment import DevelopmentServer
from app.liveCheck.route import liveCheck
from app.artistRecommendation.route import ArtistRecommendationRoute
from app.serverProduction import ProductionServer 
from os import environ
import boto3

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
sqs = boto3.client( 
    'sqs',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_KEY'),
    region_name = environ.get('AWS_REGION'),
)
sns = boto3.client(
    'sns',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_KEY'),
    region_name = environ.get('AWS_REGION'),
)

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

queue_url = environ.get('recommend-queue-url')

# Long poll for message on provided SQS queue
def retrieveMessages():
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ]
    )
    if 'Messages' in response:
        res=pd.DataFrame(response.items())[1][0]
        try:
            messages = json.loads(res[0]["Body"])
        except KeyError:
            print('Messages are unknown')
        else:
            body = pd.DataFrame([messages])
            id=pd.DataFrame([json.loads(body["Message"][0])])["id"][0]

        try:
            genRecommendation= services["artistRecommendationService"].getRecommendation({"id": id})
            if genRecommendation: 
                message = { "id": id, "status": genRecommendation['status'], "message": genRecommendation['message']}
        except:
            message = { "id": id, "status": False, "message": "Something went wrong"}
        finally:
            arn = environ.get('TopicARN_SNS_Recommendation_Processed')
            sns.publish(
                TopicArn=arn,
                Message=json.dumps({'default': json.dumps(message)}),
                MessageStructure='json'
            )  
            receiptHandle=response['Messages'][0]['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receiptHandle,
            )
    else:
        return print('No Messages available in queue')
            
def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

setInterval(retrieveMessages, 30.0)       

@app.route("/")
def home():    
    return "Hello World!!"
