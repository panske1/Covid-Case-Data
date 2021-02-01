Author: Patrick Anske
Last Update: 1/29/2021
Data Source: CDC (link - https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data/vbim-akqf/data )
Files: States.csv - 2 variable dataframe row 1 is full state name, row 2 is state abbreviate
       US_covid.csv - 15 variable dataframe from CDC. Includes aggregated and daily covid data organized by date and state

Reference Code: CovidVisuals.py
Purpose: Visualize COVID Cases and Deaths at National and State levels

To execute CovidVisuals.py the user will need to download historical covid data from the CDC, available at the link in the header of this file. Save the CDC data to a location that is easy to access. Be sure that the file is saved as a .csv file. No other alterations will need to be made prior to upload. Save the lists of state names and abbreviations to a easily accessible location (recommend storing with CDC data). If the state data set is unavailable, copy & paste the delimited list below to your local text editor and save as a .csv. 

Type or copy & paste the file paths for the CDC Covid data and State list into CovidVisual.py at the specified lines. The file path for the CDC data is needed in line 27 of the code. The State list is called in line 32.

To run the code the user will need to have pandas, numpy, Matplotlib, Seaborn, and Tkinter all accessible in the environment that the code is being executed in. Instructions to how to install these modules can be found at https://packaging.python.org/tutorials/installing-packages/. Additionally online compiling services are available for free, such as google colaboratory. 

Once the modules are available simply execute the code. A window will titled "Covid Visualizer" will pop up. This window contains a drop down menu. To select a locality click the arrow to the right of the word "National", highlight the locality of interest by hovering the cursor over it, and click it to select it. Click submit and a second window will appear with a graphical interpretation of the data for the locality selected. To close the window click "Return to Menu" at the bottom of the graphic window, or click the X in the top corner. Additionally, for visual comparison multiple visuals can be created in one session. Simply make first select, without closing the window select another locality and click submit again. A third window will be generated with the new selection.

To exit the program click "Return to Menu", and then click "Close" this will end the program.



States Data for CSV creation:

state,abbr
National,NTL
Alabama,AL
Alaska,AK
Arizona,AZ
Arkansas,AR
California,CA
Colorado,CO
Connecticut,CT
Delaware,DE
Florida,FL
Georgia,GA
Hawaii,HI
Idaho,ID
Illinois,IL
Indiana,IN
Iowa,IA
Kansas,KS
Kentucky,KY
Louisiana,LA
Maine,ME
Maryland,MD
Massachusetts,MA
Michigan,MI
Minnesota,MN
Mississippi,MS
Missouri,MO
Montana,MT
Nebraska,NE
Nevada,NV
New Hampshire,NH
New Jersey,NJ
New Mexico,NM
New York City,NYC
New York,NY
North Carolina,NC
North Dakota,ND
Ohio,OH
Oklahoma,OK
Oregon,OR
Pennsylvania,PA
Rhode Island,RI
South Carolina,SC
South Dakota,SD
Tennessee,TN
Texas,TX
Utah,UT
Vermont,VT
Virginia,VA
Washington,WA
West Virginia,WV
Wisconsin,WI
Wyoming,WY