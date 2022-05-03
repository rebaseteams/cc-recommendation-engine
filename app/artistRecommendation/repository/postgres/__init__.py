from flask import jsonify
import pandas as pd
from sqlalchemy import MetaData, Table
from app.artistRecommendation.functions import recommendation
from app.utils.loadTableDf import loadTableDf
import sqlalchemy as db


meta = MetaData()

class ArtistRecommendationRepo:
    def __init__(self, connection):
        self.connection = connection
    
    def getRecommendation(self, data):
        table = Table('artist_recommendation', meta, autoload=True, autoload_with=self.connection)
        qr = db.select([table]).filter_by(id = data["id"])
        recomm = self.connection.execute(qr).first()._asdict()
        venue_db= loadTableDf('venue', self.connection)
        event =loadTableDf('events' , self.connection)
        genre =loadTableDf('genre' , self.connection)
        performers1 =loadTableDf('event-performers' , self.connection)
        artist_genre =loadTableDf('artist-genre' , self.connection)
        artist_popularity = loadTableDf('artist-popularity' ,self.connection)
        venue = venue_db.rename(columns={'id': 'venue_id'})
        event = event.rename(columns = {'id':'event_id'})
        performers1 = performers1.rename(columns = {'performer_id':'artist_id'})
        performers = pd.merge(performers1 , artist_popularity , how = 'inner' , on = 'artist_id')
        event_artist = pd.merge(event , performers , how = 'inner' , on = 'event_id')
        event_artist = event_artist[['event_id' ,'venue_id','artist_id','popularity','approx_budget']]
        genre_artist = pd.merge(artist_genre ,performers , how = 'inner' , on = 'artist_id' )
        genre_artist = genre_artist[['artist_id', 'genre_id','event_id','popularity']]
        genre_event = pd.merge(genre_artist , event , how = 'inner' , on = 'event_id')
        genre_event = genre_event[['artist_id','popularity', 'genre_id', 'event_id','approx_budget']]
        output = recommendation(recomm ,event_artist , genre_event,venue_db,genre)
        final_result =  output.to_json(orient = 'records' , lines=True).replace('\n' , ' ')
        
        return final_result
        