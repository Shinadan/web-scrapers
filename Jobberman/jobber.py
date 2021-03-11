#import required packages
import requests
from bs4 import BeautifulSoup as bs
import time
from datetime import date
import numpy as np 

headers = {'user-agent': 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
           }
#define url list
base_url = 'https://www.jobberman.com/jobs'
url_list = ['{}?page={}'.format(base_url,str(page)) for page in range(1,5)]

timeouts = np.arange(1, 5)
with open('jobber.txt', 'w') as f:
    print(date.today().strftime("%b %d, %Y"), file = f)
    for url in url_list:
        page = requests.get(url, headers=headers)
        
        #parse html with bs4
        jobberman = bs(page.content, 'html.parser')
        jobcontainer = jobberman.find('div',class_= 'search-main__content')
        job_container = jobcontainer.find_all('article',class_='search-result')

        for jobs in job_container:
            try:
                job_title = jobs.find('h3')
                company = jobs.find('div', class_='if-content-panel padding-lr-20 flex-direction-top-to-bottom--under-lg align--start--under-lg search-result__job-meta')
                job_loc = jobs.find('div', class_='search-result__location')
                salary = jobs.find('div', class_='search-result__job-salary')
                job_func = jobs.find('div', class_="if-wrapper-row").find('span',class_='padding-lr-10 gutter-flush-under-lg')
                job_link = jobs.find('div', class_='flex--3 wrapper--inline-flex align--center direction--row').find('a')['href']
                
                #print to jobber.txt file
                print('Title: ', job_title.text.title(), file = f)
                print('Company: ', company.text.strip().title(), file = f)
                print('Location: ', job_loc.text.strip(), file = f)
                print('Job Function: ', job_func.get_text().strip(), file = f)
                print('Salary: ', ' '.join((salary.text.split())[1:]), file = f)
                print(job_link, file = f)
                print(' ', file = f)
                
                #random time out
                timeout = np.random.choice(timeouts)
                time.sleep(timeout)
                
                
            except AttributeError:
                continue