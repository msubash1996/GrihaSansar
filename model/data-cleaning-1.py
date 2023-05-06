#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 21:13:40 2021

@author: overlord
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# Extracting features from json encoded features --------

# Parse json with single quotes
def _json(s):
    return ast.literal_eval(s)

df = pd.read_csv("data.csv")

df["title"] = df["basic"].apply(lambda x: _json(x)["title"])

# Building details
df["building"] = df["building"].apply(lambda x: _json(x))
df["built_year"] = df["building"].apply(lambda x: x["built_year"] if x["built_year"]!=0 else np.nan)
df["floors"] = df["building"].apply(lambda x: x["total_floor"])
df["bedroom"] = df["building"].apply(lambda x: x["no_of"]["bedroom"])
df["bathroom"] = df["building"].apply(lambda x: x["no_of"]["bathroom"])

# Prices from json data
df["price"] = df["price"].apply(lambda x: _json(x))
df["is_price_on_call"] = df["price"].apply(lambda x: x["is_price_on_call"] if "is_price_on_call" in x.keys() else np.nan)
df["amount"] = df["price"].apply(lambda x: x["value"])
df["price_type"] = df["price"].apply(lambda x: x["label"]["title"])

# Area road and property face
df["location_property"] = df["location_property"].apply(lambda x: _json(x))
df["total_area"] = df["location_property"].apply(lambda x: x["total_area"] if x["total_area"] else np.nan)
df["total_area_unit"] = df["location_property"].apply(lambda x: x["total_area_unit"]["title"])
df["road_access"] = df["location_property"].apply(lambda x: x["road_access_value"])
df["road_access_unit"] = df["location_property"].apply(lambda x: x["road_access_length_unit"]["title"])
df["property_face"] = df["location_property"].apply(lambda x: x["property_face"]["title"] if "property_face" in x.keys() else np.nan)

# Address
#{'state_id': {'name': 'Bagmati State'}, 'district_id': {'name': 'Kathmandu'}, 'city_id': {'name': 'Budhanilkantha Municipality'}, 'area_id': {'name': 'Budhanilkantha'}, 'house_no': ''}
df["address"] = df["address"].apply(lambda x: _json(x))
df["state"] = df["address"].apply(lambda x: x["state_id"]["name"] if "state_id" in x.keys() else np.nan)
df["district"] = df["address"].apply(lambda x: x["district_id"]["name"] if "district_id" in x.keys() else np.nan)
df["city"] = df["address"].apply(lambda x: x["city_id"]["name"] if "city_id" in x.keys() else np.nan)
df["area"] = df["address"].apply(lambda x: x["area_id"]["name"] if "area_id" in x.keys() else np.nan)

df.drop(["Unnamed: 0","_id","basic","building","price","prefix","is_project","road_access_unit","is_negotiable","location_property","media","project_property_type","added_at","added_by","property_id","address","agency_id"],axis=1,inplace=True)

df.columns

# CLEANING ------------

# Built year
df["built_year"].unique()

# Floors
df["floors"].unique()

df[df["floors"]==0]
df["floors"] = df["floors"].apply(lambda x: x if x !=0 else np.nan)

# Bedroom
df["bedroom"].unique()

df[df["bedroom"]==0]
df["bedroom"] = df["bedroom"].apply(lambda x: x if x !=0 else np.nan)

# Bathroom
df["bathroom"].unique()
d=df[df["bathroom"]==0]
df["bathroom"] = df["bathroom"].apply(lambda x: x if x !=0 else np.nan)

# Is price on call
df["is_price_on_call"].unique()


# Total Area
df.total_area.unique()

    # One data point was 3 where I hand edited to 48 aanas according to website
df.loc[df['total_area'] == '3', 'total_area'] = "0-48-0-0"

def clean_total_area(row):
   
    total_area = str(row["total_area"]).strip()
    splitted = total_area.split("-")
    
    if (row["total_area_unit"] == 'Sq. Feet' and len(splitted) == 1) or total_area == "nan":
        return row["total_area"]
    
    if ( len(splitted) == 4 or len(splitted) == 5 ):
        sq_feet = 0
        start_index = 0
        
        measure_to_sq_feet = [5476, 342.25, 85.56, 21.39]
            
        if len(splitted) == 5:
            start_index = 1
            
        # Ropani or Bighar
        sq_feet+= float(splitted[start_index+0]) * measure_to_sq_feet[0]
        # Aana or Kattha
        sq_feet+= float(splitted[start_index+1]) * measure_to_sq_feet[1]
        # Paisa or Dhur
        if splitted[start_index+2]:
            sq_feet+= float(splitted[start_index+2]) * measure_to_sq_feet[2]
        # Dam or Haat
        sq_feet+= float(splitted[start_index+3]) * measure_to_sq_feet[3]
        
        return sq_feet
    return row["total_area"]

df["area_sq_ft"] = df.apply(clean_total_area,axis=1)

df["area_sq_ft"].unique()

df["area_sq_ft"] = pd.to_numeric(df["area_sq_ft"] , errors='coerce')

# Total Area Unit
df.total_area_unit.unique()
df.loc[df.total_area_unit == 'Bigha-Kattha-Dhur-Haat',"total_area_unit"] = 'Ropani-Aana-Paisa-Daam'

# Road Access
df.road_access.unique()

d = df[df.road_access=="0"]

def clean_road_access(road_access):
    road_access = str(road_access).replace("+","")
    split_on = ["-","&","/"]
    for split in split_on: 
        s = road_access.split(split)
        if len(s) == 2:
            return (float(s[0]) + float(s[1]))/2
        elif len(s) == 3:
            return float(s[1])
    return road_access

df["road_access"] = df["road_access"].apply(clean_road_access)
df["road_access"] = pd.to_numeric(df["road_access"] , errors='coerce')
df.road_access = df.road_access.apply(lambda x: np.nan if x==0 else x)

# Property Face
df.property_face.unique()

df[df.property_face == "-"]
df.property_face = df.property_face.apply(lambda x: x if x!="-" else np.nan)

# State
df.state.unique()

# District
df.district.unique()

# City 
df.city.unique()

# Area
df.area.unique()

# Amount
df["amount"].unique()

df.groupby("price_type").count().iloc[:,0]

d = df[df.price_type == "Per Aana"]
d = df[df.price_type == "Per Month"]

 # One typo in per month (hand fixed) .. and others were rental homes which we dont require

df = df[df.price_type != "Per Month"]


def clean_price(row):
    
    if row["price_type"] == "Per Aana":
        aana = row["area_sq_ft"] / 342.25
        
        return aana * row["amount"]
    return row["amount"]

df["amount"] = df.apply(clean_price, axis=1)

# Price type
df.price_type.unique()


# Saving cleaned dataset
df_cleaned = df[['slug_url', 'title', 'built_year','is_featured', 'is_premium',
       'floors', 'bedroom', 'bathroom', 'is_price_on_call',
       'price_type','road_access',
       'property_face', 'state', 'district', 'city', 'area', 'area_sq_ft','amount']]

df_cleaned.to_csv("cleaned_data.csv",index=False)


