import pandas as pd
from sqlalchemy import MetaData, Table
import sqlalchemy as db

meta = MetaData()

def loadTableDf(tableName, connection):
    table = Table(tableName, meta, autoload=True, autoload_with=connection)
    ResultSet = connection.execute(db.select([table])).fetchall()
    df = pd.DataFrame(ResultSet)
    df.columns = ResultSet[0].keys()
    return df
