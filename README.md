# SystemSpaceAnalyzer
A standalone tool built in Python to analyze the files present in the given system path with the following capabilities, 
  1. Download a HTML report with the analysis highlights,  
  2. Show Top 10 big file present in the path, 
  3. Export all the file and folder details into an excel sheet, 
  4. Plot how the size of the folder had been growing over the years, 
  5. Predict how the size of the folder will increase in the next 1 year.

This tool was built in python3 using the following libraries/packages,
  1. ‘tkinter ‘for the GUI.
  2. ‘pandas’ for analysis
  3. ‘matplotlib’ and ‘seaborn’ for the plots
  4	 ‘statsmodels’ for the time series prediction
  5	 Other standard libraries like logging, os, math, etc.

How to Run?
1. If python3 is already installed in your machine, then fulfil all the dependencies and run ‘Run.bat’ to start the tool on Windows. 
2. If you don’t want install python then I have also created an ‘exe’ file to run this standalone, but the size is around 70MB, so I was not able to place it in the github. I can share it directly if you are interested.


How to use the tool?

Step 1. Enter the system path to analyze and click ‘Analyze’ button. The tool will analyze the given path and present the following details and options.
  1. Download Report
  2. Show Top 10 Big Files
  3. Export File Details
  4. Show Size Growth Graph
  5. Predict Size Growth
  
Download Report
  1. Click the ‘Download Report’ button to download a HTML report into the ‘report’ folder of the tool. Once the report is downloaded successfully the below dialog box will appear.
  2. An error message will appear if there are any issues while downloading the report directing you to check the logs for the reason for the failure.

Show Top 10 Big Files
  1. This option will show the top 10 big files present in the path with options to select files to delete or delete all the files in one go.
 
Export File Details
 1. This option will export all the file details in an excel file into the ‘export’ folder of the tool. I have used pandas data frame export option for this.
 2. Depends upon whether the export is success or failure, a dialog box like the ‘Download Report’ option will appear.
 3. The exported excel file will have two sheets,
    a. ‘File Level’ sheet will have the Folder Name, File Name, File Type, Created Date, Last Modified Date and Size in MB
    b. ‘Folder Level’ sheet will have the Folde Name, File Count and Size in MB.

Show Size Growth Graph
  1. This option will plot a graph against the year and how the folder size has been growing during the years. I have used the created date of each file to find the cumulative size of the folder.

Predict Size Growth
  1. This option will plot a prediction of how the folder size is expected to grow in the next 1 year. I have used a simple ARIMA model for this.
 
