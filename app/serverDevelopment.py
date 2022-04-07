from app.artistRecommendation.service import ArtistRecommendationService
from app.artistRecommendation.repository.inmemory import ArtistRecommendationInMemoryRepo
from app.utils.createDbConnection import DBConnection

class DevelopmentServer:

    def __init__(self):
        # self.connection = DBConnection().generateLocalConnection()
        self.connection = "local-db-connection"
        self.config = {
            "services": {
                "artistRecommendationService": ArtistRecommendationService(
                    ArtistRecommendationInMemoryRepo(self.connection)
                ),
            }
        }
