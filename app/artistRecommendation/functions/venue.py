import pandas as pd
pd.set_option('mode.chained_assignment', None)

def find_venues(v,venue):
    list1 = []
    for i in range(len(v['venue'])):
        find_name = venue[venue['name'] == v['venue'][i]['name']]
        find_id = find_name['id'].values[0]
        list1.append(find_id)

    return list1  


def find_artist_from_venue(v ,event_artist):
    data = pd.DataFrame()
    for i in v:
        list_artist = event_artist[event_artist['venue_id'] == i]
        data = data.append(list_artist)
        
    return data




