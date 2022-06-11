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


pat


ax = plt.bar(pat['요양기관'][:-1],pat['환자수'][:-1],
        color=['purple','red','green','skyblue','orange'])
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f'))
plt.yticks(range(0,6000000,2500000))

for i in ax.patches:
    left,bottom,width,height = i.get_bbox().bounds
    plt.text(left,height+10000,format(int(height),',d'),fontdict=font1)

plt.title('2020년 요양기관별 충치 내원 환자수',size=15)


from urllib.parse import quote


kin_url=[]
for i in range(1,502,10):
    url = 'https://search.naver.com/search.naver?where=kin&kin_display=10&qt=&title=0&&answer=0&grade=0&choice=0&sec=0&nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&query=%EC%B6%A9%EC%B9%98&c_id=&c_name=&sm=tab_pge&kin_start='+str(i)+'&kin_age=0'
    html = urlopen(url)
    soup = BeautifulSoup(html,'html.parser')

    for i in soup.select('div.api_subject_bx > ul > li'):
        kin_url.append(i.select_one('div.question_group').find('a')['href'])
    time.sleep(1)
 
len(kin_url)

quote('§')

kin_url2 = [i.replace('§','%C2%A7') for i in kin_url]

txt = []
for i in kin_url2:
    try:
        html = urlopen(i)
        soup = BeautifulSoup(html,'html.parser')
        txt.append(soup.select_one('div.c-heading__content').text.strip())
    except:
        print(i)
    time.sleep(1)
        
len(txt)


from konlpy.tag import Okt
okt = Okt()


k_stopwords = pd.read_csv('c:/data/k_stopwords.csv')
k_s = [i for i in k_stopwords.아]

k_s.append('충치')

def okt_pos(arg):
    token_corpus =[]
    for i in okt.pos(arg):
        if i[1] in ['Noun','Adjective']:
            token_corpus.append(i[0])
    token_corpus = [x for x in token_corpus if len(x) >1]        
    return token_corpus

from wordcloud import WordCloud ,ImageColorGenerator
from collections import Counter

kin_token = [okt_pos(i) for i in txt]
kin_token = txt.apply(lambda x : okt_pos(x))

# 불용어 처리, 2글자 이상 뽑기
kin_word = [word2 for word in kin_token for word2 in word if word2 not in k_s and len(word2) >= 2]

Counter(kin_word).most_common(100)

kin_word_df = pd.DataFrame.from_dict([Counter(kin_word)]).T
kin_word_df.reset_index(inplace=True)
kin_word_df.columns = ['word','freq']
kin_word_df.set_index('word',inplace=True)
kin_top = kin_word_df[kin_word_df['freq']>=15]
kin_top.to_dict()['freq']

import numpy as np
from PIL import Image

tooth_mask5 = np.array(Image.open('c:/data/tooth_mask5.png'))
tooth_mask5 = 255-tooth_mask5

w = WordCloud(font_path='c:/windows/fonts/H2HDRM.TTF',
              width=900,height=500,
              background_color='white',
              colormap='cool',
              mask=tooth_mask6).generate_from_frequencies(kin_top.to_dict()['freq']) 
plt.imshow(w)
plt.axis('off')











