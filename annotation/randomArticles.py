from random import randint
import pandas as pd
from json import dumps
import ast #to cleanely retrieve links

def loadPublisherDomans(path):
    df = pd.read_csv(path)
    return set(df["Publisher Domain"].tolist())
def isPublisher(url):
    for i in publisherDomains:
        if i in url:
            return True
    return False


publisherDomains = loadPublisherDomans("dataCollection/Publishers_Domain_List.csv")
db = pd.read_csv("dataCollection/data/combined.csv")


toAnnotate = {}

for i in range(10):
    rand= randint(0,len(db)-1)
    website = db.loc[rand,"url"]
    links = set(ast.literal_eval(db.loc[rand,"all_links"]))

    publisherLinks = []
    for j in links:
        #print(j)
        if(isPublisher(j)):
            publisherLinks.append(j)
    #print(f"Article: {db.loc[rand,"url"]}, Links: {db.loc[rand,"all_links"],}")
    toAnnotate[website] = publisherLinks
    
with open("annotation/randomArticles.json",'w') as fp:
    fp.write(dumps(toAnnotate))