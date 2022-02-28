# todo scraper

from dataclasses import replace
from datetime import datetime
from bs4 import BeautifulSoup

import requests as r
import pandas as pd
import re
import jsonpickle
import pygsheets

jsonpickle.set_encoder_options('json', indent=4, ensure_ascii=False)
pd.set_option('display.max_columns', 4)

initial_load = False

# Google sheet (database)
gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS')
gsheet = gc.open('Python to Sheets') # get using name
# gsheet = gc.open_by_key('14-b6PRiyY4lb72n3_vqZAvFsm8ybwi4Bgnc89AX5Zz8') # get using google sheet key (preferred)
gworksheet = gsheet.worksheet_by_title('Najave')
# gworksheet = gsheet.worksheet_by_title('test')

class NewsItem:
    def __init__(self, title, url, date):
        self.title = title
        self.date = datetime.strptime(date, '%d.%m.%Y.').date()
        self.url = url
        self.full_text = ""

## Najave
def get_news_item_headers(url_template, pojam, stop_url):
    
    parsed_najave = list()
    print("Reading headers from page ...")

    for page_num in range(1, 10): # increase range to read more data (on initial load)

        # build url
        najave_url = url_template.replace("#pojam", pojam).replace("#pgNum", str(page_num))
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
                url = base_url + url_element["href"],
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

def get_news_item_body(url):
    print("Reading body from: " + url)
    # get html from url
    najava = r.get(url)
    soup = BeautifulSoup(najava.content, "html.parser")
    najava_text = soup.find("div", class_="page_content").text
    return najava_text

def gsheet_get_table(g_worksheet) -> pd.DataFrame:
    print("Reading worksheet: " + g_worksheet.title)
    # get the values of sheet as dataframe
    df = g_worksheet.get_as_df()
    # print(df)
    return df

# START
last_existing_news_item_id = ''
base_url = 'https://vlada.gov.hr'
najave_base_url = base_url + '/vijesti/8?trazi=1&tip=3&tip2=&tema=&profil=&datumod=&datumdo=&pojam=#pojam&page=#pgNum'


existing_spreadsheet_data = gsheet_get_table(gworksheet)

existing_row_count = existing_spreadsheet_data.shape[0]

if existing_row_count == 0:
    print("Initial run!")
    initial_load = True
    # insert header row
    header_row = ["Naslov", "Datum", "URL", "Sadrzaj"]
    gworksheet.update_row(1, header_row)
    # make it bold
    a1_cell = gworksheet.cell('A1')
    a1_cell.set_text_format('bold', True)
    a1_cell.color = (0.8,0.8,0.8,0.1)
    pygsheets.DataRange('B1','D1', worksheet=gworksheet).apply_format(a1_cell)

else:
    print("Found " + str(existing_row_count) + " rows")
    # convert the 'Datum' column to datetime format
    existing_spreadsheet_data['Datum']= pd.to_datetime(existing_spreadsheet_data['Datum'])
    existing_spreadsheet_data = existing_spreadsheet_data.sort_values(by=['Datum'])
    # get url from last saved record
    last_existing_news_item_id = existing_spreadsheet_data['URL'].iloc[-1]
    print("Latest row is:")
    print(existing_spreadsheet_data.iloc[-1:])

# get headers as list
najave_list = get_news_item_headers(najave_base_url, "sjednica", last_existing_news_item_id)

# print(jsonpickle.encode(najave_list, unpicklable=False))


for n in najave_list:
    n.full_text = get_news_item_body(n.url) # scrape content

# convert to DataFrame
new_records_count = len(najave_list)

if new_records_count > 0:
    najave_df = pd.read_json(jsonpickle.encode(najave_list, unpicklable=False))
    najave_df['date']= pd.to_datetime(najave_df['date'])
    najave_df = najave_df.sort_values(by=['date'])
    print("Writing new rows: " + str(new_records_count))
    new_data_range_start = "A" + str(existing_row_count + 2)
    gworksheet.set_dataframe(najave_df, new_data_range_start, copy_head=False)
else:
    print("No new rows found!")

# print(najave_df)

## Zatvorene sjednice

