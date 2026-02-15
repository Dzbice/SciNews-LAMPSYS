from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import csv
import requests



def loadPublisherDomans(path):
    df = pd.read_csv(path)
    return set(df["Publisher Domain"].tolist())

def saveSite(site):
    res = requests.get(site)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = soup.find("section", class_="col-span-container")
    if content is None:
        return False
    content_links = content.find_all("a")
    publisherLinksFound = []        
    for i in content_links:
        href = i.get("href")
        if not href:
            continue
        if checkBlacklist(href):
            if checkPublisherlist(href):
                publisherLinksFound.append(href)
    if publisherLinksFound:
        print(site)
        return True
    else: return False
        
def checkBlacklist(domain):
    for i in blacklist:
        if i in domain:
            return False
    return True
def checkPublisherlist(domain):
    for i in publisher_domains:
        if i in domain:
            return True
    return False


publisher_domains = loadPublisherDomans("dataCollection/Publishers_Domain_List.csv")
blacklist = set(["sciencealert.com","theconversation.com","wikipedia.org","canva.com","eurekalert.org","universetoday.com","wikimedia.org","businessinsider.com","unsplash.com","esa.int","creativecommons.org",
             "nhs.uk","tandfonline.com","mayoclinic.org","theguardian.com","instagram.com","jamanetwork.com"])

df14 = pd.read_csv("dataCollection/data/14-18.csv")
df14 = df14[df14["url"].apply(saveSite)]


df19 = pd.read_csv("dataCollection/data/19-22.csv")
df19["date"] = pd.to_datetime(df19["date"])
df19 = df19[df19["date"].dt.year != 2022]
df19 = df19[df19["url"].apply(saveSite)]


combined_14_21 = pd.concat([df14,df19],ignore_index=True)
now_22 = pd.read_csv("dataCollection/data/22-0126.csv")
df = pd.concat([combined_14_21,now_22],ignore_index=True)
df["id"] = range(1, len(df) + 1)
df.to_csv("dataCollection/data/combined.csv", index=False, quoting=csv.QUOTE_ALL)
print("df14:", len(df14))
print("df19:", len(df19))
print("combined_14_21:", len(combined_14_21))
print("now_22:", len(now_22))
