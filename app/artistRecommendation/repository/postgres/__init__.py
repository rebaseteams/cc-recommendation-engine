from flask import jsonify

from app.utils.loadTableDf import loadTableDf

class ArtistRecommendationRepo:
    def __init__(self, connection):
        self.connection = connection
    
    def getRecommendation(self, data):
        brandDf = loadTableDf('brand', self.connection)
        return jsonify({"df":  brandDf.to_dict()})
        