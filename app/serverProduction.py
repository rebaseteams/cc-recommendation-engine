from app.artistRecommendation.service import ArtistRecommendationService
from app.artistRecommendation.repository.postgres import ArtistRecommendationRepo
from app.utils.createDbConnection import DBConnection

class ProductionServer:

    def __init__(self):
        self.connection = DBConnection().generateRemoteConnection()
        self.config = {
            "services": {
                "artistRecommendationService": ArtistRecommendationService(
                    ArtistRecommendationRepo(self.connection)
                ),
            }
        }
