from random import randint
from sqlalchemy import MetaData, Table
import sqlalchemy as db
import pandas as pd

meta = MetaData()

def artistMapper(arts):
    return {
        "artistName": arts['name'],
        "artistId":  arts["id"],
        "artistImage": arts["image"],
        "artistGender": arts["gender"],
        "matchPercentage": arts['matchPercentage'], # actual percentage,
        "matchAttributes": {
            "venues": [
                {
                    "id": '1234',
                    "name": 'Los Angeles',
                    "address": {
                        "pincode": 1234,
                        "country": 'USA',
                        "city": 'Los Angeles',
                        "geoLocation": {
                            "lat": 132.121,
                            "long": 2423.234,
                        },
                    },
                    "venueCapacity":randint(500, 1000),
                    "matchPercentage": randint(1, 99),
                }
            ],
            "age": {
                "ageGroup": '18 - 25',
                "matchPercentage": randint(1, 99),
            },
            "gender": {
                "male": randint(0, 50),
                "female": randint(0, 50),
            },
            "genre": [
                {
                    "genreName": 'Rock',
                    "matchPercentage": randint(1, 99),
                },
                {
                    "genreName": 'Jazz',
                    "matchPercentage": randint(1, 99),
                },
                {
                    "genreName": 'Pop',
                    "matchPercentage": randint(1, 99),
                },
            ],
            "associatedBrands": [
                {
                    "id": '1234',
                    "name": 'Coca Cola',
                    "contact": '919292929292',
                    "website": 'https://www.coca-cola.com/',
                    "logoUrl": 'https://1000logos.net/wp-content/uploads/2016/11/Shape-Coca-Cola-Logo.jpg',
                },
                {
                    "id": '1235',
                    "name": 'Youtube',
                    "contact": '919292929292',
                    "website": 'https://www.youtube.com/',
                    "logoUrl": 'https://w7.pngwing.com/pngs/936/468/png-transparent-youtube-logo-youtube-logo-computer-icons-subscribe-angle-rectangle-airplane.png',
                },
                {
                    "id": '1236',
                    "name": 'Facebook',
                    "contact": '919292929292',
                    "website": 'https://www.facebook.com/',
                    "logoUrl": 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/2021_Facebook_icon.svg/1200px-2021_Facebook_icon.svg.png',
                },
            ],
        },
    }

def generateRecommendation(_artists, connection):
    table = Table('artist', meta, autoload=True, autoload_with=connection)
    qr = db.select([table]).filter(table.c.id.in_((list(_artists['artist_id']))))
    recomm = connection.execute(qr).fetchall()
    artists = [dict(row) for row in recomm]
    artist_data = pd.merge(pd.DataFrame(artists) , _artists.rename(columns={'artist_id':'id'}), on = 'id')
    artist_data_2 = artist_data.sort_values(by='matchPercentage',ascending=False , ignore_index = True).head(10)
    artists_1 = artist_data_2.to_dict('records')
    final_arts = map(artistMapper, artists_1)
    final_artist_data = list(final_arts)
    return final_artist_data
