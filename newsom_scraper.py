#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import urllib
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import re
import numpy as np
import logging


# In[2]:


path_to_driver = '/Users/home/LiberatingArchives/chromedriver'
prs = webdriver.Chrome(path_to_driver)


# In[3]:


home = 'https://www.gov.ca.gov/category/all/'
prs.get(home)


# In[4]:


arch = prs.find_element_by_id('archives-2')


# In[5]:


months = arch.find_elements_by_tag_name('li')


# In[10]:


logging.basicConfig(format = '%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='newsom.log',level=logging.DEBUG)

logging.info('######## Begin crawl ########')


# In[11]:


month_links = [m.find_element_by_tag_name('a').get_attribute('href') for m in months]


# In[12]:


save_path = '/Users/zanekuser/Desktop/Professional/Goodly Labs/LiberatingArchives/newsom_corpus2'
counter = 0
for month in month_links[:1]:
    logging.info('url: ######## '+month+' ########')
    print(month)
    prs.get(month)
    sleep(0.5)
    while True:
        main = prs.find_element_by_class_name('main-primary')
        links = main.find_elements_by_class_name('btn')
        num_links = len(links)
        for i in range(num_links):
            link = links[i].get_attribute('href')
            r = requests.get(link)
            file_name = 'newsom' + str(counter)
            counter += 1
            full_path = os.path.join(save_path, file_name + ".txt")
            file = open(full_path,'wb')
            file.write(r.content)
            file.close()
            sleep(.5)
        
        more = main.find_element_by_class_name('pagination')
        left = more.find_element_by_class_name('alignleft')
        try:
            more_link = False
            more_link = left.find_element_by_tag_name('a').get_attribute('href')
        except:
            break
        if more_link:
            logging.info('url: ######## '+month+' ########')
            print(more_link)
            prs.get(more_link)
    sleep(1)
logging.info('######## download complete ########') 
prs.quit()


# In[ ]:




