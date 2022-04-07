import sqlalchemy as db
from os import environ

class DBConnection:

    def __init__(self):
        pass

    def __generateDbUrl(self,username, password, host, port, name):
        urlString = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{name}'
        return urlString
        
    def generateRemoteConnection(self):
        dbUrl = self.__generateDbUrl(
            environ.get('DB_USER'),
            environ.get('DB_PASS'),
            environ.get('DB_HOST'),
            environ.get('DB_PORT'),
            environ.get('DB_NAME')
        )
        engine = db.create_engine(dbUrl)
        connection = engine.connect()
        return connection

    def generateLocalConnection(self):
        dbUrl = self.__generateDbUrl(
            environ.get('DB_USER_DEV'),
            environ.get('DB_PASS_DEV'),
            environ.get('DB_HOST_DEV'),
            environ.get('DB_PORT_DEV'),
            environ.get('DB_NAME_DEV')
        )
        engine = db.create_engine(dbUrl)
        connection = engine.connect()
        return connection