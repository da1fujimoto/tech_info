
# coding: utf-8

# In[5]:


import pymongo
from pymongo import MongoClient
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[6]:


plt.style.use('ggplot')


# In[8]:


datetime.datetime.now()


# In[16]:


datetime.datetime(2018,5,1) + datetime.timedelta(days=100)


# In[20]:


rent_dict_tbl = [
    {'state': '貸出中', 'device': 'J-Link-UBUNTU_No2', 'user_email': 'shugo.omoto@sample.com', 'rent_date': datetime.datetime(2018,2,19), 'return_date': datetime.datetime(2018,2,19) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'J-Link-UBUNTU_No4', 'user_email': 'masakazu.nakamoto@sample.com', 'rent_date': datetime.datetime(2018,2,19), 'return_date': datetime.datetime(2018,2,19) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'J-Link-UBUNTU_No1', 'user_email': 'koji.tanomoto@sample.com', 'rent_date': datetime.datetime(2018,2,26), 'return_date': datetime.datetime(2018,2,26) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'XX946_No694', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,2,27), 'return_date': datetime.datetime(2018,2,27) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'XX946_No697', 'user_email': 'shugo.omoto@sample.com', 'rent_date': datetime.datetime(2018,3,1), 'return_date': datetime.datetime(2018,3,1) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'USB_Memory_WIN_4', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,3,6), 'return_date': datetime.datetime(2018,3,6) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'USB_Memory_WIN_3', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,3,6), 'return_date': datetime.datetime(2018,3,6) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'USB_Memory_WIN_2', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,3,6), 'return_date': datetime.datetime(2018,3,6) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'USB_Memory_WIN_1', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,3,6), 'return_date': datetime.datetime(2018,3,6) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'USB_Memory_WIN_5', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,3,6), 'return_date': datetime.datetime(2018,3,6) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'J-Link-UBUNTU_No6', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,3,26), 'return_date': datetime.datetime(2018,3,26) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'XX969_No729', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,3,26), 'return_date': datetime.datetime(2018,3,26) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'XX970_No742', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,3,27), 'return_date': datetime.datetime(2018,3,27) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'XX984_No757', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,4,5), 'return_date': datetime.datetime(2018,4,5) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'XX970_No741', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,4,5), 'return_date': datetime.datetime(2018,4,5) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'J-Link-UBUNTU_No5', 'user_email': 'kengo.hirata@sample.com', 'rent_date': datetime.datetime(2018,4,6), 'return_date': datetime.datetime(2018,4,6) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'J-Link-UBUNTU_No3', 'user_email': 'masakazu.nakamoto@sample.com', 'rent_date': datetime.datetime(2018,4,9), 'return_date': datetime.datetime(2018,4,9) + datetime.timedelta(days=7)},
    {'state': '貸出中', 'device': 'XX969_No723', 'user_email': 'masakazu.nakamoto@sample.com', 'rent_date': datetime.datetime(2018,4,9), 'return_date': datetime.datetime(2018,4,9) + datetime.timedelta(days=7)},
]


# In[21]:


df = pd.DataFrame(rent_dict_tbl)


# In[22]:


df.head()


# In[24]:


df.iloc[0].to_dict()


# In[25]:


client = MongoClient('10.10.252.62', 27017)
db = client.rent_test_db
collection = db.rent_test_collection


# In[26]:


for i in range(len(df)):
    collection.insert_one(df.iloc[i].to_dict())


# In[28]:


next(collection.find({}))


# In[29]:


client.close()

