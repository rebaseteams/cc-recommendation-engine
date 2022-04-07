from flask import Blueprint

from app.artistRecommendation.service import ArtistRecommendationService

class ArtistRecommendationRoute:
    def __init__(self, artistRecommendationService):
        self.__artistRecommendationService: ArtistRecommendationService = artistRecommendationService
        self.blueprint = self.__createBlueprint()

    def __createBlueprint(self):
        blueprint = Blueprint('artist-recommendation', __name__)

        @blueprint.route("/")
        def test():
            result = self.__artistRecommendationService.getRecommendation()
            return result

        return blueprint