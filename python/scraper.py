# todo scraper

from dataclasses import replace
from datetime import datetime
from bs4 import BeautifulSoup

import requests as r
import pandas as pd
import re
# import json
import jsonpickle

jsonpickle.set_encoder_options('json', indent=4, ensure_ascii=False)

class NewsItem:
    def __init__(self, title, url, date):
        self.title = title
        self.date = datetime.strptime(date, '%d.%m.%Y.').date()
        self.url = url
        self.full_text = ""

## Najave
def get_news_item_headers(base_url, pojam, stop_url):
    
    parsed_najave = list()
    print("Reading from page ...")

    for page_num in range(1, 3):

        # build url
        najave_url = base_url.replace("#pojam", pojam).replace("#pgNum", str(page_num))
        print(najave_url)

        # get html from url
        najave = r.get(najave_url)
        soup = BeautifulSoup(najave.content, "html.parser")

        # extract news items
        news_items = soup.find_all("div", class_="news_item")

        stop_outer_loop = False

        # loop news items
        for ni in news_items:
            title_element = ni.find("span", class_="h3")
            url_element = ni.find("a", href=True)
            date_element = ni.find("span", class_="date")

            item = NewsItem(
                title = title_element.text,
                url = url_element["href"],
                date = date_element.text.split(' | ')[0]
            )

            # if stop condition reached
            if item.url == stop_url:
                stop_outer_loop = True
                break

            # append to list only if Title contains 'sjednica vlade'
            if "sjednica vlade" in item.title.lower():
                parsed_najave.append(item)
        
        if stop_outer_loop == True:
            break

    return parsed_najave

def get_najava_body(url):
    # get html from url
    najava_url = base_url + url
    najava = r.get(najava_url)
    soup = BeautifulSoup(najava.content, "html.parser")
    najava_text = soup.find("div", class_="page_content").text
    return najava_text

# START
base_url = 'https://vlada.gov.hr'
najave_base_url = base_url + '/vijesti/8?trazi=1&tip=3&tip2=&tema=&profil=&datumod=&datumdo=&pojam=#pojam&page=#pgNum'
# get headers as list
najave_list = get_news_item_headers(najave_base_url, "sjednica", "/vijesti/82-sjednica-vlade/33251")

for n in najave_list:
    n.full_text = get_najava_body(n.url)

print(jsonpickle.encode(najave_list, unpicklable=False))

# convert to DataFrame
# najave_df = pd.read_json(jsonpickle.encode(najave_list, unpicklable=False))

# print(najave_df)

## Zatvorene sjednice

