from flask import Blueprint

liveCheck = Blueprint('liveCheck', __name__)

@liveCheck.route("/")
def test(): 
    return "live check working"