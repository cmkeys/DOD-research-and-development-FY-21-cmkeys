# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 03:52:39 2020
@author: undiv

This script pulls data from the National Science Foundation Federal Funds for
Research and Development Survey related to international R&D spending (FY18).
We will eventually combine this data with domestic spending to develop a global
map of DoD spending.
"""

# import modules

import pandas as pd
import numpy as np
import requests
import zipfile
import io

# Display Max Rows so you can see what you're getting as you go

pd.set_option('display.max_rows',None)

# Set up file names: the NSF URL with the .zip file; the .xlsx file within the .zip
# folder; and the output file we will write the results into. 
# The Excel file contains FY18 international spending data by country.

zipname = 'https://ncsesdata.nsf.gov/fedfunds/2018/ffs18-dt-tables.zip'
excelname = 'ffs18-dt-tab086.xlsx'
outname = 'DoD_FY18__RD_international.csv'

# Use requests.get() to obtain the zip file from NSF. Use zipfile.ZipFile(io.BytesIO(r.content))
# to read zipfile contents obtained from variable 'r'. Use .open() to open
# desired Excel file, which is Table 86 in the zip file. 
# Read the Excel file using pd.read_excel() with arguments (xl,'Table 86',header=3)

r = requests.get(zipname)
z = zipfile.ZipFile(io.BytesIO(r.content))
inp_byte = z.open(excelname)
xl = pd.ExcelFile(inp_byte)
xlf = pd.read_excel(xl,'Table 86', header=3)

# We only want two columns of data: "Region, country, or economy" and "DOD".
# Trim the data to those columns using .iloc[]. They are columns [0,3]

trimmed = xlf.iloc[:,[0,3]]

# Set index as "Region, country, or economy"

trimmed.set_index('Region, country, or economy',inplace=True)

print(trimmed)

# NSF data includes regions as rows, which double-counts data. 
# Drop these index labels by creating a list of labels to drop
# and applying the .drop() command on the list.

droplist = ['All areas and organizations','Africa','Asia','Asian countries, other',
            'Europe','North America','Oceania','International organizations'] 

trimmed = trimmed.drop(droplist)

# We now want to drop all values with zeros. To do this, set the index to 'DOD'
# and create a for loop that runs over 'index,row' and uses the .iterrows() command.
# If the row in 'DOD' equals zero, drop the row.
 
trimmed.set_index('DOD')

for index, row in trimmed.iterrows():
    if row['DOD'] == 0:
        trimmed.drop(index, inplace=True)

# Now drop any rows with null values using the .dropna() command
        
trimmed.dropna()
        
print(trimmed)    