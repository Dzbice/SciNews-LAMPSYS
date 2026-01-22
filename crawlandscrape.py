import requests
from bs4 import BeautifulSoup
import pandas as pd

years = ["2022","2023","2024","2025","2026"]
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