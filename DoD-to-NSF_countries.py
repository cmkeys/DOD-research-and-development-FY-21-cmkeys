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

# First, the columns of the file are not helpful. Rather than "Region, country, or economy"
# and "DOD", we prefer "Country" and "Total" to be consistent with
# other scripts. Use the .rename() command, changing columns using Dict {} symbols.

xlf = xlf.rename(columns={"Region, country, or economy": "Country", "DOD": "Total"})

# We only want two columns of data: "Country" and "Total".
# Trim the data to those columns using .iloc[]. They are columns [0,3]

trimmed = xlf.iloc[:,[0,3]]

# Set index as "Country"

trimmed.set_index('Country',inplace=True)

# We need to rename a handful of indexes to align Country names in NSF's database
# with international names in latitude/longitude databases.
# We need to replace country names with: "South Korea", "The Bahamas",
# "Hong Kong S.A.R." , "Czech Republic", and "British Virgin Islands".
# Use the .rename() command with arguments 'index= {}, inplace=True'

trimmed.rename(index={'Korea, South':'South Korea','Bahamas, The':'The Bahamas',
                      'Czechia':'Czech Republic','Hong Kong':'Hong Kong S.A.R.',
                      'Virgin Islands, British':'British Virgin Islands'},inplace=True)

print(trimmed)

# NSF data includes regions as rows, which double-counts data.
# Drop these index labels by creating a list of labels to drop
# and applying the .drop() command on the list.

droplist = ['All areas and organizations','Africa','Asia','Asian countries, other',
            'Europe','North America','South America','Oceania','International organizations']

trimmed = trimmed.drop(droplist)

# We now want to drop all values with zeros. To do this, set the index to 'Total'
# and create a for loop that runs over 'index,row' and uses the .iterrows() command.
# If the row in 'Total' equals zero, drop the row.

trimmed.set_index('Total')

for index, row in trimmed.iterrows():
    if row['Total'] == 0:
        trimmed.drop(index, inplace=True)

# Now drop any rows with null values using the .drop() command. Here we
# first reset the index to locate the rows with null values, then drop the
# rows with null values.

trimmed = trimmed.reset_index()

trimmed = trimmed.drop(index=[60,61,62,63,64])

# print result to make sure there are no nulls and no regions

# Return the index to 'Country'

trimmed.set_index('Country',inplace=True)

# The dollars are in thousands in this Table, therefore multiply all values
# by 1000.

trimmed = trimmed*1000

# Finally, multiply the Totals by the DoD FY21 Multiplier, which is
# '1.2887570722688233' -- use .astype(np.int64) to set the result to integer datatype.
# Print the result.

trimmed['Total'] = trimmed['Total'].apply(lambda x: x*1.2887570722688233)

trimmed['Total'] = trimmed['Total'].astype(np.int64)

print(trimmed)

print("\n\n",trimmed.sum())

# Note also: this sum does not include any "Undistributed" amounts that may or
# may not have been spent overseas on R&D for which Vendor Information is
# undisclosed. There was over $1.6 Billion in "Undistributed" DoD R&D spending
# in FY18. This money was spent *somewhere*, we just cannot say where.

# Finally export to .csv which is the variable 'outname'

trimmed.to_csv(outname)
