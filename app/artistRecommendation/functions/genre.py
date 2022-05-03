import pandas as pd
pd.set_option('mode.chained_assignment', None)


def find_genre(body,genre ):
    genre_list = []
    for i in range(len(body['target_audience']['genre'])):
        genre_id = genre[genre['name'] == body['target_audience']['genre'][i]['genreId']]
        if len(genre_id)>0:
            genre1 = genre_id['id'].values[0]
            genre_list.append(genre1)
            return genre_list
    
    return genre_list

def find_genre_artist(body , genre , genre_event):
    artist_list = pd.DataFrame()
    list2 = find_genre(body ,genre)
    for i in list2:
        genre2 = genre_event[genre_event['genre_id'] == i]
        artist_list = artist_list.append(genre2)
        
    return artist_list


