def discarded_artist(body):
    list1 = []
    for i in range(len(body['discarded_artists'])):
        list1.append(body['discarded_artists'][i]['artistId'])
        
    return list1  
