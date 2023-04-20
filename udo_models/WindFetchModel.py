import requests
from bs4 import BeautifulSoup
import lxml
import datetime
import json

def fetch_weather_info():
    res = requests.get("https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8")
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")     

    sum = soup.find("dl", attrs={"class":"summary_list"})

    wind = sum.find_all("dd")[2].get_text()[:-3]


    EnvData = {
        'datetime' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'wind' : float(wind)
        }
    
    with open("env_data.log","a") as f:
        json.dump(EnvData,f)
        f.write(",\n")

    return EnvData