# 관련 모듈 사용선언
import bs4
from selenium import webdriver
import time,os,sys,math
from bs4 import BeautifulSoup 
import random
import pandas as pd


query_txt = input("검색어는?:")
save_txt = "c:/py_temp/"+query_txt+" save_text.txt"
save_csv = "c:/py_temp/"+query_txt+" save_text.csv"
save_xls = "c:/py_temp/"+query_txt+" save_text.xls"

driver = webdriver.Chrome("c:/py_temp/chromedriver.exe")
driver.get("http://www.riss.kr")
time.sleep(random.randrange(1,3))
driver.maximize_window() # 창 최대화
# driver.set_window_size(900,800)


# 팝업창이 몇개인지 모르는 경우 모두 닫기
b_win = len(driver.window_handles)

for i in range(b_win):
    if i != 0:
        driver.switch_to_window(driver.window_handles[i])
        driver.close()
    else:
        driver.switch_to_window(driver.window_handles[0])
        #main 창임


driver.find_element_by_id('query').send_keys(query_txt)
driver.find_element_by_class_name('btnSearch').click()
driver.find_element_by_link_text('학위논문').click()
# driver.find_element_by_xpath('//*[@id="tabMenu"]/div/ul/li[3]/a/span').click()

# 페이지 정보 정보 수집하기
html = driver.page_source                #원본
soup = BeautifulSoup(html,'html.parser') #분석본

# content_1 = soup.find('div','srchResultListW').find_all('li')

# def content_print() :
#     for i in content_1 :
#         print(i.get_text().replace('\n', "").strip())
#         print('\n')

# content_print()


# 검색 건수 입력받고 데이터 수집
total_cnt = soup.find('div','searchBox pd').find('span','num').get_text()
print('키워드 %s (으)로 총 %s 건 검색' %(query_txt,total_cnt))

collect_cnt = int(input("몇 건을 수집할까요?: "))
collect_page_cnt = math.ceil(collect_cnt/10)
print("%s 건 수집을 위해 %s 페이지를 조회합니다."%(collect_cnt,collect_page_cnt))


# file = open(save_txt , 'a' , encoding='UTF-8')
# sys.stdout = file  
# content_print()
# file.close()

# sys.stdout = orig_stdout








# 항목별로 수집하기 위한 pandas 데이터프레임 생성
no2 = []
title2 = []
writer2 = []
org2 = []

no = 1 # 변수 초기화


# 페이지를 탐색하며 데이터 수집
page_no = []

for a in range(1, collect_page_cnt + 1): #마지막 페이지까지
    
    html_2 = driver.page_source #매 페이지마다
    soup_2 = BeautifulSoup(html_2,'html.parser')

    content_2 = soup_2.find('div','srchResultListW').find_all('li')

    for b in content_2:
        try:
            title = b.find('div','cont').find('p','title').get_text()
        except:
            continue
        else:
            f = open(save_txt,'a',encoding='UTF-8')
            print('1.번호: ',no)
            no2.append(no)
            f.write('\n' + '1.번호: '+ str(no)) #텍스트 형식으로 바꿔야함

            print('2.논문제목: ',title)
            title2.append(title)
            f.write('\n' + '2.논문제목: '+ title) #텍스트 형식으로 바꿔야함

            writer = b.find('span','writer').get_text() 
            print('3.저자: ',writer)
            writer2.append(writer)
            f.write('\n' + '3.저자: '+ writer) #텍스트 형식으로 바꿔야함

            org = b.find('span','assigned').get_text()
            print('4.소속기관: ',org)
            org2.append(org)
            f.write('\n' + '4.소속기관: '+ org + '\n') #텍스트 형식으로 바꿔야함
        
        f.close()

        no += 1
        print('\n')

        if no > collect_cnt:
            break

        time.sleep(1)

    a += 1

    try:
        driver.find_element_by_link_text('%s' %a).click()
    except:
        driver.find_element_by_link_text('다음 페이지로').click()

# 데이터 프레임 생성
df = pd.DataFrame()
df['번호']=no2
df['제목']=pd.Series(title2)
df['저자']=pd.Series(writer2)
df['소속(발행)기관']=pd.Series(org2)

# xls 형태로 저장하기
df.to_excel(save_xls,index=False, encoding="utf-8")

# csv 형태로 저장하기
df.to_csv(save_csv,index=False, encoding="utf-8-sig")
print('요청하신 데이터 수집 작업이 정상적으로 완료되었습니다')


# 수집 데이터를 csv, xls로 저장하기

time.sleep(5)
driver.close()
