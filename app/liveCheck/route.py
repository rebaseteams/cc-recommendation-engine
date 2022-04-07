from flask import Blueprint
from os import environ

liveCheck = Blueprint('liveCheck', __name__)

@liveCheck.route("/")
def test(): 
    return {
        "status": "working",
        "environment": environ.get('FLASK_ENV'),
    }
