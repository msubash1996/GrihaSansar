#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 21:09:11 2021

@author: overlord
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_data.csv")

summary = df.describe()

sorted_amount_df = df.sort_values("amount")

# Price mistype 
df.loc[df.amount == 5e+06,"amount"] = 50000000

sorted_area_df = df.sort_values("area_sq_ft")

# 48 sq ft area to nan
df.loc[df.area_sq_ft == 48.68,"area_sq_ft"] = np.nan

df.to_csv("cleaned_data.csv",index=False)