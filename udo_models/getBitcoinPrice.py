import requests
from bs4 import BeautifulSoup
import lxml
import datetime
import json
import pandas as pd

def get_bf():


    url = "https://www.google.com/search?q=%EB%B9%84%ED%8A%B8%EC%BD%94%EC%9D%B8+%EC%8B%9C%EC%84%B8"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.find("div", class_="BNeawe iBp4i AP7Wnd").get_text()


    time= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    BF=f"{time}\nCurrent Bitcoin price : {price[:-6]} won"

    return BF