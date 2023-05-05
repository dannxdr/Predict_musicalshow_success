# -*- coding: utf-8 -*-
"""딥솜+코드.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WPBkmVT5XvEA9sAGpusjObMiceF3c5e3

### kopis open api 크롤링
"""

import pandas as pd

# 공연id 추출을 위한 공연 목록
url = 'http://www.kopis.or.kr/openApi/restful/prfstsPrfBy?service=b9f51495d6894442ad44f96a0b3b174a&cpage=1&rows=10000&stdate=20200120&eddate=20220906&shcate=AAAB'

df = pd.read_xml(url, xpath='./*')
df

df.to_csv("공연목록.csv", index=False, encoding='utf-8-sig')

# 공연상세목록

## 공연id 추출
id = df['mt20id'].astype(str)
final = pd.DataFrame()

for i in range(len(id)):
  url2 = 'http://www.kopis.or.kr/openApi/restful/pblprfr/'+id[i]+'?service=b9f51495d6894442ad44f96a0b3b174a'
  df2 = pd.read_xml(url2, xpath='./*')
  final_df = pd.DataFrame(data=df2)
  final = final.append(final_df)
  print(df2)

final.to_csv("공연상세.csv", index=False, encoding='utf-8-sig')

import re

final1 = pd.read_csv("/content/공연상세.csv", encoding='utf-8')

# 데이터프레임에서 공연 아이디, 이름, 포스터만 추출
final1 = final1[['mt20id', 'prfnm', 'poster']]

# 포스터가 없는 행 삭제
final1 = final1.dropna(subset = ['poster'])

# 특수 문자 제거(중복된 이름의 공연 제거를 위함)
final1['prfnm'] = final1['prfnm'].str.replace(pat=r'\[[^)]*\]',repl=r' ')
final1['prfnm'] = final1['prfnm'].str.replace(pat=r'\([^)]*\)',repl=r' ')

# 중복된 제목 제거
final1 = final1.drop_duplicates(subset=['prfnm'], keep = 'first')
final1

final1.to_csv("공연목록(중복제거).csv", index=False, encoding='utf-8-sig')

final1 = pd.read_csv("/content/drive/MyDrive/KOPIS/정형데이터/공연목록(중복제거) (1).csv", encoding='utf-8')
final1

# 데이터프레임에서 포스터 이미지 저장
import urllib.request
from collections import defaultdict

img_url = []
location = []
for k in range(final1.shape[0]):
  img = str(final1['poster'][k])
  id = final1['mt20id'][k]
  img_url.append(img)
  location.append("/content/drive/MyDrive/KOPIS/poster/"+str(id)+".jpg")

for i in range(len(img_url)):
  urllib.request.urlretrieve(img_url[i], location[i])

musical_df = pd.read_csv("/content/drive/MyDrive/KOPIS 공모전/정형데이터/뮤지컬데이터.csv", encoding='utf-8')
musical_df

# 수상작 추출
url3 = 'http://www.kopis.or.kr/openApi/restful/prfawad?service=b9f51495d6894442ad44f96a0b3b174a&cpage=1&rows=10000&stdate=20200120&eddate=20220906&shcate=AAAB'

awards = pd.read_xml(url3, xpath='./*')
print(awards)

awards.to_csv("수상작.csv", index=False, encoding='utf-8-sig')

awards = awards[['mt20id', 'awards']]
awards

awards.to_csv("수상작.csv", index=False, encoding='utf-8-sig')

# 뮤지컬데이터와 수상여부 결합

musical = pd.merge(musical_df, awards, on='mt20id', how='left')
musical.to_csv("뮤지컬데이터(1).csv", index=False, encoding='utf-8-sig')

"""### 흥행수치 및 공연코드 전처리



"""

import os
import pandas as pd
import numpy as np

#저장된 raw 데이터 파일 불러오기
df = pd.read_excel('C:\\Users\\clstm_\\OneDrive\\Desktop\\KOPIS\\통합 문서2.xlsx',
                   usecols=['공연코드', '공연시작일자', '공연종료일자', '소요시간', '장르명', '관람연령'])
df = df[df['장르명']=='뮤지컬'].reset_index(drop=True)

#데이터 형식 바꾸기
for q in range(df.shape[0]):
  df.iloc[q, 0] = str(df.iloc[q, 0])
  df.iloc[q, 1] = str(df.iloc[q, 1])
  df.iloc[q, 2] = str(df.iloc[q, 2])
  df.iloc[q, 3] = str(df.iloc[q, 3])
  df.iloc[q, 4] = str(df.iloc[q, 4])
  df.iloc[q, 5] = str(df.iloc[q, 5])

result = df.groupby('공연코드').head(1)
result.to_csv('C:\\Users\\clstm_\\OneDrive\\Desktop\\KOPIS\\22_concat.csv')
print(result)

url = 'C:\\Users\\clstm_\\OneDrive\\Desktop\\KOPIS\\'
folder_list = os.listdir(url)

#필요한 columns만 추출하기
for i in folder_list[3:8]:
    listing = os.listdir(url+str(i))
    for k in range(len(listing)):
        df = pd.read_excel(url+i+'\\'+listing[k], usecols=['공연코드', '공연시작일자', '공연종료일자', '소요시간', '장르명', '관람연령'])
        df = df[df['장르명']=='뮤지컬'].reset_index(drop=True)

        for q in range(df.shape[0]):
            df.iloc[q, 0] = str(df.iloc[q, 0])
            df.iloc[q, 1] = str(df.iloc[q, 1])
            df.iloc[q, 2] = str(df.iloc[q, 2])
            df.iloc[q, 3] = str(df.iloc[q, 3])
            df.iloc[q, 4] = str(df.iloc[q, 4])
            df.iloc[q, 5] = str(df.iloc[q, 5])

        result = df.groupby('공연코드').head(1)
        result.to_csv('C:\\Users\\clstm_\\OneDrive\\Desktop\\KOPIS\\new_2\\' + i + '_' + str(k) + '.csv')
        print(i + '의 ' + str(k) + '번째까지 완료')
        print(result)


        reserveds_01 = []
        reserveds_02 = []
        for r in range(df.shape[0]):
            if df.iloc[r, 3] == 1:
                try:
                    reserved = df.iloc[r, 4]*df.iloc[r, 5]
                    reserveds_01.append(reserved)
                    reserveds_02.append(0)
                except:
                    reserveds_01.append(0)
                    reserveds_02.append(0)
            elif df.iloc[r, 3] == 2:
                try:
                    reserved = df.iloc[r, 4]*df.iloc[r, 5]
                    reserveds_01.append(0)
                    reserveds_02.append(reserved)
                except:
                    reserveds_01.append(0)
                    reserveds_02.append(0)
            else:
                reserveds_01.append(0)
                reserveds_02.append(0)

        df['예매금액'] = reserveds_01
        df['취소금액'] = reserveds_02

        df1 = df.groupby(['공연코드', '공연일시'])['예매금액'].sum()
        df2 = df.groupby(['공연코드', '공연일시'])['취소금액'].sum()

        result = pd.merge(df1, df2, how='left', on=['공연코드', '공연일시'])
        result = pd.merge(result, df3, how='left', on=['공연코드', '공연일시'])
        result = pd.merge(result, df4, how='left', on=['공연코드', '공연일시'])
        result = pd.merge(result, df5, how='left', on=['공연코드', '공연일시'])
        
        result.to_csv('C:\\Users\\clstm_\\OneDrive\\Desktop\\KOPIS\\new\\'+i+'_'+str(k)+'.csv')
        print(i+'의 '+str(k)+'번째까지 완료')

#흥행수치 2가지로 도출하기
result['흥행수치_1'] = (result['예매금액']-result['취소금액'])/(result['장당금액']*result['좌석수'])
result['흥행수치_2'] = (result['판매좌석수']/result['좌석수'])
result_1 = result.groupby('공연코드')['흥행수치_1'].mean()
result_2 = result.groupby('공연코드')['흥행수치_2'].mean()
result = pd.merge(result_1, result_2, how='left', on='공연코드')

url = 'C:\\Users\\clstm_\\OneDrive\\Desktop\\KOPIS\\new'
files_list = os.listdir(url)
result = pd.DataFrame()

for file in files_list:
    path = os.path.join(url, file)
    preprocessed = pd.read_csv(path)
    result = pd.concat([result, preprocessed])

result.rename(columns={'counts':'판매좌석수'}, inplace=True)

result['흥행수치_1'] = (result['예매금액']-result['취소금액'])/(result['장당금액']*result['좌석수'])
result['흥행수치_2'] = (result['판매좌석수']/result['좌석수'])
result_1 = result.groupby('공연코드')['흥행수치_1'].mean()
result_2 = result.groupby('공연코드')['흥행수치_2'].mean()
result_3 = result.groupby('공연코드')['좌석수'].max()
result = pd.merge(result_1, result_2, how='left', on='공연코드')
result = pd.merge(result, result_3, how='left', on='공연코드')

#서로 다른 공연코드 맞추기
concat_1 = pd.read_csv('C:\\Users\\clstm_\\OneDrive\\Desktop\\KOPIS\\19_21_concat.csv')
concat_2 = pd.read_csv('C:\\Users\\clstm_\\OneDrive\\Desktop\\KOPIS\\22_concat.csv')
api = pd.read_csv('C:\\Users\\clstm_\\OneDrive\\Desktop\\KOPIS\\공연상세.csv')

for i in range(concat_1.shape[0]):
  concat_1.iloc[i, 1] = concat_1.iloc[i, 1].replace('.', '-')
  concat_1.iloc[i, 2] = concat_1.iloc[i, 2].replace('.', '-')

for i in range(api.shape[0]):
  api.iloc[i, 1] = api.iloc[i, 1].replace('.', '-')
  api.iloc[i, 2] = api.iloc[i, 2].replace('.', '-')

list_01 = []
list_02 = []
concated = pd.concat([concat_1, concat_2])
concated = concated[['공연코드', '공연시작일자', '공연종료일자', '소요시간', '관람연령']]
api = api[['mt20id', 'prfpdfrom', 'prfpdto', 'prfruntime', 'prfage']]

print(concated)
print(api)

for i in range(api.shape[0]):
  for k in range(concated.shape[0]):
    if (concated.iloc[k, 1] == api.iloc[i, 1]) and (concated.iloc[k, 2] == api.iloc[i, 2]) \
            and (concated.iloc[k, 3] == api.iloc[i, 3]) and (concated.iloc[k, 4] == api.iloc[i, 4]):
      list_01.append(concated.iloc[k, 0])
      list_02.append(api.iloc[i, 0])

df = pd.DataFrame()
df['공연코드_1'] = list_01
df['공연코드_2'] = list_02

"""### 중소규모 데이터 라벨링

"""

import pandas as pd

df = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/모든공연.csv')
df = df[['공연코드_2', '좌석수', '판매좌석수']]
df

df = df[df['좌석수'] <= 1000]
df['판매좌석수'] = df['판매좌석수'].str.replace(pat=r'[ㄱ-ㅣ가-힣]+',repl=r'',regex=True)
df

df = df.dropna(subset = ['좌석수','판매좌석수'])
df = df[df.좌석수 != 0]
df

df['x'] = df['좌석수'].astype(float)-df['판매좌석수'].astype(float)
df

import numpy as np

df['레이블'] = np.where(df['좌석수'].astype(float)/2 >= df['x'], 1,0)
df = df[['공연코드_2', '레이블']]
df = df.rename(columns = {'공연코드_2' : '공연코드'})
df

df2 = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/모든공연.csv')
df2  = df2[['공연코드_2',	'좌석수',	'무대시설_무대넓이',	'공연일시',	'공연시작일자',	'공연종료일자',	'출연진내용',	'제작진내용',	'기획제작사명']]
df2 = df2.drop_duplicates(subset=['공연코드_2'], keep = 'first')
df2 = df2.rename(columns = {'공연코드_2' : '공연코드'})
df2

# posters 폴더 안 이미지 파일 리스트 불러오기
import glob
import os

image_list = glob.glob("/content/drive/MyDrive/KOPIS/posters_all/posters/*.jpg")

# resized 된 이미지 빼고 데이터프레임
df3 = pd.DataFrame(image_list, columns=['포스터경로'])
df3 = df3[~df3["포스터경로"].str.contains("resized")]
df3

# 포스터 이름
path = "/content/drive/MyDrive/KOPIS/posters_all/posters"
img_list_df = os.listdir(path)
img_list_df = [img for img in img_list_df if img.endswith('.jpg')] 
img_list_df = pd.DataFrame(img_list_df, columns=['공연코드'])
img_list_df = img_list_df[~img_list_df["공연코드"].str.contains("resized")]

# 공연코드에서 .jpg 제거(흥행수치와 맞추기 위함)
img_list_df["공연코드"]= img_list_df["공연코드"].str.replace(pat=r'.jpg',repl=r'',regex=True)
img_list_df["공연코드"]

# 포스터경로, 공연코드 결합
img_list = pd.concat([img_list_df, df3], axis=1)
img_list

# 흥행수치와 img_list 결합
img_rate = pd.merge(df2, df, on="공연코드", how="left")
img_rate = pd.merge(img_rate, img_list, on="공연코드", how="left") 
img_rate = img_rate.dropna(subset=['포스터경로'])

img_rate = img_rate.drop_duplicates(subset=['공연코드'], keep = 'first')
img_rate = img_rate.dropna(subset=['레이블'])
img_rate

posters = img_rate[['공연코드', '포스터경로', '레이블']]
posters

posters['레이블'] = pd.to_numeric(posters['레이블'])

"""### PlayDB에서 제작사, 제작진, 배우 전체 크롤링"""

pip install selenium

from urllib.request import urlopen
from selenium import webdriver
import pandas as pd
import time

# 제작진 전체 크롤링
driver = webdriver.Chrome(executable_path = 'C:/Users/ttwin/Desktop/pythonProject/chromedriver.exe')

f = open("제작진.csv", "w", encoding="utf-8-sig")

for i in range(1, 210):
    driver.get("http://www.playdb.co.kr/artistdb/list_iframe.asp?Page="+str(i)+"&code=013011&sub_code=&ImportantSelect=&ClickCnt=Y&NameSort=&Country=Y&TKPower=&WeekClickCnt=&NameStart=&NameEnd=")
    time.sleep(1)
    names = driver.find_elements_by_css_selector("body > table > tbody > tr > td > table > tbody > tr > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > a")
    for name in names:
        print(name.text)
        f.write(name.text+"\n")
f.close()

# 제작사 전체 크롤링
driver = webdriver.Chrome(executable_path = 'C:/Users/ttwin/Desktop/pythonProject/chromedriver.exe')

f = open("제작사.csv", "w", encoding="utf-8-sig")

for i in range(1, 21):
    driver.get("http://www.playdb.co.kr/productiondb/index_iframe.asp?Page="+str(i)+"&Sort=click&Part=000001")
    time.sleep(1)
    companies = driver.find_elements_by_css_selector("body > table > tbody > tr > td > table > tbody > tr > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > a > b")
    for company in companies:
        print(company.text)
        f.write(company.text+"\n")
f.close()

# 배우 전체 크롤링
driver = webdriver.Chrome(executable_path = 'C:/Users/ttwin/Desktop/pythonProject/chromedriver.exe')

f = open("배우.csv", "w", encoding="utf-8-sig")

for i in range(1, 366):
    driver.get("http://www.playdb.co.kr/artistdb/list_iframe.asp?Page="+str(i)+"&code=013003&sub_code=&ImportantSelect=&ClickCnt=Y&NameSort=&Country=Y&TKPower=&WeekClickCnt=&NameStart=&NameEnd=")
    time.sleep(1)
    actors = driver.find_elements_by_css_selector("body > table > tbody > tr > td > table > tbody > tr > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > a")
    for actor in actors:
        print(actor.text)
        f.write(actor.text+"\n")
f.close()

import os
import pandas as pd
import glob

input = '/content/drive/MyDrive/KOPIS 공모전/정형데이터/제작진,사,뮤배/'
output = '제작진+사+뮤배.csv'

file_list = os.listdir(input)
file_list_py = [file for file in file_list if file.endswith('.csv')] 
file_list_py

names = pd.DataFrame()
for i in file_list_py:
  data = pd.read_csv(input + i,header=None)
  names = pd.concat([names, data], axis=1)

names.columns = ["제작진", "제작사", "배우"]
names = names.reset_index(drop = True)
names.head(10)

names.to_csv("제작사+진+배우.csv", encoding='utf-8-sig')

"""### 인물 수 카운트"""

import pandas as pd

df = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/소중규모.csv')

data = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/제작사+진+배우(최종의 최종).csv')

#제공데이터와 제작사 순위를 크롤링한 데이터 제작사 표기 맞추기
data["제작사"] = data["제작사"].str.replace('([^\w]|주)', repl=r' ', regex=True)

#크롤링한 데이터에서 제작사만 추출
data3 = data['제작사'].values.tolist()

#제공데이터에서 rank안에 들어가는 제작사가 있을 경우 +1씩 카운트
c_data = []

for c_string in df['기획제작사명']:
	num = 0
	if type(c_string) == str:
		c_list = c_string.split(", ")
		for c in c_list:
			if c in data3:
				num += 1
	c_data.append(num)
df['company'] = c_data

#크롤링한 데이터에서 배우만 리스트로 추출
data2 = data['배우'].values.tolist()

#제공데이터에서 rank안에 들어가는 배우가 있을 경우 +1씩 카운트
a_data = []

for a_string in df['출연진내용']:
	num = 0
	if type(a_string) == str:
		actors_list = a_string.split(", ")
		for actor in actors_list:
			if actor in data2:
				num += 1
	a_data.append(num)
df['actor'] = a_data

#크롤링한 데이터에서 제작진만 리스트로 추출
data1 = data['제작진'].values.tolist()

#제공데이터에서 rank안에 들어가는 제작진이 있을 경우 +1씩 카운트
d_data = []

for d_string in df['제작진내용']:
	num = 0
	if type(d_string) == str:
		d_list = d_string.split(", ")
		for d in d_list:
			if d in data1:
				num += 1
	d_data.append(num)
df['director'] = d_data

"""### 데이터 전처리1"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
df = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/모든공연.csv')

arb = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/소중규모데이터_전처리.csv')

DF = pd.merge(df, arb[['공연코드', '레이블', 'director', 'actor', 'company']], how='right', left_on='공연코드_2', right_on='공연코드')
#qwe = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/정형데이터_최종.csv')
#DF = pd.merge(DF, qwe[['공연코드', 'company', 'director', 'actor', 'award_counts']], on='공연코드', how='left')

DF = DF.drop_duplicates(subset=['공연코드'], keep='first')
DF = DF.dropna(subset=['공연코드'])
DF = DF.fillna(0)

DF

DF = DF[['공연코드', '시설특성', '편의시설_레스토랑 여부', '편의시설_카페 여부', '편의시설_편의점 여부', '편의시설_놀이방 여부',
       '편의시설_수유실 여부', '장애인시설_주차장 여부', '장애인시설_화장실 여부', '장애인시설_경사로 여부',
       '장애인시설_전용엘리베이터 여부', '주차시설_자체 여부', '주차시설_공영 여부', '좌석수', '장애인석', '무대시설_오케스트라피트 여부', '무대시설_연습실 여부', '무대시설_분장실 여부',
       '공연일시', '공연시작일자', '공연종료일자', '소요시간', '공연지역명', 'director', 'actor', 'company',
       '관람연령', '아동공연 여부', '축제 여부', '내한공연 여부', '오픈런 여부', 
       '출연진내용',	'제작진내용',	'기획제작사명', '레이블']]
DF

DF.isnull().sum()

# 제작진 수 카운트
for actors_string in DF['제작진내용']:
 if type(actors_string) == str:
   DF['제작진수'] = DF.제작진내용.str.count(',') + 1
   
DF['제작진수']

# 출연진 수 카운트
for actors_string in DF['출연진내용']:
 if type(actors_string) == str:
   DF['출연진수'] = DF.출연진내용.str.count(',') + 1
   
DF['출연진수']

# 제작사 수 카운트
for actors_string in DF['기획제작사명']:
 if type(actors_string) == str:
   DF['제작사수'] = DF.기획제작사명.str.count(',') + 1
   
DF['제작사수']

DF = DF.fillna(0)
DF

"""### 전처리"""

DF.columns
#출연진내용, 제작진내용, 기획제작사명, 무대시설_무대넓이,

import datetime

def preprocessing(df):

  df.fillna(0, inplace=True)

  df['시설특성'] = df['시설특성'].map({'민간(대학로 외)' : 1, '민간(대학로)' : 2, '공공(기타)' : 3, 
                                '국립' : 4, '공공(문예회관)' : 5, '기타(비공연장)' : 6})
  
  df['편의시설_레스토랑 여부'] = df['편의시설_레스토랑 여부'].map({'Y' : 1, 'N' : 2})
  df['편의시설_카페 여부'] = df['편의시설_카페 여부'].map({'Y' : 1, 'N' : 2})
  df['편의시설_편의점 여부'] = df['편의시설_편의점 여부'].map({'Y' : 1, 'N' : 2})
  df['편의시설_놀이방 여부'] = df['편의시설_놀이방 여부'].map({'Y' : 1, 'N' : 2})
  df['편의시설_수유실 여부'] = df['편의시설_수유실 여부'].map({'Y' : 1, 'N' : 2})
  df['장애인시설_주차장 여부'] = df['장애인시설_주차장 여부'].map({'Y' : 1, 'N' : 2})
  df['장애인시설_화장실 여부'] = df['장애인시설_화장실 여부'].map({'Y' : 1, 'N' : 2})
  df['장애인시설_경사로 여부'] = df['장애인시설_경사로 여부'].map({'Y' : 1, 'N' : 2})
  df['장애인시설_전용엘리베이터 여부'] = df['장애인시설_전용엘리베이터 여부'].map({'Y' : 1, 'N' : 2})
  df['주차시설_자체 여부'] = df['주차시설_자체 여부'].map({'Y' : 1, 'N' : 2})
  df['주차시설_공영 여부'] = df['주차시설_공영 여부'].map({'Y' : 1, 'N' : 2})
  df['장애인석'] = df['장애인석'].map({'Y' : 1, 'N' : 2})
  df['무대시설_오케스트라피트 여부'] = df['무대시설_오케스트라피트 여부'].map({'Y' : 1, 'N' : 2})
  df['무대시설_연습실 여부'] = df['무대시설_연습실 여부'].map({'Y' : 1, 'N' : 2})
  df['무대시설_분장실 여부'] = df['무대시설_분장실 여부'].map({'Y' : 1, 'N' : 2})
  df['아동공연 여부'] = df['아동공연 여부'].map({'Y' : 1, 'N' : 2})
  df['축제 여부'] = df['축제 여부'].map({'Y' : 1, 'N' : 2})
  df['내한공연 여부'] =  df['내한공연 여부'].map({'Y' : 1, 'N' : 2})
  df['오픈런 여부'] = df['오픈런 여부'].map({'Y' : 1, 'N' : 2})
     
  #df['극작가명'] = df['극작가명'].map({'손님(각색)' : 1})   

  df['소요시간'] = df['소요시간'].map({'2시간 20분' : 1, '1시간 30분' : 2, '1시간 50분' : 3, '1시간' : 4, '1시간 25분' : 5, '1시간 40분' : 6, '2시간' : 7,
                                 '1시간 35분' : 8, '2시간 30분' : 9, '1시간 10분' : 10, '1시간 20분' : 11, '1시간 45분' : 12, '55분' : 13,
                                 '2시간 10분' : 14, '2시간 5분' : 15, '50분' : 16, '1시간 15분' : 17, '2시간 15분' : 18, '1시간 5분' : 19,
                                 '2시간 35분': 20, '2시간 40분' : 21})
  
  df['공연지역명'] = df['공연지역명'].map({'서울' : 1, '충청도' : 2, '경기도' :3, '경상도' : 4, '전라도' : 5, '강원도' : 6})

  df['관람연령'] = df['관람연령'].map({'전체 관람가' : 1, '만 13세 이상' : 2, '만 14세 이상' : 2, '만 15세 이상' :2, '만 17세 이상' : 2,
                               '만 16세 이상' : 2, '만 12세 드림아트센터이상' : 2, '만 8세 이상' : 3, '만 7세 이상': 3, '만 5세 이상': 3, '만 10세 이상': 3, 
                               '만 11세 이상': 3, '36개월 이상': 3, '만 9세 이상': 3, '만 6세 이상': 3, '만 4세 이상': 3, '24개월 이상': 3, '48개월 이상': 3, '만 3세 이상': 3})
  

  df['공연일시'] = pd.to_datetime(df['공연일시'])
  df['시작-종료일수'] = pd.to_datetime(df['공연종료일자']) - pd.to_datetime(df['공연시작일자'])
  df['시작-종료일수'].dt.days

  df['공연일시_요일'] = df['공연일시'].dt.weekday
  df['공연일시_시간'] = df['공연일시'].dt.time

  df['공연일시_시간'].astype(str).str.replace(pat=r'[^\w]',repl=r'',regex=True)

# 필요 없는 행 빼기
  drops = ['공연일시', '공연종료일자','공연시작일자', '출연진내용',	'제작진내용',	'기획제작사명']
  df = df.drop(drops, axis=1)

  return df

DF = preprocessing(DF)
DF

DF['시작-종료일수'] = DF['시작-종료일수'].dt.days
DF['공연일시_시간'] = DF['공연일시_시간'].astype(str).str.replace(pat=r'[^\w]',repl=r'',regex=True)
DF

DF.to_csv('중소규모_전처리.csv', encoding='utf-8-sig')

"""### 경로 지정해서 이미지 파일 라벨링에 맞게 옮기기"""

from numpy import add 
import shutil

directory0 = "/content/drive/MyDrive/KOPIS/1000posters/0" 
directory1 = "/content/drive/MyDrive/KOPIS/1000posters/1" 

for posters, ad in zip(posters['레이블'], posters['포스터경로']): 
  if posters == 0: 
    shutil.copy(ad, directory0)
  elif posters == 1: 
    shutil.copy(ad, directory1)

directory = "/content/drive/MyDrive/KOPIS/1000posters"

for posters, ad in zip(posters['레이블'], posters['포스터경로']): 
  shutil.copy(ad, directory)

path = "/content/drive/MyDrive/KOPIS/1000posters/"
dr0 = sorted(glob.glob(path+"/0" + '/*jpg'))
dr1 = sorted(glob.glob(path+"/1"+'/*jpg'))

print('dr0 이미지 개수: {}\ndr1 이미지 개수: {}'.format(len(dr0), len(dr1)))

import math

dr0_test_count = round(len(dr0)*0.08)
dr1_test_count = round(len(dr1)*0.08)

print('dr0 test파일에 들어갈 이미지 개수 : {}/{}'.format(dr0_test_count,len(dr0)))
print('dr1 test파일에 들어갈 이미지 개수 : {}/{}'.format(dr1_test_count,len(dr1)))

import shutil
import random
def split(posters, test_count, train_path, test_path):
  
  test_files=[]
  for i in random.sample( posters, test_count ):
    test_files.append(i)

  # 차집합으로 train/test 리스트 생성하기
  train_files = [x for x in posters if x not in test_files]

  for k in train_files:
    shutil.copy(k, train_path)
  
  for c in test_files:
    shutil.copy(c, test_path)

  print('train 폴더 이미지 개수 : {}\ntest 폴더 이미지 개수 : {}'.format(len(glob.glob(train_path+'/*')),len(glob.glob(test_path+'/*'))))

dr0_train_path='/content/drive/MyDrive/KOPIS/1000posters/train/0'
dr0_test_path='/content/drive/MyDrive/KOPIS/1000posters/test/0'

dr1_train_path='/content/drive/MyDrive/KOPIS/1000posters/train/1'
dr1_test_path='/content/drive/MyDrive/KOPIS/1000posters/test/1'


split(dr0, dr0_test_count, dr0_train_path, dr0_test_path)
split(dr1, dr1_test_count, dr1_train_path, dr1_test_path)

"""### 이미지에 맞춰 정형데이터 train_test_split"""

import os
import pandas as pd 

file_name = []

for i in range(0,2):
  path = '/content/drive/MyDrive/KOPIS/posters_all/train/'+str(i)+'/'
  file_list = os.listdir(path)
  file_list

  #file_name = []
  for file in file_list:
    if file.count(".") == 1: 
      name = file.split('.')[0]
      file_name.append(name)
    else:
      for k in range(len(file)-1,0,-1):
        if file[k]=='.':
          file_name.append(file[:k])
          break
                
file_name
train = pd.DataFrame(file_name, columns=['공연코드'])
train = train.dropna(subset=['공연코드'])
train

df2 = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/중소규모_전처리 (1).csv')
df2

# 흥행수치와 img_list 결합
train = pd.merge(df2, train, on="공연코드", how="right")
train

file_name = []

for i in range(0,2):
  path = '/content/drive/MyDrive/KOPIS/posters_all/test/'+str(i)+'/'
  file_list = os.listdir(path)
  file_list

  #file_name = []
  for file in file_list:
    if file.count(".") == 1: 
      name = file.split('.')[0]
      file_name.append(name)
    else:
      for k in range(len(file)-1,0,-1):
        if file[k]=='.':
          file_name.append(file[:k])
          break
                
file_name
test = pd.DataFrame(file_name, columns=['공연코드'])
test = test.dropna(subset=['공연코드'])
test

test = pd.merge(df2, test, on="공연코드", how="right")
test

train.to_csv('train_nums2.csv', encoding='utf-8-sig')

test.to_csv('test_nums2.csv', encoding='utf-8-sig')

"""### pycaret"""

!pip uninstall sklearn -y
!pip install --upgrade sklearn
!pip install scikit-learn==0.23.2 --user

import sklearn
sklearn.__version__

!pip install pycaret

!pip install Jinja2==3.1.2

from pycaret.utils import enable_colab
enable_colab()

from pycaret.classification import *

import pandas as pd
data = pd.read_csv('/content/소중규모데이터_전처리 (1).csv')

exp = setup(data = data,  
            target = '레이블',
            
            normalize = True, 
            normalize_method = 'minmax', # 기본은 zscore 
            
            transformation = True, 
            
            fold = 5, # 기본적으로 10 fold 로 training 한다.
            fold_shuffle=True,
            
            ignore_features = ['Unnamed: 0', 'Unnamed: 0.1', '공연코드',
                                '출연진내용','제작진내용', '기획제작사명', '포스터경로'], # 제외할 컬럼 (이거 너무 편하다!)
            numeric_features = ['무대시설_무대넓이','director','actor','company','좌석수'],
            categorical_features = [], # 지정하면 onehotencoding된다. 
            date_features = ['공연일시',
       '공연시작일자', '공연종료일자'], # 날짜 feature를 년월일시 로 바꿔서 onehotencoding 해준다. 
            
            silent = True, # setup 시 중간에 피쳐속성 확인하고 엔터 쳐줘야하는데 알아서 넘어가게 해준다.
           
            session_id = 123, # random state number 지정
            
            use_gpu = True, # gpu 사용 옵션
            
            feature_selection = True,
            feature_selection_method = 'classic', # or 'boruta' 
            # classic 은 permutation importance 기반이다.
            
          
            
            # custom_pipeline = pipe, preprocess =False 
            # 두 개는 세트, 사용자가 원하는 파이프라인을 구성할 수 있다. 
            
            )

models()

compare_models()

"""### VGG16 이미지 학습"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import shutil
import os, glob

from PIL import Image
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import keras.backend as K
import tensorflow as tf

from keras.applications.vgg16 import VGG16
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers import Adam

#이미지 데이터 전처리 후 배열로 변환
image_w = 224
image_h = 224
pixels = image_h * image_w * 3
X = {'train':[], 'test':[]}
Y = {'train':[], 'test':[]}
categories = ['0', '1']

x_list_str = ['train',  'test']

destination = '/content/drive/MyDrive/KOPIS/posters_all/'

for list_str in x_list_str:
  for idx, cls in enumerate(categories):
    label = [0 for i in range(len(categories))]
    label[idx] = 1

    image_dir = destination + list_str +'/' + cls
    files = glob.glob(image_dir+'/*.jpg')
    print(list_str, cls, " 파일 길이 : ", len(files))

    for n, k in enumerate(files):
      files[n] = k.split('/')[-1]
    files = sorted(files)

    for i, f in enumerate(files):
      f = destination + list_str + '/' + cls + '/' + str(f)
      img = Image.open(f)
      img = img.convert("RGB")
      img = img.resize((image_w, image_h))
      data = np.asarray(img)

      X[list_str].append(data)
      Y[list_str].append(label)

  print('ok', len(Y[list_str]))
X['train'] = np.array(X['train'])
Y['train'] = np.array(Y['train'])

X['test'] = np.array(X['test'])
Y['test'] = np.array(Y['test'])

# PF189345 에러 나면 사진 삭제해주기

#이미지 데이터 크기 정규화 후 vgg16 모델 로딩
X['train'] = X['train'].astype(float) / 255
X['test'] = X['test'].astype(float) / 255

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import tensorflow as tf
from keras import regularizers
from keras import layers, models
from keras.applications import VGG16
from keras import Input
from keras.models import Model
from keras import optimizers, initializers, regularizers, metrics
from keras.callbacks import ModelCheckpoint
import os
from glob import glob
from PIL import Image
import numpy as np

pre_trained_vgg = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
pre_trained_vgg.trainable = False
pre_trained_vgg.summary()

#vgg16 밑에 레이어 추가
additional_model = models.Sequential()
additional_model.add(pre_trained_vgg)
additional_model.add(layers.Flatten())
additional_model.add(layers.Dense(4096, kernel_regularizer = regularizers.l1_l2
                                  (l1=0.001,l2=0.001),activation='relu'))
additional_model.add(layers.Dropout(0.5))
additional_model.add(layers.Dense(2048, kernel_regularizer = regularizers.l1_l2
                                  (l1=0.001,l2=0.001),activation='relu'))
additional_model.add(layers.Dropout(0.5))
additional_model.add(layers.Dense(1024, kernel_regularizer = regularizers.l1_l2
                                  (l1=0.001,l2=0.001),activation='relu'))
additional_model.add(layers.Dropout(0.5))
model.add(Dense(2, activation='sigmoid'))

opt = RMSprop(learning_rate=0.00001)
model.compile(loss='mean_absolute_error', optimizer=opt, metrics=['accuracy'])
model_dir = 'model'
    
if not os.path.exists(model_dir):
  os.mkdir(model_dir)
    
model_path = model_dir + 'multi_img_classification.model'
checkpoint = ModelCheckpoint(filepath=model_path , monitor='val_loss', verbose=1, save_best_only=True)
early_stopping = EarlyStopping(monitor='val_loss', patience=6)

history = model.fit(X['train'], Y['train'], batch_size=3, 
                    steps_per_epoch=40, 
                    shuffle = True,
                    epochs=50, validation_data=(X['test'], Y['test']),callbacks=[checkpoint, early_stopping])

model.save('중소2vgg.h5')

#이미지데이터 모델 성능 평가
print(model.evaluate(X['test'], Y['test']))

"""### xgboost + vgg16 앙상블 데이터 불러오기"""

from google.colab import drive
drive.mount('/content/drive')

pip install tensorflow==2.4.3

pip install keras==2.4.3

import tensorflow as tf
print(tf.__version__)

import keras
print(keras.__version__)

import pandas as pd
import numpy as np
import shutil
import os, glob
from PIL import Image

"""데이터 준비"""

#정형데이터 불러오기

train = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/train_nums2.csv', index_col=0)
test = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/test_nums2.csv', index_col=0)

train = train.dropna(subset=['공연코드'])

y_train = train['레이블']
y_test = test['레이블']
x_train = train.drop(['레이블', '공연코드'], axis=1)
x_test = test.drop(['레이블', '공연코드'], axis=1)

"""### 이미지 불러오기"""

#이미지 데이터 전처리 후 배열로 변환

destination = '/content/drive/MyDrive/KOPIS/posters_all/'

image_w = 224
image_h = 224
pixels = image_h * image_w * 3
X = {'train':[], 'test':[]} #'valid':[]
Y = {'train':[], 'test':[]} #'valid':[]
categories = ['0', '1']

x_list = [x_train, x_test] #x_valid]
y_list = [y_train, y_test] #y_valid]
x_list_str = ['train',  'test'] #valid

for list_str in x_list_str:
  for idx, cls in enumerate(categories):
    label = [0 for i in range(len(categories))]
    label[idx] = 1

    image_dir = destination + list_str +'/' + cls
    files = glob.glob(image_dir+'/*.jpg')
    print(list_str, cls, " 파일 길이 : ", len(files))

    for n, k in enumerate(files):
      files[n] = k.split('/')[-1]
    files = sorted(files)

    for i, f in enumerate(files):
      f = destination + list_str + '/' + cls + '/' + str(f)
      img = Image.open(f)
      img = img.convert("RGB")
      img = img.resize((image_w, image_h))
      data = np.asarray(img)

      X[list_str].append(data)
      Y[list_str].append(label)

  print('ok', len(Y[list_str]))

X['train'] = np.array(X['train'])
Y['train'] = np.array(Y['train'])

X['test'] = np.array(X['test'])
Y['test'] = np.array(Y['test'])

# PF189345 에러 나면 사진 삭제해주기
#X['valid'] = np.array(X['valid'])
#Y['valid'] = np.array(Y['valid'])

#이미지 데이터 크기 정규화 후 vgg16 모델 로딩
X['train'] = X['train'].astype(float) / 255
X['test'] = X['test'].astype(float) / 255

from tensorflow.python.keras.models import load_model
from sklearn.metrics import accuracy_score
import joblib

vgg = load_model('/content/drive/MyDrive/KOPIS/정형데이터/중소2vgg.h5')

vgg_pred = vgg.predict(X['test'])

vgg_pred = np.argmax(vgg_pred, axis=1)
Y['test'] = np.argmax(Y['test'], axis=1)

print('VGG정확도: {0:.4f}'.format(accuracy_score(Y['test'], vgg_pred)))

"""### xgboost 학습"""

#정형데이터 모델 불러와서 xgboost 학습
from xgboost import XGBClassifier

model = XGBClassifier(n_estimators=2000, 
                      seed=1234,
                      max_depth=10,
                      learning_rate=0.0015,
                      num_class = 1)

xgb_model = model.fit(x_train, y_train, early_stopping_rounds=100, 
                      eval_metric='logloss', eval_set=[(x_test, y_test)])

xgboost_pred = model.predict(x_test)
print('XGBOOST 정확도 :',accuracy_score(y_test, xgboost_pred))

"""### vgg16 + xgboost 앙상블"""

from sklearn.metrics import accuracy_score

pred1 = xgb_model.predict_proba(x_test)
pred2 = vgg.predict(X['test'])

print(pred1)
print(' ')
print(pred2)

arr = []
for n in range(len(pred1)):
  rows = []
  for k in range(2):
    m = (pred1[n][k] + pred2[n][k]) / 2
    rows.append(m)
  arr.append(rows)

pred = []
for pr in arr:
  k = np.argmax(pr)
  pred.append(k)

print(arr)
print(' ')

accuracy = accuracy_score(y_test, pred)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

"""### XAI_SHAP 설명가능 인공지능"""

# Commented out IPython magic to ensure Python compatibility.
# 그래프에서 한글표현을 위해 폰트를 설치합니다.
# %config InlineBackend.figure_format = 'retina'

!apt -qq -y install fonts-nanum > /dev/null

# 기본 글꼴 변경
import matplotlib as mpl
mpl.font_manager._rebuild()
mpl.pyplot.rc('font', family='NanumBarunGothic')

import matplotlib.font_manager as fm
fontpath = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
font = fm.FontProperties(fname=fontpath, size=9)

#런타임 재실행해야됨

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

df = pd.read_csv('/content/drive/MyDrive/KOPIS/정형데이터/중소규모_전처리 (1).csv')

df.columns

df.info()

pip install shap

import shap
from sklearn.model_selection import train_test_split

x_train, x_valid, y_train, y_valid = train_test_split(df[['시설특성', '편의시설_레스토랑 여부', '편의시설_카페 여부',
       '편의시설_편의점 여부', '편의시설_놀이방 여부', '편의시설_수유실 여부', '장애인시설_주차장 여부',
       '장애인시설_화장실 여부', '장애인시설_경사로 여부', '장애인시설_전용엘리베이터 여부', '주차시설_자체 여부',
       '주차시설_공영 여부', '좌석수', '장애인석', '무대시설_오케스트라피트 여부', '무대시설_연습실 여부',
       '무대시설_분장실 여부', '소요시간', '공연지역명', 'director', 'actor', 'company', '관람연령',
       '아동공연 여부', '축제 여부', '내한공연 여부', '오픈런 여부', '제작진수', '출연진수', '제작사수',
       '시작-종료일수', '공연일시_요일', '공연일시_시간']], 
                                                      df['레이블'], test_size=0.2, shuffle=True, stratify=df['레이블'], random_state=34)
X_train, X_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=2021)

import xgboost as xgb
from xgboost import plot_importance ## Feature Importance를 불러오기 위함
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from xgboost import plot_importance # 중요변수 시각화
from sklearn.model_selection import train_test_split # train/test
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from sklearn.metrics import confusion_matrix, f1_score, roc_auc_score
import warnings

from xgboost import XGBRegressor, plot_importance
from sklearn.model_selection import train_test_split

model = XGBRegressor()
model.fit(X_train, y_train)

from sklearn.metrics import mean_absolute_error

prediction = model.predict(X_test)

shap.initjs()
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_train)

shap.initjs()
shap.force_plot(explainer.expected_value, shap_values, X_train)

import pandas as pd
import numpy as np

shap.initjs()
# 총 13개 특성의 Shapley value를 절댓값 변환 후 각 특성마다 더함 -> np.argsort()는 작은 순서대로 정렬, 큰 순서대로 정렬하려면
# 앞에 마이너스(-) 기호를 붙임
top_inds = np.argsort(-np.sum(np.abs(shap_values), 0))

# 영향력 top 2 컬럼
for i in range(2):
    shap.dependence_plot(top_inds[i], shap_values, X_train)

shap.summary_plot(shap_values, X_train, plot_type='bar')

shap.summary_plot(shap_values, X_train)

shap_interaction_values = explainer.shap_interaction_values(X_train)
shap.summary_plot(shap_interaction_values, X_train)

import numpy as np

# 모델 예측 결과 시각화
class_names = train_ds.class_names

for images, labels in test_ds:
    predictions = model.predict(images)
    fig, axs = plt.subplots(4, 4, figsize=(12, 12))
    axs = axs.flatten()
    for img, label, pred, ax in zip(images, labels, predictions, axs):
        img = img.numpy().reshape(img_size[0], img_size[1], 3)
        ax.imshow(img)
        if label == 1:
            ax.set_title('Real: ' + class_names[1])
        else:
            ax.set_title('Real: ' + class_names[0])
        if pred > 0.5:
            ax.set_xlabel('Predicted: ' + class_names[1])
        else:
            ax.set_xlabel('Predicted: ' + class_names[0])
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    plt.show()
