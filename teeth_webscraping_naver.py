
##########################################################################################
# 논의 사항
"""

"""
# 사용 패키지
import sys #무시하세요
sys.path.append("D:\\anaconda3\\lib\\site-packages") #무시하세요
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver #동적 웹페이지 패키지
from selenium.webdriver.common.keys import Keys # 동적 웹페이지 스크롤 패키지
import time # 동적 웹페이지 시간 지연 설정 패키지
from selenium.webdriver.common.by import By #동적 웹페이지 By 클래스
import urllib.request as req # 웹페이지 사진 다운로드
import re # 정규표현식 패키지

##################################################################################
# <네이버 사진 수집>
url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=image&query=&oquery='
#chrome open
driver = webdriver.Chrome("C:/Users/selec/chromedriver.exe")
driver.get(url)
time.sleep(1)
# 충치 검색
    # '충치' 키워드 검색
    element = driver.find_element(By.ID,'nx_query') #검색창 변수 지정
    element.send_keys('충치') #'충치' 검색창에 입력
    time.sleep(1)
    element.submit() #검색 클릭
    # 스크롤 페이지 최하단까지 내리기
    for i in range(6):
        driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
        time.sleep(1)
    html = driver.page_source # 현재 페이지 소스 변수 저장
    soup = BeautifulSoup(html, 'html.parser') # 페이지 소스 beautiful soup 변수 저장
    # 사진 링크들 변수에 저장
    cav_link = []
    for i in soup.select('img._image'):
        cav_link.append(i.attrs['src'])
    driver.back() # 뒤로 가기로 검색창 초기화

# 정상 치아
    # '이' 키워드 검색
    element = driver.find_element(By.ID,'nx_query') #검색창 변수 지정
    element.send_keys('이') #'이' 검색창에 입력
    time.sleep(1)
    element.submit() #검색 클릭
    # 스크롤 페이지 최하단까지 내리기
    for i in range(6):
        driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
        time.sleep(1)
    html = driver.page_source # 현재 페이지 소스 변수 저장
    soup = BeautifulSoup(html, 'html.parser') # 페이지 소스 beautiful soup 변수 저장
    # 정상 치아 사진 링크들 변수에 저장
    teeth_link = []
    for i in soup.select('img._image'):
        teeth_link.append(i.attrs['src'])
    driver.back() # 뒤로 가기로 검색창 초기화
    
    # '치아' 키워드 검색
    element = driver.find_element(By.ID,'nx_query') #검색창 변수 지정
    element.send_keys('치아') #'치아' 검색창에 입력
    time.sleep(1)
    element.submit() #검색 클릭
     # 스크롤 페이지 최하단까지 내리기
    for i in range(6):
        driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
        time.sleep(1)
    html = driver.page_source # 현재 페이지 소스 변수 저장
    soup = BeautifulSoup(html, 'html.parser') # 페이지 소스 beautiful soup 변수 저장
     # 정상 치아 사진 링크들 변수에 저장
    for i in soup.select('img._image'):
         teeth_link.append(i.attrs['src'])
    
    # 사진 다운로드
    for i in range(len(cav_link)):
        req.urlretrieve(cav_link[i],'D:/Oracle/worksheet/data/final/teeth/cavity/{}.jpg'.format(i))
    for i in range(len(teeth_link)):
         req.urlretrieve(teeth_link[i],'D:/Oracle/worksheet/data/final/teeth/normal/{}.jpg'.format(i))    
    driver.quit() # driver 종료

######################################################################################

