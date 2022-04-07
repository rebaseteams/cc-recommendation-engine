from app.artistRecommendation.repository.postgres import ArtistRecommendationRepo

class ArtistRecommendationService:
    def __init__(self, recommendationRepo):
        self.recommendationRepo: ArtistRecommendationRepo = recommendationRepo

    def getRecommendation(self):
        return self.recommendationRepo.getRecommendation()
