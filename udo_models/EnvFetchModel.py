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

    sensible_temp = sum.find_all("dd")[0].get_text()[:-1]
    humidity = sum.find_all("dd")[1].get_text()[:-1]
    wind = sum.find_all("dd")[2].get_text()[:-3]
    temp = soup.find('div','temperature_text').text.strip()[5:-1]

    time= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    wbgt2 = float(sensible_temp)
    temp2 = float(temp)
    humid2 = float(humidity)
    wind2 = float(wind)

    
    EnvData = f"{time}\nWBGT :{wbgt2}     |  Temperation : {temp2}\nHumid : {humid2}%  |   Wind Speed :  {wind2}"

    return EnvData