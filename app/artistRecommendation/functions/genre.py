import pandas as pd

def genre(i,genre_artist):
    list_artist = genre_artist[genre_artist['genre'] == i]
    return list_artist 


def from_genre(genre1,genre_name1,events,genre_artist):
    list_of_genre=genre(genre1,genre_artist)
    list1=list_of_genre['artist_id'].tolist()
    find_artist=events[events['artist_id'].isin(list1)]
    recommend_1 = pd.merge(find_artist, genre_name1, how='inner', on=['artist_id'])
    recommend_1['rating'] = recommend_1['popularity_1']*0.5
    recommend_1 = recommend_1[[ 'artist_id','name_x'  , 'popularity_1', 'genres1','approx_budget' , 'rating']]
    return recommend_1
