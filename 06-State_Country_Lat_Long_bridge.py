# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 08:41:43 2020
@author: undiv

This script intends to attach latitude and longitude data to the 50 states
and countries.
"""

import pandas as pd

statelat = 'State_lat_long.csv'
countrylat = 'country_centroids_az8.csv'
dodcountry = 'DoD_FY18__RD_international.csv'
dodstate = 'DoD_FY18__RD_50_state.csv'
outname = 'FY21_dod_lat_estimate.csv'

dodstateread = pd.read_csv(dodstate)
dodcountryread = pd.read_csv(dodcountry)
statelatread = pd.read_csv(statelat)
countrylatread = pd.read_csv(countrylat)

# Merge the State-level spending totals and latitude/longitude files, using the
# .merge() command, with "State" as the join column, and "m:1" as the join type.
# Print the result to make sure Total and Lat/Long are present for each state.

statemerge = dodstateread.merge(statelatread, on='State', validate='m:1', indicator=True)

#print(statemerge)

# Do the same for the country-level data.

countrymerge = dodcountryread.merge(countrylatread, on='Country', validate='m:1', indicator=True)

#print(countrymerge)

# Now let's merge the State and Country datasets under a unified set of column headings.
# First, rename the 'Country' column in 'countrymerge' to 'State'
# and use lowercase letters for 'Latitude' and 'Longitude'.

countrymerge = countrymerge.rename(columns={"Country": "State","Latitude":"latitude","Longitude":"longitude"})

# Now notice that the US States have latitude first, then longitude, while the
# Countries have longitude, then latitude. We need to align these. So,
# rearrange the countrymerge columns in the following order: 'State, Total, latitude, longitude'.

countrymerge = countrymerge[countrymerge.columns[[0,1,3,2]]]

# We in effect just dropped the "_merge" column from the Country dataframe.
# Do the same with the State data.

statemerge = statemerge[statemerge.columns[[0,1,2,3]]]

# Now, use pd.concat() to fuse the datasets on the "State" column. Call the variable
# 'dodlat'.

frames = [countrymerge,statemerge]
dodlat = pd.concat(frames)

# Set the index on 'State' column

dodlat.set_index('State',inplace=True)

# print result

print(dodlat)

# Now print the grand total we've obtained

print(dodlat.Total.sum())

# Notice that the total is only $77,827,361,780 out of the total FY21 request of $107,901,057,000
# Why the discrepancy of $30.07 Billion? Well, we cannot use: "Undistributed" amounts totalling $24.1 Billion; 
# "Other Areas" without country designation totalling $5.9 Billion. 

# Finally, export the result to a .csv file that can be used in QGIS.

dodlat.to_csv(outname)
