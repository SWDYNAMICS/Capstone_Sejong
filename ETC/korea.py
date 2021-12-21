import bs4
from selenium import webdriver
import time,os,sys,math
from bs4 import BeautifulSoup 
import random
import pandas as pd

#멀티 텍스트와 번호의 조합으로 입력받는 방법도 있음.
query_txt = input("지역을 입력하세요:")
save_txt = "c:/py_temp/"+query_txt+" save_text.txt"
driver = webdriver.Chrome("c:/py_temp/chromedriver.exe")
driver.get("https://korean.visitkorea.or.kr")
driver.maximize_window()

driver.find_element_by_id('btnMenu').click()
driver.find_element_by_link_text('인기').click()
driver.find_element_by_link_text(query_txt).click()

time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

content = soup.find('ul','list_thumType flnon').find_all('li')

for i in content :
    print(i.get_text().replace("\n","").strip())

# 데이터 저장하기
orig_stdout = sys.stdout
file = open(save_txt , 'a' , encoding='UTF-8')
sys.stdout = file  

for i in content :
    print(i.get_text().replace("\n",""))

file.close()    
sys.stdout = orig_stdout  #원래대로 변경   

print('요청하신 데이터 수집 작업이 정상적으로 완료되었습니다')
print(f'수집된 결과는 {save_txt} 에 저장되었습니다' )    


# 크롬브라우저 종료
time.sleep(5)
driver.close()
