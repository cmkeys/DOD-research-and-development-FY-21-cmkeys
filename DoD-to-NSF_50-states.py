# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 01:53:45 2020
@author: undiv

This script will form an estimate of DoD FY18 R&D spending in the 50 states
and District of Columbia. The data combines spending for 11 federal agencies.
DoD's portion of the total is 42.0677%.

We will eventually combine this data with GIS shapefiles to build a map of projected 
DoD FY21 R&D spending (after applying a DoD multiplier). 
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
# The Excel file contains FY10 to FY18 combined geographical spending data 
# for 11 federal agencies, including DoD.

zipname = 'https://ncsesdata.nsf.gov/fedfunds/2018/ffs18-dt-tables.zip'
excelname = 'ffs18-dt-tab129.xlsx'
outname = 'DoD_FY18__RD_50_state.csv'

# Use requests.get() to obtain the zip file from NSF. Use zipfile.ZipFile(io.BytesIO(r.content))
# to read zipfile contents obtained from variable 'r'. Use .open() to open
# desired Excel file, which is Table 129 in the zip file. 
# Read the Excel file using pd.read_excel() with arguments (xl,'Table 129',header=3)

r = requests.get(zipname)
z = zipfile.ZipFile(io.BytesIO(r.content))
inp_byte = z.open(excelname)
xl = pd.ExcelFile(inp_byte)
xlf = pd.read_excel(xl,'Table 129', header=3)

# We only want two columns of data: "State or location" and "2018".
# Trim the data to those columns using .iloc[].

trimmed = xlf.iloc[:,[0,9]]

# trim further to include only rows 1-52. This will remove row [0] which is a grand total,
# along with rows 53-57 which included 'Outlying areas', 'Undistributed', 'Other areas',
# and 'Offices abroad', each of which cannot be easily mapped. 

trimmed = trimmed.iloc[1:52]

# Set index as 'State or location'

trimmed.set_index('State or location',inplace=True)

# Set data type to 'int64' to macth the DoD and NSF data types in other scripts.

trimmed = trimmed.astype(np.int64)

# Values are in $ Millions, so multiply the values by 1,000,000

trimmed = trimmed*1000000

# print result. Notice that the data includes District of Columbia. 

print(trimmed)

# Since DoD spending accounts for 42.0667% of the 11 agency total, multiply each value
# by .420667. 

dodportion = trimmed*.420667

# Set result to .astype(np.int64)

dodportion = dodportion.astype(np.int64)

# take the sum of the result as variable 'sumgeo' 

sumgeo = dodportion.sum()

# print 'sumgeo'

print('\n',sumgeo)

# DoD in FY18 spent an estimated $51,969,621,847 on R&D in the 50 states plus 
# District of Columbia.

# Finally, send 'dodportion' to the output file

dodportion.to_csv(outname)