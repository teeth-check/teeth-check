# 사용 패키지
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver #동적 웹페이지 패키지
from selenium.webdriver.common.keys import Keys # 동적 웹페이지 스크롤 패키지
import time # 동적 웹페이지 시간 지연 설정 패키지
from selenium.webdriver.common.by import By #동적 웹페이지 By 클래스
import urllib.request as req # 웹페이지 사진 다운로드
from pandas import DataFrame, Series
import os #폴더 생성 패키지

# <충치 사진 수집-구글>
driver = webdriver.Chrome('c:/data_bigdata/chromedriver.exe')
url1='https://www.google.com/search?q='
url2='&source=lnms&tbm=isch&sa=X'
lst = ['충치','충치 사진','유아 충치','dental caries'] #충치 한글, 영문으로 검색

for j in lst:
    pic_link=[]
    driver.get(url1+j+url2) # 충치 이미지 주소로 이동
    # 스크롤 페이지 최하단까지 내리기
    for i in range(10): # 스크롤 후 결과 더보기가 뜨면 클릭
        driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
        time.sleep(1)
        try: 
            driver.find_element(By.CLASS_NAME,'r0zKGf').click()   
            time.sleep(1)
        except:
            try:
                driver.find_element(By.CLASS_NAME,'YstHxe').click()
                time.sleep(1)
            except:
                pass
    html = driver.page_source # 현재 페이지 소스 변수 저장
    soup = BeautifulSoup(html, 'html.parser') # 페이지 소스 beautiful soup 변수 저장
    for i in soup.select_one('div.OcgH4b').select('img'):
        try: #사진 저장(2가지attrs에 저장되어 try문 사용)
            pic_link.append(i.attrs['src'])
        except:
            try:
                pic_link.append(i.attrs['data-src'])
            except:
                pass
   
    # 사진 다운로드
    for i in range(len(pic_link)):
        path = 'c:/data_bigdata/dental_caries/pic/dental_caries/'
        if not os.path.isdir(path): #폴더가 존재하지 않는다면 폴더 생성
            os.makedirs(path)
        try:
            req.urlretrieve(pic_link[i],path+f'충치_{i}.jpg')
        except:
            pass

driver.close()

#충치 사진 정제 후 파일 이름 수정
path = "c:/data_bigdata/dental_caries/pic/dental_caries/"
files = os.listdir(path)
for index, file in enumerate(files):
    os.rename(path+file, path +'detal_caries_' + str(index)+ '.jpg')






















