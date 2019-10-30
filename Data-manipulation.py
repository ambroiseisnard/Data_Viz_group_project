#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Set Up 
import pandas as pd
import numpy as np
import wget
import sh
import simplejson as json


# In[2]:


# Download the data
wget.download("http://deepyeti.ucsd.edu/jianmo/amazon/categoryFiles/Musical_Instruments.json.gz")
wget.download("http://deepyeti.ucsd.edu/jianmo/amazon/metaFiles/meta_Musical_Instruments.json.gz")


# In[3]:


# Unzip 
sh.gunzip("Musical_Instruments.json.gz")
sh.gunzip("meta_Musical_Instruments.json.gz")


# In[4]:


# Normalize the data to create a .csv file
F1 = "Musical_Instruments.json"
DF1 = pd.io.json.json_normalize([json.loads(line) for line in open(F1)]))

F2 = "meta_Musical_Instruments.json"
DF2 = pd.io.json.json_normalize([json.loads(line) for line in open(F2)])


# In[5]:


# Create the .csv file 
DF1.to_csv("Musical_Instruments.csv", index=False)
DF2.to_csv("meta_Musical_Instruments.csv", index=False)


# In[56]:


# Reading the .csv file with pandas 
DF1 = pd.read_csv("Musical_Instruments.csv")
DF2 = pd.read_csv("meta_Musical_Instruments.csv")


# In[57]:


# Merging the review data and meta data on 'asin'
DF3 = pd.merge(DF1, DF2, how='inner', left_on='asin', right_on='asin')


# In[58]:


# Slicing the significant columns
DF4 = DF3.loc[:, ['overall','verified', 'reviewTime', 'asin', 'summary', 'unixReviewTime', 'title', 'brand', 'rank', 'price', 'description']]


# In[59]:


# Converting the price column from string to float
DF4 = DF4.dropna(subset = ['price']) # Drop the rows containing NaN values for price 
DF4 = DF4[~DF4['price'].str.contains('-')] # Drop the rows containing "-" values for price (e.g: "123 - 158")
DF4['price'] = DF4['price'].str.replace(',', '') # Deleting "," for price (e.g: "$1,538.34")
DF4['price'] = DF4['price'].str.replace('$', '').astype(float) # Deleting "$" for price (e.g: " $1538.34")


# In[60]:


# Loc the rows with price above $100
DF4 = DF4.loc[(DF4['price'] > 100), :]


# In[61]:


DF4[['verified']] = DF4[['verified']].astype(str) 


# In[62]:


# Drop all rows containing False in 'verified'
DF4 = DF4[~DF4['verified'].str.contains('False')] 


# In[63]:


DF4.head()['reviewTime']


# In[71]:


# add a time stamp 
DF4.loc[:, "timestamp"] = pd.to_datetime(DF4["reviewTime"],format="%m %d, %Y")


# In[65]:


DF4.head()[["reviewTime", "timestamp"]]


# In[73]:


# create new columns for year, month and day
DF4.loc[:, "review_year"] = DF4["timestamp"].dt.year
DF4.loc[:, "review_month"] = DF4["timestamp"].dt.month
DF4.loc[:, "review_day"] = DF4["timestamp"].dt.day


# In[75]:


# set timestamp as index
DF4.set_index("timestamp", inplace=True)


# In[85]:


DF4.head().T


# In[ ]:
print('ambroise has a tiny penis')




a = "so funny Felix"

l = 'hello world'

Ambroise = 1+1
