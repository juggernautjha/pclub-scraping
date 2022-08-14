#Running scraping.py multiple times isn't really a viable option considering that 
#each iteration takes ~5 seconds

#boilerplate imports
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
#A lot of boiler plate imports.

import sys
try:
    if sys.argv[1] == "tag":
        print("You've choosen tagging")
except:
    pass
def tag():
    f = open('orgs.json', 'r')
    orgs = json.load(f)
    f.close()
    url = 'https://summerofcode.withgoogle.com/api/program/2022/organizations/'

    '''
    Fun fact: It turns out that Google (obviously) uses API. And I found out the URL.
    Sometimes my genius and/or laziness scares me.
    '''

    r = requests.get(url)
    dic  = r.text
    dic = json.loads(dic)
    for i in dic:
        name = i["name"]
        # print(name)
        # print(i['categories'])
        orgs[name]["tags"] = i['categories']

    f = open('orgs.json', 'w')
    orgs = json.dump(orgs, f, indent = 4)
    f.close()