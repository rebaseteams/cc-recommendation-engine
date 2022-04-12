from app.artistRecommendation.repository.postgres import ArtistRecommendationRepo

class ArtistRecommendationService:
    def __init__(self, recommendationRepo):
        self.recommendationRepo: ArtistRecommendationRepo = recommendationRepo

    def getRecommendation(self, data):
        return self.recommendationRepo.getRecommendation(data)
