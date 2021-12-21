#################################################################################################################
## 파이썬 실무 활용 능력 실기 시험 과제용 소스코드
## 시험 응시생은 아래 코드 30번 행의 Chrome Driver 경로를 올바르게 수정한 후
## 아래 코드 73번 행의 빈 곳의 코드를 올바르게 완성하고
## 아래 코드 106 , 110 행의 빈곳을 완성한 후 이 소스코드와 결과가 저장된 2가지 파일(csv , xls 파일)을 
## 한국정보인재개발원 홈페이지에 제출하세요.
#################################################################################################################
print("=" *80)
print(" 파이썬 활용능력 1급 실기 시험 문제 ")
print(" 네이버 블로그 정보 수집 후 xls , csv 형식으로 저장하기")
print("=" *80)

#Step 0. 필요한 모듈과 라이브러리를 로딩하고 검색어를 입력 받습니다

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys       
import math
import pandas  as pd    

query_txt = "겨울여행"
cnt=30
page_cnt = math.ceil(cnt / 10)

fc_name='c:/py_temp/2107-00069-이승우.csv'
fx_name='c:/py_temp/2107-00069-이승우.xls'

#Step 1. 크롬 드라이버를 사용해서 웹 브라우저를 실행합니다.
path = "c:/py_temp/chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get('http://www.naver.com')
time.sleep(2)

#Step 2. 네이버 검색창에 입력 받은 검색어를 넣고 검색한 후 "View" -> "블로그" 선택
element = driver.find_element_by_id("query")
element.send_keys(query_txt)
element.submit()

driver.find_element_by_link_text("VIEW").click()
time.sleep(2)

driver.find_element_by_link_text("블로그").click()

# Step 3. 저장 목록을 만든 후 목록에 있는 내용을 파일에 저장하기

no2 = [ ]           # 게시글 번호 컬럼
title2 = [ ]        # 게시물 제목 컬럼
contents2 = [ ]     # 게시글 내용 컬럼
bdate2 = [ ]        # 작성 일자 컬럼
nick2 = [ ]         # 블로그 닉네임

no = 1

# 자동 스크롤다운 함수
def scroll_down(driver):
  driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
  time.sleep(5)

i = 1
while (i <= page_cnt):
      scroll_down(driver) 
      i += 1
    

print("\n")

# Step 4. 항목별 내용 추출하기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

view_list = soup.find('div','_more_contents_event_base').find_all('li') # 이곳은 검색된 블로그 글들의 목록을 추출하는 부분입니다.

for i in view_list :
    
    no2.append(no)                            # 게시물 번호 리스트에 추가
    print('1.번호:',no)

    all_title = i.find('a','api_txt_lines total_tit')
    title = all_title.get_text( )          # 게시물 제목
    title2.append(title)                      # 게시물 제목 리스트에 추가
    print('2.제목:',title)

    contents = i.find('div' , 'api_txt_lines dsc_txt').get_text( )   # 게시물 내용
    contents2.append(contents)                # 게시물 내용 리스트에 추가
    print('3.내용:',contents)

    bdate = i.find('span','sub_time sub_txt').get_text( )  # 작성일자
    bdate2.append(bdate)                     # 작성일자 리스트에 추가
    print('4.작성일자:',bdate)

    print("\n")
    
    if no == 30:
      break

    no += 1

#Step 5. 출력 결과를 표(데이터 프레임) 형태로 만들어 파일로 저장하기

naver_blog = pd.DataFrame()
naver_blog['번호'] = no2
naver_blog['제목'] = title2
naver_blog['내용'] = contents2
naver_blog['작성일자'] = bdate2

# csv 형태로 저장하기
naver_blog.to_csv(fc_name,index=False,encoding="utf-8-sig")
print(" csv 파일 저장 경로: %s" %fc_name) 

# 엑셀 형태로 저장하기
naver_blog.to_excel(fx_name,index=False, encoding="utf-8")
print(" xls 파일 저장 경로: %s" %fx_name) 

