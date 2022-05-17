from selenium import webdriver
import urllib
from urllib.request import urlopen
import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup
import time

https://www.modoodoc.com/

#충치치료 키워드 검색 -> 치과 목록 URL 수집
hos_url = []
for i in range(1,101):
    url = 'https://www.modoodoc.com/hospitals/?search_query=%EC%B6%A9%EC%B9%98%EC%B9%98%EB%A3%8C&page='+str(i)
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')

    for i in soup.select('div.doctor-total-box.border-bottom'):
        hos_url.append('https://www.modoodoc.com' + i.find('a')['href'])

len(hos_url)

# 각 URL의 병원이름, 평점, 주소 수집
driver = webdriver.Chrome('c:/data/chromedriver.exe')
hos_df = DataFrame()
for i in hos_url:
    driver.get(i)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    name = soup.select_one('h1.my-1.hospital-doctor-name-box.d-flex.align-items-center').text.strip() # 병원이름
    point = soup.select_one('div.col-4.px-3.pt-3.pb-0 > div.mb-2 > b').text.strip() # 평점
    addr = soup.select_one('div[style="  letter-spacing: -0.4px;color: #ffffff;font-size: 14px;"]').text.strip() # 주소
    hos_df = hos_df.append({'name':name,'point':point,'addr':addr},ignore_index=True)
    time.sleep(1)
    print(len(hos_df))
    
len(hos_df)
hos_df
    






