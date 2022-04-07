from flask import jsonify
from app.utils.getLocalCsv import getLocalCsv


class ArtistRecommendationInMemoryRepo:
    def __init__(self, connection):
        self.connection = connection
    
    def getRecommendation(self):
        df = getLocalCsv("genre_artist.csv")
        return jsonify({"df":  df.to_dict()})