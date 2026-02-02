import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import csv
import tldextract

baseUrl = "https://www.sciencealert.com"
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
sites = {}

def crawlto(j=""):
    req = requests.get(baseUrl + "/2025"+"/"+j)
    s = BeautifulSoup(req.text,'html.parser')
    cont = s.find("div", class_="container-posts")
    if cont:
        link = cont.find_all("a")
        for k in link:
            sitelist(k['href'])
            
            
def crawl():
    for j in months:
        crawlto(j)
        
        
        
def sitelist(site):
    res = requests.get(site)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = soup.find("section", class_="col-span-container")
    content_links = content.find_all("a")
    for i in content_links:
        href = i.get("href")
        if not href:
            continue
        site = tldextract.extract(href)
        domain = site.domain + "." +site.suffix
        if domain not in sites:
            sites[domain] = 1
        else:
            sites[domain] = sites[domain]+1




crawl()
sorted_dict = dict(sorted(sites.items(), key=lambda item: item[1], reverse=True))
fout = "dataCollection/siteList.txt"
fo = open(fout, "w")
for k, v in sorted_dict.items():
    fo.write(str(k) + ','+ str(v) + '\n')
fo.close()