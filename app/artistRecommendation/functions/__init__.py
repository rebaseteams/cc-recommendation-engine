from app.artistRecommendation.functions.venue import   find_venues , find_artist_from_venue
from app.artistRecommendation.functions.genre import find_genre , find_genre_artist
import pandas as pd
import json


def recommendation(abc ,event_artist,genre_event,venue_db,genre):
    venues_list=find_artist_from_venue(find_venues(abc , venue_db), event_artist)
    genre_list=find_genre_artist(abc, genre , genre_event)
    ab = pd.concat([venues_list , genre_list])
    list1=list(set(ab['artist_id'].tolist()))
    data1 = genre_event[genre_event['artist_id'].isin(list1)]
    list2=list(set(data1['genre_id'].tolist()))
    data2 = genre_event[genre_event['genre_id'].isin(list2)]
    frame_1 = data2[data2['approx_budget'].between(int(abc['artistBudget']['min']) , int(abc['artistBudget']['max']))]
    idx = frame_1.groupby(['artist_id'])['approx_budget'].transform(max) == frame_1['approx_budget']
    max1=frame_1[idx]
    max2 = max1.sort_values(by='popularity',ascending=False , ignore_index = True)
    max3 = max2.drop_duplicates(subset = 'artist_id',ignore_index = True)
    return max3


