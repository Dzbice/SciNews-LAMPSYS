import requests
from bs4 import BeautifulSoup
import pandas as pd


baseUrl = "https://www.sciencealert.com"
years = ["2022","2023","2024","2025","2026"]
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
for i in years:
    for j in months:
        req = requests.get(baseUrl + "/"+i+"/"+j)
        s = BeautifulSoup(req.text,'html.parser')
        print(s.find("section",class_="col-span-containter"))
        
res = requests.get("https://www.sciencealert.com/suni-williams-retires-after-record-space-career-and-final-ill-fated-mission")
id = 23675

publisher_domains = []

def saveSite(site):
    res = requests.get(site)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = soup.find("section", class_="col-span-container")
    content_links = content.find_all("a")
    for i in content_links:
        for j in publisher_domains:
            if j in i:
                pass

def saveInfo():
    pass