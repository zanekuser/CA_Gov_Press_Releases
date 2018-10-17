
# coding: utf-8

# In[11]:


import os
import urllib
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from settings import *


# In[12]:


path_to_driver = PATH_TO_DRIVER
prs = webdriver.Chrome(path_to_driver)


# In[13]:


prs.get('https://www.gov.ca.gov/all-press-releases/')


# In[15]:


links = prs.find_elements_by_class_name("more-link")
save_path = SAVE_PATH
num_links = len(links)
for i in range(num_links):
    link = links[i].get_attribute('href')
    r = requests.get(link)
    file_name = 'release' + str(num_links - i)
    full_path = os.path.join(save_path, file_name + ".txt")
    file = open(full_path,'wb')
    file.write(r.content)
    file.close()
    sleep(.5)
prs.quit()

