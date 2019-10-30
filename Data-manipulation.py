#!/usr/bin/env python
# coding: utf-8

# Set Up 
import pandas as pd
import numpy as np
import wget
import sh
import simplejson as json


# Download the data
wget.download("http://deepyeti.ucsd.edu/jianmo/amazon/categoryFiles/Musical_Instruments.json.gz")
wget.download("http://deepyeti.ucsd.edu/jianmo/amazon/metaFiles/meta_Musical_Instruments.json.gz")

# Unzip 
sh.gunzip("Musical_Instruments.json.gz")
sh.gunzip("meta_Musical_Instruments.json.gz")

# Normalize the data to create a .csv file
F1 = "Musical_Instruments.json"
DF1 = pd.io.json.json_normalize([json.loads(line) for line in open(F1)])))))))))))))))

F2 = "meta_Musical_Instruments.json"
DF2 = pd.io.json.json_normalize([json.loads(line) for line in open(F2)])

# Create the .csv file 
DF1.to_csv("Musical_Instruments.csv", index=False)
DF2.to_csv("meta_Musical_Instruments.csv", index=False)

# Reading the .csv file with pandas 
DF1 = pd.read_csv("Musical_Instruments.csv")
DF2 = pd.read_csv("meta_Musical_Instruments.csv")

# Merging the review data and meta data on 'asin'
DF3 = pd.merge(DF1, DF2, how='inner', left_on='asin', right_on='asin')

# Slicing the significant columns
DF4 = DF3.loc[:, ['overall','verified', 'reviewTime', 'asin', 'summary', 'unixReviewTime', 'title', 'brand', 'rank', 'price', 'description']]

# Converting the price column from string to float
DF4 = DF4.dropna(subset = ['price']) # Drop the rows containing NaN values for price 
DF4 = DF4[~DF4['price'].str.contains('-')] # Drop the rows containing "-" values for price (e.g: "123 - 158")
DF4['price'] = DF4['price'].str.replace(',', '') # Deleting "," for price (e.g: "$1,538.34")
DF4['price'] = DF4['price'].str.replace('$', '').astype(float) # Deleting "$" for price (e.g: " $1538.34")

# Loc the rows with price above $100
DF4 = DF4.loc[(DF4['price'] > 100), :]

DF4[['verified']] = DF4[['verified']].astype(str) 

# Drop all rows containing False in 'verified'
DF4 = DF4[~DF4['verified'].str.contains('False')] 

DF4.head()['reviewTime']

# add a time stamp 
DF4.loc[:, "timestamp"] = pd.to_datetime(DF4["reviewTime"],format="%m %d, %Y")

DF4.head()[["reviewTime", "timestamp"]]

# create new columns for year, month and day
DF4.loc[:, "review_year"] = DF4["timestamp"].dt.year
DF4.loc[:, "review_month"] = DF4["timestamp"].dt.month
DF4.loc[:, "review_day"] = DF4["timestamp"].dt.day

# set timestamp as index
DF4.set_index("timestamp", inplace=True)

DF4.head().T



l = 'hello world'


