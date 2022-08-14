import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tagging
#A lot of boiler plate imports.

links = []
orgs = dict()
#defining driver
options = webdriver.ChromeOptions()
s = Service('/home/juggernautjha/Desktop/Pclub-Scraping/chromedriver')
driver = webdriver.Chrome(service = s, options = options)

#fetching url
driver.get('https://summerofcode.withgoogle.com/programs/2022/organizations')
time.sleep(20) #20 is very arbitrary. It just sounds good. 

#utility function
next_xpath = '/html/body/app-root/app-layout/mat-sidenav-container/mat-sidenav-content[1]/div/div/main/app-program-organizations/app-orgs-grid/section[2]/div/div[2]/mat-paginator/div/div/div[2]/button[2]'

def go_next():
    next = driver.find_elements(By.XPATH , next_xpath)
    next[-1].click()

#populating links
for i in range(4):
    a = driver.find_elements(By.CSS_SELECTOR, 'a.content')
    for i in a:
        links.append(i.get_attribute("href"))
    go_next()
    time.sleep(1)

#scraping detaails
for link in links:
    print(link)
    
    driver.get(link)
    time.sleep(6)
    
    temp = dict()
    name = driver.find_element(By.CSS_SELECTOR, 'span.title')
    desc = driver.find_elements(By.CSS_SELECTOR, 'div.constrainer--line-length')[1]
    tech_stack = driver.find_element(By.CSS_SELECTOR, 'div.tech__content')
    topics = driver.find_element(By.CSS_SELECTOR, 'div.topics__content')
    prose = driver.find_element(By.CSS_SELECTOR, 'div.bd')
    url = driver.find_element(By.CSS_SELECTOR, 'a.link')
    
    temp['desc'] = desc.text
    temp['tech_stack'] = tech_stack.text.split(',')
    temp['topics'] = topics.text.split(',')
    temp['detail'] = prose.text
    temp['url'] = url.text
    temp['tags'] = []
    try:
        twitter = driver.find_element(By.CSS_SELECTOR, 'body > app-root > app-layout > mat-sidenav-container > mat-sidenav-content.mat-drawer-content.mat-sidenav-content.site__main.theme.theme--gray.ng-star-inserted > div > div > main > app-program-organization > app-org-info > section > div.section__inner > div > div > div.grid__row__item.grid__row__item--span3\@md > app-org-info-contact-card > app-card > div > div > ul > li:nth-child(3) > a')
        discord = driver.find_element(By.CSS_SELECTOR, 'body > app-root > app-layout > mat-sidenav-container > mat-sidenav-content.mat-drawer-content.mat-sidenav-content.site__main.theme.theme--gray.ng-star-inserted > div > div > main > app-program-organization > app-org-info > section > div.section__inner > div > div > div.grid__row__item.grid__row__item--span3\@md > app-org-info-contact-card > app-card > div > div > ul > li:nth-child(2) > a')
        temp['discord'] = discord.get_attribute('href')
        temp['twitter'] = twitter.get_attribute('href')
    except:
        temp['discord'] = 'NA'
        temp['twitter'] = 'NA'
    orgs[name.text] = temp
    # print(name.text, links.index(link)+1)

#dumping json
file = open("orgs.json", "w")
json.dump(orgs, file, indent=4)
file.close()


'''
Getting tags, however, requires a bit of law-breaking.
Google uses an API to get json that populates the page. By making a request to that API, we can essentially circumvent the whole scraping process. 
That sounds illegal given the name of the task. But I want my brownie points.
'''
import sys
try:
    if sys.argv[1] == "tag":
        print("You've choosen tagging")
        tagging.tag()
except:
    pass
