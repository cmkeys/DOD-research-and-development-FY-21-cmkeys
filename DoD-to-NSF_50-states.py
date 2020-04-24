# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 01:53:45 2020
@author: undiv

This script will gather the latest available DoD R&D spending data for the 50 states
and District of Columbia. The data covers obligations (i.e. contract awards) 
that occurred during FY18.

Note: A significant portion of DoD R&D spending is listed as "Undistributed"
in the dataset. This is a result of 1) classified research, and 2) legacy accounting 
systems that simply do not provide geographic details for reporting to NSF.
In future years DoD hopes to minimize 'Undistributed' reporting, but for now
this is the best we can do. 

Also, the data is from FY18. We would prefer FY19 spending, but these will not 
be available until NSF publishes the next volume of its R&D Funds Survey.

We will eventually combine this data with GIS shapefiles to build a map of projected 
DoD FY21 R&D spending (after applying a DoD multiplier). 
"""
# import pandas

import pandas as pd

# Display Max Rows so you can see what you're getting as you go

pd.set_option('display.max_rows',None)

# Set up file names: the NSF URL with the .xlsx file, 
# and the output file we will write the results into. 
# The Excel file contains FY18 DoD geographical spending data.
# We will select data for the 50 states.

excelname = 'https://ncsesdata.nsf.gov/fedfunds/2018/excel/ffs18-dt-tab094.xlsx'
outname = 'DoD_FY18__RD_50_state.csv'

# Open the desired Excel file from the URL, which is Table 94. 
# Read the Excel file using pd.read_excel() with arguments (xl,'Table 94',header=3)

xl = pd.ExcelFile(excelname)
xlf = pd.read_excel(xl,'Table 94', header=3)

# We only want two columns of data: "State or location and agency" and "Total".
# Trim the data to those columns using .iloc[].

trimmed = xlf.iloc[:,[0,1]]

# trim further to include only rows 1-253. 

trimmed = trimmed.iloc[1:253]

# We only want the State and the R&D Total, but there are rows in between.
# The state names are in rows 1,6...251 alternating every 5 rows. The R&D Totals
# are in rows 2,7...252 alternating every five rows. Make a list for trimming.
# [If you know of a better way, by all means go for it.]

statelist = [
        1,2,6,7,11,12,16,17,21,22,26,27,31,32,36,37,41,42,46,47,51,52,56,57,61,
        62,66,67,71,72,76,77,81,82,86,87,91,92,96,97,101,102,106,107,111,112,116,
        117,121,122,126,127,131,132,136,137,141,142,146,147,151,152,156,157,161,
        162,166,167,171,172,176,177,181,182,186,187,191,192,196,197,201,202,206,
        207,211,212,216,217,221,222,226,227,231,232,236,237,241,242,246,247,251,252
        ]

# Use .loc[statelist] to trim the data frame.

trimmed = trimmed.loc[statelist]

# Now we need the value of every other row to be switched into the second column.
# Use pd.DataFrame(trimmed.Total.values.reshape(-1,2),columns=['State','Total']) to 
# put the values where they should be. Set the Totals to integer datatype.

trimmed = pd.DataFrame(trimmed.Total.values.reshape(-1,2),columns=['State','Total'])
trimmed.Total = trimmed.Total.astype(int)

# This method produced the unintended consequence of replacing the States with
# null values. To resolve the problem, add a list of the States in alphabetical order
# just as in the NSF dataset.

statenames = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 
              'California', 'Colorado', 'Connecticut', 'Delaware', 
              'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 
              'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 
              'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
              'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 
              'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 
              'North Carolina', 'North Dakota', 
              'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 
              'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 
              'Texas', 'Utah', 'Vermont', 'Virginia', 
              'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

# Replace the null values with the State names, using .drop() to remove the null
# values and replacing with the State names.

n = trimmed.columns[0]
trimmed.drop(n, axis = 1, inplace = True)
trimmed['State'] = statenames

# This method produced an unintended consequence of flipping the columns.
# "Total" is now column [0] and State is column [1].
# To resolve, switch the columns using .head()

trimmed = trimmed[['State','Total']]
trimmed.head()

# The values in the NSF dataset are in $K, so multiply the Totals by 1000
# using .apply(lambda x: x*1000)

trimmed['Total'] = trimmed['Total'].apply(lambda x: x*1000)

# print the result. Check that the values are correct by using the Variable explorer
# and viewing the xlf DataFrame in comparison with the trimmed DataFrame.

print(trimmed)

# Set the index to 'State' for ease of use later.

trimmed.set_index('State',inplace=True)

# Finally, send to the output file

trimmed.to_csv(outname)