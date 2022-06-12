# teeth-check

## PYTHON 기반 CNN 딥러닝 이미지 분류 협업 프로젝트

#### 1. 프로젝트 목표

* 문제정의
  * 충치 관련 궁금증 워드클라우드 시각화(네이버 지식인 '충치' 검색, 내용 추출)

![지식인WC1-removebg](https://user-images.githubusercontent.com/104886103/173189116-63a48aee-3d3a-4058-957e-874761a5d345.png)
```
치료 : 치료 필요성, 충치치료의 종류
 
치과 : 치과 방문 필요성, 우수 치과 추천 니즈
 
어금니 : 충치가 가장 많이 생기는 치아
 
레진 : 가장 많이 쓰이는 치과용 수복재료
```

__충치 발병 유무를 판단하고, 치과를 추천 받고자 하는 니즈 존재__  

#

* 분석계획

  * 일반 사용자가 사진 **이미지**를 바탕으로 **정상치아/충치**를 판단하고, 충치일 경우 **치과를 추천**하는 시스템 구현
   
  * **CNN 이미지 학습**으로 정상치아/충치 분류, **folium** 툴을 이용해 우수 치과 위치 **지도 시각화**
---------
#### 2. 데이터준비

* 필요 데이터 : 정상치아, 충치 실제 이미지 데이터
   
* 수집 방법 : 네이버, 구글 이미지 검색 웹 스크래핑, 캐글 데이터셋

* 데이터 정제 : 주제와 상관없는 이미지(그림, 그래프 등) 삭제, 한 이미지 당 하나의 이가 표현되도록 편집 작업

<img width="300" alt="이" src="https://user-images.githubusercontent.com/104886103/173189802-b537e443-d645-4d72-beda-bbfcca5663bb.PNG">

__이미지 데이터(722개) -> 학습(577개), 검증(145개)__


-----------------------
#### 3. 데이터 분석

* 이미지 RGB 변환

<img width="290" alt="이RGB" src="https://user-images.githubusercontent.com/104886103/173190155-20b96270-49cf-4af5-acf8-c5c374722ce2.PNG">  

#
* CNN 모델 형성 input_size:(64,64)

```python
model_cnn64 = Sequential()
model_cnn64.add(Conv2D(filters=32,kernel_size=(3,3),strides=(1,1),padding='same',input_shape=(64,64,3),activation='relu'))
model_cnn64.add(MaxPool2D(pool_size=(2,2)))

model_cnn64.add(Conv2D(filters=64, kernel_size=(3,3),strides=(1,1),padding='same',activation='relu'))
model_cnn64.add(MaxPool2D(pool_size=(2,2)))

model_cnn64.add(Conv2D(filters=64, kernel_size=(3,3),strides=(1,1),padding='same',activation='relu'))
model_cnn64.add(MaxPool2D(pool_size=(2,2)))

model_cnn64.add(Flatten())
model_cnn64.add(Dense(512,activation='relu'))
model_cnn64.add(Dropout(0.5))

model_cnn64.add(Dense(2,activation='softmax'))
model_cnn64.summary()
```

<img width="534" alt="graph64" src="https://user-images.githubusercontent.com/104886103/173191166-0e6e04d0-2eda-4655-b637-4bb5b70205d3.PNG">

> learning_rate : 0.001 / Epochs : 20 / Batch_size : 32
>
> train_accuracy : 0.97 / test_accuracy : 0.88 / train_loss : 0.09 / test_loss : 0.30  
#
* CNN 모델 형성 input_size:(128,128)

```python
model_cnn128 = Sequential()
model_cnn128.add(Conv2D(filters=32,kernel_size=(3,3),strides=(1,1),padding='same',input_shape=(128,128,3),activation='relu'))
model_cnn128.add(MaxPool2D(pool_size=(2,2)))

model_cnn128.add(Conv2D(filters=64, kernel_size=(3,3),strides=(1,1),padding='same',activation='relu'))
model_cnn128.add(MaxPool2D(pool_size=(2,2)))

model_cnn128.add(Conv2D(filters=64, kernel_size=(3,3),strides=(1,1),padding='same',activation='relu'))
model_cnn128.add(MaxPool2D(pool_size=(2,2)))

model_cnn128.add(Flatten())
model_cnn128.add(Dense(512,activation='relu'))
model_cnn128.add(Dropout(0.5))

model_cnn128.add(Dense(2,activation='softmax'))
model_cnn128.summary()
```

<img width="526" alt="graph128" src="https://user-images.githubusercontent.com/104886103/173191409-550cc531-e6c3-4310-9650-888d8313a4fe.PNG">

> learning_rate : 0.001 / Epochs : 20 / Batch_size : 32
> 
> train_accuracy : 0.96 / test_accuracy : 0.94 / train_loss : 0.10 / test_loss : 0.17  

#

* CNN 모델 형성 input_size:(224,224)

```python
model_cnn224 = Sequential()
model_cnn224.add(Conv2D(filters=32,kernel_size=(3,3),strides=(1,1),padding='same',input_shape=(224,224,3),activation='relu'))
model_cnn224.add(MaxPool2D(pool_size=(2,2)))

model_cnn224.add(Conv2D(filters=64, kernel_size=(3,3),strides=(1,1),padding='same',activation='relu'))
model_cnn224.add(MaxPool2D(pool_size=(2,2)))

model_cnn224.add(Conv2D(filters=64, kernel_size=(3,3),strides=(1,1),padding='same',activation='relu'))
model_cnn224.add(MaxPool2D(pool_size=(2,2)))

model_cnn224.add(Flatten())
model_cnn224.add(Dense(512,activation='relu'))
model_cnn224.add(Dropout(0.5))

model_cnn224.add(Dense(2,activation='softmax'))
model_cnn224.summary()
```

<img width="534" alt="graph224" src="https://user-images.githubusercontent.com/104886103/173191415-64b0875b-d4cf-4102-89e3-f991076bdbd8.PNG">

> learning_rate : 0.001 / Epochs : 20 / Batch_size : 32
> 
> train_accuracy : 0.89 / test_accuracy : 0.85 / train_loss : 0.28 / test_loss : 0.35  

#

* input_size (64, 128, 224) 별 비교

<img width="528" alt="graph_비교" src="https://user-images.githubusercontent.com/104886103/173191418-afb6fb72-1a43-41a5-b2b1-4dd05467dbe2.PNG">

__최적 모델 선택 : input_size(128,128)__

-------------------------

#### 4. 지도 시각화

* 모두닥 (병원 후기 공유 사이트)

<img width="608" alt="모두닥1" src="https://user-images.githubusercontent.com/104886103/173220520-7bc211b6-e425-4873-8eb2-0befc8769114.PNG">

<img width="384" alt="모두닥2" src="https://user-images.githubusercontent.com/104886103/173220521-9b2c1fd6-dd90-421a-ab73-59708aedcefd.PNG">

__충치 치료 검색 -> 치과정보(이름, 평점, 주소) 수집 (총 483개)__  

#

* Folium 지도시각화

<img width="838" alt="지도-강남" src="https://user-images.githubusercontent.com/104886103/173217653-11db6a7f-3e67-4ca1-ba45-7b34dd9764d7.PNG">



ㆍ 분석용 데이터 : 치아 이미지 데이터셋, 리뷰 평점 8.0 이상 치과의 주소 정보 데이터셋

ㆍ 학습데이터 / 검증데이터 설정
   
ㆍ 모델링 : TensorFlow - CNN 이미지 학습 분류 분석

ㆍ 모델평가 검증

ㆍ 치과 위치 정보(위도, 경도) 변환 및 folium 지도시각화




ㆍ 설계 구현

ㆍ 시스템 테스트 운영

#### ▷평가전개

ㆍ 모델 발전 계획 수립

ㆍ 프로젝트 평가
