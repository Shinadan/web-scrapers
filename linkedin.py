# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:01:31 2021

@author: Adegboyega
"""

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import numpy as np
import time

url = 'https://www.linkedin.com/jobs/search/?f_TPR=r86400&geoId=105365761&location=Nigeria&sortBy=R'
#page = requests.get(url)
options = Options()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
driver = webdriver.Chrome(chrome_options = options,executable_path=chromedriver_autoinstaller.install())
driver.get(url)
page = driver.page_source

#parse html with bs
linkedin = bs(page,'html.parser')
jobcontainer = linkedin.find('ul', class_="jobs-search__results-list")

timeouts = np.linspace(1, 5)
timestr = time.strftime("%Y%m%d")
with open('linkedin_'+str(timestr)+'.txt', 'w') as f:
    for jobs in jobcontainer:
        job_title = jobs.find('h3',class_='result-card__title job-result-card__title')
        company = jobs.find('h4', class_='result-card__subtitle job-result-card__subtitle')
        job_loc = jobs.find('span', class_='job-result-card__location')
        job_link = jobs.find('a', {'class':'result-card__full-card-link'})['href']

        print('Title: ', job_title.text,file = f)
        print('Company: ', company.text.strip(),file = f)
        print('Location: ', job_loc.text.strip(),file = f)
        print(job_link,file = f)
        print(' ',file = f)
         
        #random time out
        timeout = np.random.choice(timeouts)
        time.sleep(timeout)
        
driver.quit()