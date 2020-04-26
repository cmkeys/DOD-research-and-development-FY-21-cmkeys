# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 05:34:15 2020
@author: undiv

The goal in this script is to combine the NSF Federal Funds for R&D Survey data
with the FY21 DoD Budget Request Data from the .csv files obtained in previous scripts.
We want a ratio that tells us the growth from FY18 to FY21.

The NSF data is coded as: "Total Research" -- corresponding to Budget Activity 1+2;
"Total experimental developmentb"-- corresponding to Budget Activities 3-6;
and "Total operational systems developmentc"-- corresponding to Budget Activity 7.

We can then apply the ratio to each term of the 50-state NSF geographical spending table,
and to the international data will will obtain later.
"""

# import pandas as pd

import pandas as pd
import csv
import numpy as np

# set variables for the .csv files from prior scripts

dodcsv = 'DoD FY21 BA Totals.csv'
nsfcsv = 'NSFtotals.csv'

# create output .csv filename for combined results

outname = 'DoD_FY21_Multiplier.csv'

#  Set up output file with columns titled "BA1-6" and "Total"

out_handle = open(outname,'w',newline='')
out_writer = csv.writer(out_handle)

# set variables to read input files with pd.read_csv() command

dodreader = pd.read_csv(dodcsv)
nsfreader = pd.read_csv(nsfcsv)

# print csv outputs to see which rows you will need. Goal is include
# Budget Activities 1-6 and 8 from the DoD file, and compare the sum of these 
# with the sum of the NSF data to get a ratio.

print(dodreader)
print(nsfreader)

# Use .iloc[] command with arguments [[rows],column] to select 
# Budget Activities from Dod data.

dodBA = dodreader.iloc[[0,1,2,3,4,5,6,7],1]

# print result to verify a column of BA totals for DoD FY21 R&D budget request.
# Print the sum

print('\n', dodBA)
print('\nSum of FY21 DoD Request:',dodBA.sum())

# Use .iloc[] to select the totals from nsfreader. We need to exclude
# 'Total operational systems developmentc' because NSF does not use this data
# for its geographical R&D distributions.

nsfBA = nsfreader.iloc[[0,1,2],1]

# Note: the NSF data is currently in $Millions while DoD data is in $.
# Multiple NSF data by 1,000,000 to get actuals

nsfactuals = nsfBA*1000000

# use .astype(np.int64) command to set NSF data to dtype 'int64',
# which will match DoD data. Print the sum.

nsfactuals = nsfactuals.astype(np.int64)

print('\n',nsfactuals)
print('\nSum of NSF DoD FY18:',nsfactuals.sum())

# The DoD FY21 R&D Budget Request total is $68.084022 Billion.
# The NSF FY19 R&D Budget spending total is $56.0494 Billion
# We can now obtain a ratio of FY21 to FY19, which will function as
# a multiplier for the geographical projections that follow.

# Divide the two sums to obtain the multiplier

multiplier = dodBA.sum()/nsfactuals.sum()

print("\n\nMultiplier is:",multiplier)

# Finally, write the multiplier into the .csv output file.
# Close the file.

out_writer.writerow(['1.2887570722688233'])
out_handle.close()

