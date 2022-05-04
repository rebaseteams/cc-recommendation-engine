from flask import Blueprint, request

from app.artistRecommendation.service import ArtistRecommendationService

class ArtistRecommendationRoute:
    def __init__(self, artistRecommendationService):
        self.__artistRecommendationService: ArtistRecommendationService = artistRecommendationService
        self.blueprint = self.__createBlueprint()

    def __createBlueprint(self):
        blueprint = Blueprint('artist-recommendation', __name__)

        @blueprint.route("", methods=["POST"])
        def predict():
            try:
                data = request.get_json()
                result = self.__artistRecommendationService.getRecommendation(data)
                return result
            except:
                return {"success": False}

        return blueprint