from app.artistRecommendation.functions.venue import   find_venues , find_artist_from_venue
from app.artistRecommendation.functions.genre import find_genre , find_genre_artist
import pandas as pd
import json


def recommendation(body ,event_artist,genre_event,venue_db,genre):
    if 'venue' in body:
        venues_list=find_artist_from_venue(find_venues(body , venue_db), event_artist)
    else:
        venues_list = pd.DataFrame() 

    
    if 'targetAudience' in body:
        if 'genre' in body["targetAudience"]:
            genre_list=find_genre_artist(body, genre , genre_event)
        else:  
            genre_list = pd.DataFrame()      

    combine_functions = pd.concat([venues_list , genre_list])
    list_combine_functions =list(set(combine_functions['artist_id'].tolist()))
    data_of_artist_1 = genre_event[genre_event['artist_id'].isin(list_combine_functions)]
    list_of_genre=list(set(data_of_artist_1['genre_id'].tolist()))
    data_of_artist_2 = genre_event[genre_event['genre_id'].isin(list_of_genre)]
    budget_frame = data_of_artist_2[data_of_artist_2['approx_budget'].between(int(body['artistBudget']['min']) , int(body['artistBudget']['max']))]
    groupby_artist_id = budget_frame.groupby(['artist_id'])['approx_budget'].transform(max) == budget_frame['approx_budget']
    sorted_budget_frame = budget_frame[groupby_artist_id]
    sort_by_popularity = sorted_budget_frame.sort_values(by='popularity',ascending=False , ignore_index = True)
    drop_duplicate_artist = sort_by_popularity.drop_duplicates(subset = 'artist_id',ignore_index = True)
    drop_duplicate_artist['matchPercentage'] = drop_duplicate_artist['popularity']*0.7
    drop_duplicate_artist = drop_duplicate_artist[['artist_id' , 'matchPercentage']]
    recommend_artist = drop_duplicate_artist.head(10)
    return recommend_artist


