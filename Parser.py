
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import re
import os.path
import io
from bs4 import BeautifulSoup


# In[ ]:

text_files = '/Users/home/LiberatingArchives/corpus'


# In[ ]:

all_text = []
for file in os.listdir(text_files):
    if file != '.DS_Store':
        all_text.append(os.path.join(text_files, file))


# In[ ]:

# Global Lists for all Texts
all_titles = []
all_dates = []
all_post_id = []
all_locations = []
all_categories = [] # list within list
all_entry_content = []

# Global Lists for Legislation Texts
bill_number = [] # i.e. AB ###
bill_author = []
bill_party = []
bill_post_id = []
bill_title = []
bill_veto = [] # True = Veto
bill_pdf_link = []

# Global Lists for Appointments
app_post_id = []
app_name = []
app_role = []
app_party = []
app_compensation = []
app_full_descr = []


# In[ ]:

for textFile in all_text: # Change to length of list
    with open(textFile, "r") as f:
        curr_text = f.read()
    #
    all_titles.append(re.findall("""<h1 class=\"[^\"]+\".*?>(.+?)<\/h1>""", curr_text)[0])
    try:
        all_dates.append(re.findall("""Published: <time datetime=\"(.*?)\"""", curr_text)[0])
    except IndexError:
        all_dates.append(np.nan) # Date not specified in text file. There is 1 occurrence.
        
    post_id = re.findall("""<article id=\"post-([\d]+)\"""", curr_text)[0]
    categories = re.findall("""category-([\w-]+)""", curr_text)
    
    all_post_id.append(post_id)
    all_categories.append(categories)
    
    curr1_text = re.findall("""<div class=\"entry-content\">([\s\S]+?)<!-- .et_pb_post -->""", curr_text)
    souped = BeautifulSoup(curr1_text[0], 'html.parser')
    text_parsed = souped.get_text()
    
    all_entry_content.append(text_parsed)
    
    try:
        all_locations.append(re.findall('([A-Z][A-Z| ]+)', text_parsed)[0])
    except IndexError:
        all_locations.append(np.nan)
    
    
    #
    if 'appointments' in categories:
        apps = re.split('\n',text_parsed)[1:-1]
        #print(apps)
        for app in apps:
            #print(app)
            app_post_id.append(post_id)
            try:
                name = re.findall('(^.+?),', app)[0]
                if name[0:16] == 'The compensation':
                    raise IndexError
                app_name.append(name)
            except IndexError:
                app_name.append(np.nan)
            
            try:
                app_party.append(re.findall('Democrat|Republican', app)[0])
            #print(party)
            except IndexError:
                app_party.append(np.nan)
            app_full_descr.append(app)
           
   # elif 'legislation' in categories:
    #    bill_split_veto = souped_bill_entry_content_no_html.split("vetoed")
     #   bills_regex = """(\w+?\s\d+?) by ([\s\S]+?)( | \(([\w\s-]+?)\) )(–|which) ([\s\S]+?)(\.|\n)"""
      #  bills_passed = re.findall(bills_regex, bill_split_veto[0])
       # bills_vetoed = []
       # if len(bill_split_veto) == 2:
        #    bills_vetoed = re.findall(bills_regex, bill_split_veto[1])


# In[ ]:

#all_titles = []
#all_dates = []
#all_post_id = []
#all_locations = []
#all_categories = []  list within list
#all_entry_content = []


# In[ ]:

#app_post_id = []
#app_name = []
#app_role = []
#app_party = []


# In[ ]:

apps_tbl = pd.DataFrame()
apps_tbl['post_id'] = app_post_id
apps_tbl['name'] = app_name
apps_tbl['party'] = app_party
apps_tbl['full_text'] = app_full_descr


# In[ ]:

apps_tbl.dropna(subset = ['name'], inplace = True)
s = apps_tbl.name.str.len().sort_values().index


# In[ ]:

apps_tbl = apps_tbl.reindex(s)
apps_tbl = apps_tbl.iloc[:5640]


# In[ ]:

apps_tbl.sort_values('name')


# In[ ]:

temp = temp[~temp.name.str.contains("NOTE")]
temp = temp[~temp.name.str.contains("Justice")]
temp = temp[~temp.name.str.contains(",")]
temp = temp[~temp.name.str.contains("committee")]
temp = temp[~temp.name.str.contains("moments")]
temp = temp[~temp.name.str.contains("According")]
temp.iloc[5700:]


# In[ ]:

full_tbl = pd.DataFrame()
full_tbl['post_id'] = all_post_id
full_tbl['date'] = all_dates
full_tbl['title'] = all_titles
full_tbl['location'] = all_locations
full_tbl['categories'] = all_categories
full_tbl['entry_content'] = all_entry_content
full_tbl.head()


# In[ ]:

full_tbl['post_id'] = full_tbl['post_id'].apply(int)
full_tbl['date'] = pd.to_datetime(full_tbl['date'])
full_tbl['location'] = full_tbl['location'].str.rstrip()
#full_tbl['entry_content'] = full_tbl['entry_content'].str.replace('\n', '')
full_tbl.head()


# In[ ]:

full_tbl[full_tbl['location'].str.len() < 6]
id_to_alter = [2730, 40696, 684, 2529, 7691, 663, 665, 2754, 1027, 9695, 4071, 9987, 10040, 10193, 1305, 20229, 5923, 6025, 6038, 656, 881, 4668, 657, 3848, 916, 7563, 7568, 7651]
full_tbl.loc[full_tbl['post_id'].isin(id_to_alter),'location'] = [np.nan for _ in id_to_alter]


# In[ ]:

full_tbl.replace({'location': {'CIUDAD DE M': 'CIUDAD DE MEXICO'}}, inplace = True)


# In[ ]:

full_tbl.categories[0]


# In[ ]:

full_tbl['categories'].apply(lambda x: )


# In[ ]:




# In[ ]:

import sqlite3


# In[ ]:

con = sqlite3.connect("database.db")


# In[ ]:

full_tbl.to_sql("all_releases", con, if_exists = "replace")


# In[ ]:




# In[ ]:




# In[ ]:

with open(text_file, "r") as f:
    text = f.read()


# In[ ]:

re.findall("""Published: <time datetime=\"(.*?)\"""", text)


# In[ ]:

entry_raw = re.findall("""<div class=\"entry-content\">([\s\S]+?)###""", text)[0]


# In[ ]:

souped = BeautifulSoup(entry_raw, 'html.parser')


# In[ ]:

text_parsed = souped.get_text()


# In[ ]:

re.findall('([A-Z][A-Z| ]+)', text_parsed)[0]


# In[ ]:

apps = re.split('\n',text_parsed)[1:-1]


# In[ ]:

#grab name
re.findall('(^.+?),', apps[0])[0]


# In[ ]:

#grab party (if empty, nan)
re.findall('Democrat|Republican', apps[3])[0]


# In[ ]:

#grap party, should work for any party 
#jk don't use this one bc of "is registered without party preference" oct 11
re.findall('^\.(.*?[A-Z])', apps[3][::-1])[0][::-1]


# In[ ]:

#grab role, works when role doesn't contain any commas
re.findall('appointed [to the]*(.+?)[,|\.]', apps[0])


# In[ ]:




# In[ ]:



