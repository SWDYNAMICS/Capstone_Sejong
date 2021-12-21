from selenium import webdriver
import os, time, sys
from bs4 import BeautifulSoup as bs

driver = webdriver.Chrome("c:/py_temp/chromedriver.exe")
driver.get('http://www.riss.kr')
query_txt = '로봇'
time.sleep(2)

driver.find_element_by_id('query').send_keys(query_txt + '\n')
driver.find_element_by_link_text('국내학술논문').click()

# page analysis

html = driver.page_source
soup = bs(html,'html.parser')

content_1 = soup.find('div',class_='srchResultListW').find_all('li')

# for i in content_1:
#     print(i.get_text())
print(content_1[1].get_text())

driver.close()