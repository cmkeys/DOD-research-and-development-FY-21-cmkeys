# Using Python and QGIS to Anticipate R&D Spending Patterns:
![](https://github.com/cmkeys/DOD-research-and-development-FY-21-cmkeys/blob/master/World.png)

The goal of these scripts is to answer the following question: where is the Department of Defense (DoD) likely to spend 
its Fiscal Year 2021 Research & Development (R&D) dollars? 

DoD R&D Projects are sorted into 8 Budget Activities:
##### 01 – Basic Research
##### 02 – Applied Research
##### 03 – Advanced Technology Development
##### 04 – Advanced Component Development and Prototypes
##### 05 – System Development and Demonstration
##### 06 – RDT&E Management Support
##### 07 – Operational System Development
##### 08 – Software and Digital Technology Pilot Programs

We write scripts to fetch the Fiscal Year 2021 President's Budget request from the DoD Comptroller's website, 
and we fetch historical data from the National Science Foundation's Survey of Federal Funds for R&D. We then
clean and analyse the datasets, isolating DoD spending for all 50 United States and all countries internationally.

Next, we attach Geo-locator data (latitude and longitude) to the State and Country data, and fetch Shape Files 
from the web for the States and Countries. We then project a rough estimate of the geographic distribution 
for Fiscal Year 2021 using QGIS. The results look like the graph above:

We can zoom into particular regions to get a better view:

##### U.S. Tri-State area (Virginia, Maryland, Washington D.C.):
![](https://github.com/cmkeys/DOD-research-and-development-FY-21-cmkeys/blob/master/Tri-State%20Estimate%20FY21%20DoD%20R%26D.png)

##### Western United States:
![](https://github.com/cmkeys/DOD-research-and-development-FY-21-cmkeys/blob/master/West_US.png)

##### U.S. Central, Midwest, South:
![](https://github.com/cmkeys/DOD-research-and-development-FY-21-cmkeys/blob/master/Plains_Midwest_TX_LA.png)

##### Central & South America:
![](https://github.com/cmkeys/DOD-research-and-development-FY-21-cmkeys/blob/master/Central%20%26%20South%20America.png)

##### Portions of Europe:
![](https://github.com/cmkeys/DOD-research-and-development-FY-21-cmkeys/blob/master/UK_NE_BL_LX.png)
![](https://github.com/cmkeys/DOD-research-and-development-FY-21-cmkeys/blob/master/E.Europe_Greece_Turkey.png)

##### Middle East:
![](https://github.com/cmkeys/DOD-research-and-development-FY-21-cmkeys/blob/master/Middle%20East%20Estimate_DoD%20FY21%20R%26D%20Spending.png)

##### Asia:
![](https://github.com/cmkeys/DOD-research-and-development-FY-21-cmkeys/blob/master/Asia_estimate.png)

##### Australia & New Zealand
![](https://github.com/cmkeys/DOD-research-and-development-FY-21-cmkeys/blob/master/AUS_NZ_.png)

##### There are several limitations inherent in the analysis:

1) The best available data is from FY18. We are making a projection to FY21. Major adjustments in geographic distribution in FY19 and FY20 will not show up, to say nothing of changes that will occur in FY21. Furthermore, the data covers "obligations," i.e. initial contract awards. The data does not account for the allocation of sub-contracting dollars. There is extensive sub-contracting in the DoD R&D ecosystem. NSF Survey data cannot capture the geographic distribution of sub-contracting. 

2) After gathering all available State and Country data, we can only map $77,827,361,780 out of the total FY21 request of $107,901,057,000. The discrepancy of $30.07 Billion is a result of **two un-mappable pieces of NSF data**: "Undistributed" amounts totalling $24.1 Billion in FY21; and spending labeled "Other Areas" without country designation totalling $5.9 Billion in FY21. "Undistributed" amounts are a result of DoD using "legacy systems" for a significant portion of its R&D accounting. These legacy systems do not deliver reports by geographic distribution. Therefore, DoD reports these amounts in a separate category: "Undistributed". A separate portion of classified research is also reported as "Undistributed." These data are all absent from the QGIS projections.

5) Funding for the Marshall Islands is underreported in the NSF FY18 dataset. US Army R&D funds for Kwajalein Atoll would add ~$400 million to the Marshall Islands total, not depicted in QGIS projections.

Despite these limitations, the data provide a useful overview of R&D spending patterns for the U.S. Department of Defense. This global research enterprise spans over 60 countries.

#### For more information on method, see notes in the repository .py scripts. 
