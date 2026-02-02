import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import csv


def loadPublisherDomans(path):
    df = pd.read_csv(path)
    return set(df["Publisher Domain"].tolist())

def crawlto(i, j=""):
    req = requests.get(baseUrl + "/"+i+"/"+j)
    s = BeautifulSoup(req.text,'html.parser')
    cont = s.find("div", class_="container-posts")
    if cont:
        link = cont.find_all("a")
        for k in link:
            saveSite(k['href'])

def crawl():
    for i in years:
        if i =="2026":
            crawlto("2026","01")
            break
        for j in months:
            crawlto(i,j)
            

def saveSite(site):
    global totalSites, totalLinks, publishedLinks, id
    totalSites = totalSites+1
    res = requests.get(site)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = soup.find("section", class_="col-span-container")
    content_links = content.find_all("a")
    publisherLinksFound = []        
    for i in content_links:
        totalLinks = totalLinks+1
        href = i.get("href")
        if not href:
            continue
        if checkBlacklist(href):
            if checkPublisherlist(href):
                publisherLinksFound.append(href)
    if publisherLinksFound:
        publishedLinks = publishedLinks + len(publisherLinksFound)
        saveInfo(content, site, publisherLinksFound)
        id = id +1
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

def saveInfo(content, site, links):
    print(site)

    TITLE = safe(lambda: content.find_all("h1")[0].text)
    AUTHORS = safe(lambda: content.find("div", class_="author-details").find_all("span")[1].text)
    CATEGORY = safe(lambda: content.find_all(
        "a",
        class_="article-cat text-body-sm sm:text-body-md uppercase font-source-sans font-semibold text-legibility inline-block mr-3"
    )[0].text)
    DATE = safe(lambda: content.find(
        "span",
        class_="article-date text-body-xs sm:text-body-sm text-gray-500 block mr-3"
    ).text)

    PLAINTEXT = safe(lambda: content.get_text())
    HTML = safe(lambda: str(content))

    df.loc[len(df)] = {
        "id": id,
        "title": TITLE,
        "authors": AUTHORS,
        "category": CATEGORY,
        "date": DATE,
        "url": site,
        "plaintext": PLAINTEXT,
        "html": HTML,
        "all_links": links
    }
    
def safe(getter, default="not found"):
    try:
        value = getter()
        if value:
            return value.strip()
    except Exception:
        pass
    return default


df = pd.DataFrame(columns=[
    "id",
    "title",
    "authors",
    "category",
    "date",
    "url",
    "plaintext",
    "html",
    "all_links"
])
publisher_domains = loadPublisherDomans("dataCollection/Publishers_Domain_List.csv")
baseUrl = "https://www.sciencealert.com"
#years = ["2022", "2023", "2024", "2025", "2026"], testing smaller range
years = ["2025"]
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
blacklist = set(["sciencealert.com","theconversation.com","wikipedia.org","canva.com","eurekalert.org","universetoday.com","wikimedia.org","businessinsider.com","unsplash.com","esa.int","creativecommons.org",
             "nhs.uk","tandfonline.com","mayoclinic.org","theguardian.com","instagram.com","jamanetwork.com"])
id = 23675
totalSites = 0
totalLinks = 0
publishedLinks = 0


if __name__ == "__main__":
    crawl()
    df.to_csv("14-0126.csv", index=False, quoting=csv.QUOTE_ALL)
    with open("stats.txt","w") as fp:
        fp.write(f"totalSites: {totalSites}\n totalLinks: {totalLinks}\n publishedLinks: {publishedLinks}")