"""
The goal of this script is to sort the Fisal Year 2021 Department of Defense
Research and Budget Request by Budget Activity. 
There are 8 DoD Budget Activities:

01 – Basic Research
02 – Applied Research
03 – Advanced Technology Development
04 – Advanced Component Development and Prototypes
05 – System Development and Demonstration
06 – RDT&E Management Support
07 – Operational System Development
08 – Software and Digital Technology Pilot Programs

We will eventually combine this data with the geographical distribution
of DoD R&D expenditures from Fiscal Year 2018 obtained from the 
National Science Foundation, in order to make a guess at likely 
geographical distributions of FY21 funds.

DoD R&D budget requests are stored in Excel files.
Pandas can read Excel files.
If we need to write to Excel files, we'll need a third party module later, but
this will not be necessary for our purposes.
"""

#Step 1: import pandas as pd

import pandas as pd

# Display Max Rows so you can see what you're getting as you go

pd.set_option('display.max_rows',None)

# Download the R&D Budget for FY21 from DoD Comptroller website

urlxl = 'https://comptroller.defense.gov/Portals/45/Documents/defBudget/fy2021/r1.xlsx'

# just in case
# xl = requests.get(urlxl)

# Use pandas to identify the Excel file:

xlsx = pd.ExcelFile(urlxl)

# Use pandas to read the Excel file.
# We use "header=1" because the first spreadsheet row [0] is blank)

rf = pd.read_excel(xlsx,'Exhibit R-1',header=1)

# Because we are interested in sorting by Budget Activity, set the index
# to the Budget Activity column, which on the Excel sheet is 'Budget\nActivity'.
# For ease, shorten to a variable 'BA'.

BA = 'Budget\nActivity'
rf.set_index(BA,inplace=True)

# Print 'Budget Activity Title' for reference and orientation using the
# .drop_duplicates() operation.
# Note that there are only 8 Budget Activities, but there is some inconsistency
#in the spreadsheet, with uses of '&' or 'and' creating different rows, etc.
# We don't need to clean up this mess to fulfill our purposes, since the numeric
# Budget Activity values are as they should be, and those are what matter.

print(rf['Budget Activity Title'].drop_duplicates())

# Verify that the list of unique index values is no more or less than 8.
# Note: Budget Activity 8 (Software and Digital Technology Pilot Programs) is
# was created in Fiscal Year 21. In prior years there were only 7 Budget Activities.

# print(rf.info())
print(rf.index.unique())

# For orientation, print the columns and data types.

print(rf.dtypes)

# Filter for the two columns we really want (BA and FY21 Total) using the
# .filter() command.
# These columns have quirky titles due to the formatting of the Excel columns.
# For ease, create a variable 'FY21' for the Total column from the rf.dtypes printout,
# to go with 'BA'.

FY21 = 'FY 2021\nTotal\n(Base + OCO)'
trimmed = rf.filter([BA,FY21],axis=1)

# Now sum up the BA values using the .groupby() command and the .agg(['sum']) command.

sumBA = trimmed.groupby(BA)[FY21].agg(['sum'])

# Since the data are in $Thousands, we need to multiply by 1000 to get actuals

sumBA = sumBA*1000

# create a variable to store only the sums rather than each of the 1136 row values.
# print to make sure it looks right

totals = sumBA

print(totals)

# Write the results to a .csv file named 'DoD FY21 BA Totals.csv'

totals.to_csv('g01-DoD-FY21-BA-Totals.csv')

# For orientation, take a sum of 'sumBA'. Result: DoD is requesting ~$108 Billion
# of Research & Development funding for Fiscal Year 2021. This money will be spent
# worldwide during FY21 and FY22. We'd like to know where the money will be spent.
# That will be the next exercise.

print('\n',totals.sum())
