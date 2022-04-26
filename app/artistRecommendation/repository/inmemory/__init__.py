from app.utils.getLocalCsv import getLocalCsv
from app.artistRecommendation.functions import recommendation
import pandas as pd

class ArtistRecommendationInMemoryRepo:
    def __init__(self, connection):
        self.connection = connection
    
    def getRecommendation(self, data):
        venues_csv = getLocalCsv('venues.csv')
        sorted_events = getLocalCsv('sorted_events.csv')
        sorted_genres = getLocalCsv('sorted_genres.csv')
        final_sorted_genres = getLocalCsv('final_sorted_genres.csv')
        sorted_bowie_spotify =  getLocalCsv('sorted_bowie_spotify.csv')
        sorted_bowie_spotify = sorted_bowie_spotify[['artist_id' , 'name' , 'popularity_1']] 
        sorted_events1 = pd.merge(sorted_events,sorted_bowie_spotify , how = 'inner' , on = 'artist_id')
        final_sorted_genres = final_sorted_genres.rename(columns={'name': 'artist_name', 'genre' : 'name'})
        sorted_genres1 = sorted_genres.rename(columns={'Unnamed: 0': 'id', 'genre' : 'name'})
        list_genre = pd.merge(sorted_genres1 , final_sorted_genres , how = 'inner' , on = 'name')
        event_artist_csv = sorted_events1[['id','artist_id' , 'venue_id','popularity_1' ,'approx_budget']]
        event_artist_csv = event_artist_csv.rename(columns={'popularity_1' : 'popularity'})
        genre_events_csv = pd.merge(list_genre , event_artist_csv , how = 'inner' , on = 'artist_id')
        genre_events_csv = genre_events_csv.rename(columns={'id_x': 'genre_id', 'id_y' : 'id' })
        genre_events_csv = genre_events_csv[['artist_id','popularity', 'genre_id', 'id','venue_id','approx_budget']]

        output = recommendation(data , event_artist_csv , genre_events_csv,venues_csv,sorted_genres1)
        final_result =  output.to_json(orient = 'records' , lines=True).replace('\n' , ' ')
        
        return final_result