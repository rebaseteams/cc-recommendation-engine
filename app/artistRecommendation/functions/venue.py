import pandas as pd
pd.set_option('mode.chained_assignment', None)

def venue(v,venues):
    list1 = []
    for i in range(len(v)):
        final_result1 = v[i]['name']
        find_name = venues[venues['name'] == final_result1]
        find_id = find_name['id'].values[0]
        list1.append(find_id)

    return list1  

def event(e,events):
    data = pd.DataFrame()
    for i in range(len(e)):
        eve = events[events['venue_id'] == e[i]]
        data = data.append(eve)

    return data


def recommend_venue(df1,genre_name1,genres,events,venues):
    col_names = ['name_x' ,'popularity_1' , 'genres1','female','male','approx_budget','rating']
    data_frame = pd.DataFrame(columns = col_names)
    find_events =event(venue(df1,venues),events)
    if len(find_events.columns) > 0:
        merge_1 = pd.merge(find_events, genre_name1, how='inner', on=['artist_id'])
        merge_2 = merge_1[['artist_id' , 'popularity_1' ,'female','male', 'approx_budget' ]]
        merge_3=merge_2.sort_values(by='popularity_1',ascending=False)
        merge_3 = merge_3.drop_duplicates(subset = 'artist_id', ignore_index = True)
        for i in range(len(merge_3)):
            merge_4=merge_3['artist_id'].values[i]
            result_1=genres[genres['artist_id'] == merge_4]['genre'].values[0]
            result_2=genres[genres['genre'] == result_1]
            result_3 = pd.merge(result_2, genre_name1 ,how='inner', on = ['artist_id'])
            result_4 = pd.merge(result_3 , events , how = 'inner' , on = ['artist_id'])
            product_1=result_4.sort_values(by='popularity_1',ascending=False)
            product_2 = product_1[['name_x' , 'popularity_1' , 'genres1' ,'female','male' ,'approx_budget']]
            product_2['rating'] = product_2['popularity_1']*0.4
            data_frame = data_frame.append(product_2)
    else:
        return data_frame
    
    return data_frame



