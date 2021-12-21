from bs4 import BeautifulSoup
from selenium import webdriver
import time, sys, os

# 사용자에게 검색어 키워드를 입력 받습니다.
query_area = input('''
 1.서울      2.인천      3.대전      4.대구      5.광주      6.부산      7.울산
 8.세종      31.경기     32.강원     33.충북     34.충남     35.경북     36.경남
37.전북     38.전남     39.제주     

1.위 지역 중 조회하고 싶은 지역의 번호를 입력해 주세요:   ''')

save_txt = "c:/py_temp/" + query_area + ".txt"


# 크롬 드라이버를 사용해서 웹 브라우저를 실행합니다.
driver = webdriver.Chrome("c:/py_temp/chromedriver.exe")
driver.get('https://korean.visitkorea.or.kr/list/ms_list.do?areacode='+query_area)
driver.set_window_size(1600,1000)

time.sleep(2)
# driver.find_element_by_id('btnMenu').click()
# driver.find_element_by_link_text('인기').click()

# 보이는 메뉴를 선택
# time.sleep(2)
# driver.find_element_by_link_text(query_area).click()


# 데이터 수집하기
time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
content = soup.find('ul', 'list_thumType flnon').find_all('li')

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
