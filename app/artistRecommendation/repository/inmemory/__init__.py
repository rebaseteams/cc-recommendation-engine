from app.utils.getLocalCsv import getLocalCsv
from app.artistRecommendation.functions import recommendation

class ArtistRecommendationInMemoryRepo:
    def __init__(self, connection):
        self.connection = connection
    
    def getRecommendation(self, data):
        # df = getLocalCsv("genre_artist.csv")
        genre_artist = getLocalCsv('final_sorted_genres.csv')
        genre_artist = genre_artist[['artist_id', 'name', 'genre']]
        events = getLocalCsv('sorted_events.csv')
        genre_name = getLocalCsv('sorted_bowie_spotify.csv')
        genre_name1 = genre_name[['artist_id' , 'name' , 'popularity_1' ,'genres1' , 'male' , 'female']]
        venues = getLocalCsv('venues.csv')
        genres = getLocalCsv('genre_artist.csv')
        genre_list = getLocalCsv('sorted_genres.csv')
        genre_list['genre'] = genre_list['genre'].str.replace("'", '')
        output = recommendation(data, genre_name1,genres,events,venues,genre_artist)
        final_result =  output.to_json(orient = 'records' , lines=True).replace('\n' , ' ')
        
        return final_result