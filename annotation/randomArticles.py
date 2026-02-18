from random import randint
import pandas as pd

db = pd.read_csv("dataCollection/data/combined.csv")
for i in range(10):
    print(db.loc[randint(0,len(db)),"url"])