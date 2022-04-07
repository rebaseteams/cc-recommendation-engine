import pandas as pd
import os

cwd = os.getcwd()

def getLocalCsv(fileName):
    path = os.path.join(cwd, "app/mockData", fileName)
    df = pd.read_csv(path)
    return df

