from app.artistRecommendation.functions.venue import   venue , recommend_venue_1
from app.artistRecommendation.functions.genre import genre , from_genre
import pandas as pd
import json


def recommendation(body , genre_name1,genres,events,venues,genre_artist):
    df=json.dumps(body)
    train = pd.read_json(df , orient = 'index')
    df1 = train.T
    print(df1)
    df2 = df1.explode('genre' , ignore_index= True)
    df2['approx budget'] = df2['approx budget'].astype(int)
    recommend_from_venue=recommend_venue_1(df1['venue'][0],genre_name1,genres,events,venues)
    column = [ 'artist_id','name_x'  , 'popularity_1', 'genres1','approx_budget' , 'rating']
    genre_list1 = pd.DataFrame(columns = column)
    list1 = df2['genre'].to_list()
    for i in list1:
        find_artists = from_genre(i,genre_name1,events,genre_artist)
        genre_list1=genre_list1.append(find_artists)

    frames = [genre_list1,recommend_from_venue]
    result = pd.concat(frames)
    result['approx_budget'] = result['approx_budget'].astype(int)
    frame_1 = result[result['approx_budget'].between(int(float(10000)) , int(df2['approx budget'][0]))]
    idx = frame_1.groupby(['name_x'])['approx_budget'].transform(max) == frame_1['approx_budget']
    max1=frame_1[idx]
    max2 = max1.sort_values(by='rating',ascending=False , ignore_index = True)
    max3 = max2[['name_x' ,'popularity_1' ,'genres1']]
    max3 = max3.drop_duplicates(subset = 'name_x',ignore_index = True)
    return max3.head(6)  
