import pandas as pd
import json
import boto3
from os import environ
from app.artistRecommendation import service

sqs = boto3.client( 
    'sqs',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_KEY'),
    region_name = environ.get('AWS_REGION_US'),
)
sns = boto3.client(
    'sns',
    aws_access_key_id=environ.get('AWS_ACCESS_KEY'),
    aws_secret_access_key=environ.get('AWS_SECRET_KEY'),
    region_name = environ.get('AWS_REGION_US'),
)
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
    
    if not 'Messages' in response:
        print('No Messages found in queue')
        return
        
    res=pd.DataFrame(response.items())[1][0]
    try:
        messages = json.loads(res[0]["Body"])
    except KeyError:
        print('Messages are unknown')
    else:
        body = pd.DataFrame([messages])
        id=pd.DataFrame([json.loads(body["Message"][0])])["id"][0]
        print(id)

        try:
            genRecommendation= service.ArtistRecommendationService["service.ArtistRecommendationService"].getRecommendation({"id": id})
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