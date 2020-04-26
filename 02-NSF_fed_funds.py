# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 00:58:58 2020
@author: undiv

The goal of this script is to bring in FY18 Dept. of Defense R&D spending 
from the National Science Foundation's Federal Funds for Research and Development Survey,
which tracks R&D spending by geography, performer type, budget activity, field and 
sub-field of science and engineering, among other variables.

The first step is to store the values we need in a .csv
that can be combined with the DoD Budget Request data from the "DoD FY21 BA Totals.py" script.

"""

# import pandas, requests, zipfile, io 

import pandas as pd
import requests
import zipfile
import io

# Display Max Rows so you can see what you're getting as you go

pd.set_option('display.max_rows',None)

# Set up file names: the NSF URL with the .zip file; the .xlsx file within the .zip
# folder; and the output file we will write the results into. 
# The Excel file contains FY18 DoD R&D obligations (i.e. contract award) data.

zipname = 'https://ncsesdata.nsf.gov/fedfunds/2018/ffs18-dt-tables.zip'
excelname = 'ffs18-dt-tab009.xlsx'
outname = 'NSFtotals.csv'


# It is best to use the requests.get() command to extract the .zip from the URL,
# then to use BytesIO translate the contents.
# Open the .xlsx file once the .zip is obtained. Make an Excel reader for the file. 
# If you open the Excel file, there is one worksheet 'Table 9' with messy headers.
# We are seeking data from the 'Total' column, where the header is in row 3.
# As a result we need to use 'header=3'.

r = requests.get(zipname)
z = zipfile.ZipFile(io.BytesIO(r.content))
inp_byte = z.open(excelname)
xl = pd.ExcelFile(inp_byte)
xlf = pd.read_excel(xl,'Table 9',header=3)

# Filter for the 'Agency' and 'Total' columns

trimmed = xlf.filter(['Agency','Total'],axis=1)

# If you print 'trimmed' at this point, you will see what we're dealing with:
# We only want the Department of Defense totals, but each Component of DoD has 
# identically-titled rows. We need only the first 12 rows of data.
# Use the .head() command to remove rows we don't need. Print the result

tot = trimmed.head(11)

print(tot)

# We only want data for the following Budget Activity proxies: 
# 'Total research','Total experimental developmentb','Total operational systems developmentc'
# From print(tot) we see these correspond to rows 4, 7, and 10.
# Use .iloc[] to obtain these rows, keeping the column data, using
# print() to verify

trimtot = tot.iloc[[4,7,10],:]

print("\n\n",trimtot)

# Take the sum. The numbers are in $ Millions.
# As you can see, the Department of Defense spent $83.7249 Billion on R&D in 2018.
# We can now set about mapping the NSF spending data onto the DoD FY21 Budget Request

print("\n\n",trimtot.sum())

# Now set the index to 'Agency' and write the result to a .csv file

trimtot.set_index('Agency',inplace=True)
trimtot.to_csv(outname)

