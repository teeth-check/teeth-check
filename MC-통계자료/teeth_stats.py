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

hos_df.to_csv('c:/data/teamproject/hospital.csv',encoding="utf-8-sig")
hos_df.info()   

# 평점 -> 숫자 변환
hos_df.point = hos_df.point.astype('float')

# 평점 8점이상 & 서울 소재 치과
hos_sort = hos_df.loc[(hos_df['point']>=8.0) & (hos_df.addr.str.startswith('서울')),].sort_values(by='point',ascending=False)

hos_sort.to_csv('c:/data/teamproject/hos_sort.csv',encoding="utf-8-sig")

hos_final = pd.read_csv('c:/data/teamproject/hos_final.csv',encoding='cp949')

hos_final.to_csv('c:/data/teamproject/hos_final_final.csv',encoding="utf-8-sig")

del hos_final['_']

hos_final.X


goo = pd.read_csv('c:/data/teamproject/구정보.csv',encoding='cp949')


import folium


for i in goo.index:
    m = folium.Map(location = [goo.Y[i] , goo.X[i]], zoom_start=15)
    
    for j in hos_final.index:
        folium.CircleMarker([hos_final['Y'][j],hos_final['X'][j]],
                            radius=(hos_final['point'][j]*10-70),
                            color='blue',
                            fill='True',
                            popup=hos_final['name'][j],
                            tooltip=hos_final['point'][j]).add_to(m)
    
    m.save('c:/data/teamproject/'+goo['구'][i]+'map.html')


# 충치 관련 통계
pat = pd.read_csv('c:/data/teamproject/요양기관.csv',encoding='cp949')
year = pd.read_csv('c:/data/teamproject/년도별.csv',encoding='cp949')
year = year.drop(5,axis=0)



year = year.astype('int64')


import matplotlib.pylab as plt
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname='c:/windows/fonts/HMFMMUEX.TTC').get_name()
rc('font',family=font_name)
import matplotlib.ticker as mticker
import matplotlib as mpl



plt.plot(year['년도'],year['환자수'],marker='o',label='환자수')
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f'))
plt.yticks(range(5500000,7000001,500000))
plt.xticks(year['년도'],[str(i) +'년' for i in year['년도']])

font1 = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 11}

for i in year.index:
    if i == 4:
        plt.text(year['년도'][i]-0.6,year['환자수'][i]+70000,format(year['환자수'][i],',d'),fontdict=font1)
    else:
        plt.text(year['년도'][i]-0.2,year['환자수'][i]+50000,format(year['환자수'][i],',d'),fontdict=font1)
plt.legend(loc='upper left')

