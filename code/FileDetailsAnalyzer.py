import pandas as pd
import numpy as np
import logging
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter.messagebox as tkmsg
from datetime import datetime, date
from tkinter import *
import os
import traceback



'''
Description : Function to create a folder level daraframe by aggregating the file level datafram created.
Input       : List of all the files and its details in the System Path..
Return      : File level dataframe.
'''
def createFolderDataFrame(file_df):
	# Aggregate the size in each folder
	folder_df_size = file_df.groupby(by='Folder Name', as_index=False).sum()
	# Aggregate the number of files in each folder
	folder_df_count = pd.DataFrame (file_df.groupby(by='Folder Name', as_index=False).count() [['Folder Name', 'File Name']])
	# Merge both data frames together on the key 'Folder Name'
	folder_df = pd.merge(folder_df_count, folder_df_size, left_on='Folder Name', right_on='Folder Name')
	#Rename 'File Name' column into 'File Count'
	folder_df = folder_df.rename({'File Name': 'File Count'}, axis=1)

	return folder_df


'''
Description : Create the analyzer report and download 
Input       : File and Folder level dataframes.
Return      : None
'''
def downloadReport(report_highlights_list, file_df):

	report_success_indc = True
	try:		
		with open('..\\report\\SystemFileAnalyzer_Report.html','w') as html_file:	

			html_file.write("""<html>""")
			# Report header and generated Timestamp
			html_file.write("""<head><h1 style ="color:blue;text-align:center;"><b>Sytem File Analyzer Report</b></h1> 
			                <h4 style ="color:red;text-align:center;"><b>Generated at """+datetime.now().isoformat()+"""</b></h4></head>""")

			#Style for table header
			html_file.write("""<style>table, th, td {border: 1px solid black;  border-collapse: collapse;}
			            th, td {padding: 5px;}
			            th{text-align: center; background-color:grey;}</style>""")
			#Insights			
			html_file.write("""<body><h1 style ="text-align:left;"><b>Insights:</b></h1> """)
			#Insights from Report Highlights Section
			for highlights_text in report_highlights_list:
				html_file.write("""<p>"""+highlights_text+"""</p<br>""")			

			html_file.write("""<p>4. The top 10 files in terms of size are:</p>""")

			html_file.write("""<table border="1" class="table"><thead><tr><th>S.No</th><th>File Path</th> <th>Size in MB</th></tr> </thead><tbody>""")			
			
			#Top 10 File List
			top_10_file_df = file_df.sort_values('Size in MB',ascending=False).head(10)
			top_10_file_list = top_10_file_df.values.tolist()
			#count for S.No column
			count = 1
			#create each row in th table
			for file_detail in top_10_file_list:
				html_file.write("""<tr><td>"""+str(count)+"""</td><td>"""+str(file_detail[0]+file_detail[1]+"""</td><td>"""+str(file_detail[5])+"""</td></tr>"""))
				count = count+1

			html_file.write("""</tbody></table>""")	
			#File Type and its Count 
			file_type_df = file_df.groupby(by='File Type', as_index=False).count() [['File Type', 'File Name']]
			file_type_df = file_type_df.rename(columns = {'File Name':'File Count'})
			plt.figure(figsize=(10,10))
			sns.barplot(x='File Type', y = 'File Count', data =file_type_df.sort_values('File Count',ascending=False).head(10)).set_title("Top 10 File Types")
			plt.savefig('..\\report\\images\\File_Type.png')

			html_file.write("""<p>5. You have   """+ str(len (file_df['File Type'].unique()))+""" different file types in the shared path. The top 10 files and its counts are plotted below:</p>""")
			html_file.write("""<img src="..\\report\\images\\File_Type.png" width="700" height="500"/>""")
			#add end tags
					
			html_file.write("""</body>""")
			html_file.write("""</html>""")
			
	except Exception as e:
		report_success_indc = False
		logging.error('Error while creating the report and the error is {}'.format(str(e)))

	if report_success_indc:
		tkmsg.showinfo(title='Download Report', message='Successfully downloaded the report. Please check the \'report\' folder')
	else:
		tkmsg.showerror(title='Download Report', message='Error while downloding the report. Please check the logs')



'''
Description : Function to create a size growth grapah and save it inside the images folder.
Input       : List of all the files and its details in the System Path..
Return      : Success Indicator
'''
def createGrowthGraph(file_df):

	creat_grpah_indicator = False

	try:	

		# Delete the image if it is present already
		if os.path.isfile('..\\report\\images\\size_growth_graph.png'):
			os.remove('..\\report\\images\\size_growth_graph.png')

		# Group by on Created Date to find the size of the file on each day.
		ts_size_in_mb_df = pd.DataFrame(file_df.groupby('Created Date').sum()['Size in MB'])

		# oldest date in the data frame index
		oldest_date =  ts_size_in_mb_df.index.min()		
		#latest date in the dataframe index
		latest_Date = ts_size_in_mb_df.index.max()

		#use the oldest date and latest date and create an index of all dates between these two.
		date_index = pd.date_range(start=oldest_date,end=latest_Date)

		# Create an empty dataframe only using the date_index
		size_graph_df = pd.DataFrame(index=date_index)
		# Merge two dataframes on Index
		size_graph_df = pd.merge(size_graph_df, ts_size_in_mb_df, left_index=True,right_index=True, how='left')


		# Fill the previous day size for the missing values in 'Aggregated Size In MB column'
		size_graph_df['Size in MB'].fillna(0, inplace=True)

		#Calculate monthly sum and store it in a DataFrame
		mon_size_graph_df = pd.DataFrame(size_graph_df['Size in MB'].resample('MS').sum())


		# Sum the previous size in MB and create the aggregate the size
		mon_size_graph_df.reset_index(level=0, inplace=True)

		for i in range(1, len(mon_size_graph_df)):
			mon_size_graph_df.loc[i, 'Size in MB'] = mon_size_graph_df.loc[i-1, 'Size in MB'] + mon_size_graph_df.loc[i, 'Size in MB']

		mon_size_graph_df.rename(columns={'index':'Created Date'}, inplace=True)
			
		plt.figure(figsize=(10, 6))
		mon_size_graph_df.plot(x='Created Date', y = 'Size in MB', kind = 'line', label='Actual Size (MB)')
		
		plt.title('Size Growth Graph')
		plt.xlabel('Date')
		plt.ylabel('Size (MB)')	

		plt.savefig('..\\report\\images\\size_growth_graph.png')
		logging.info('Graph has been created and stored succuessfull under \\report\\image folder')

		# Set the indicator to True
		creat_grpah_indicator = True

		# Aggregate the size of the files created every day
	except Exception as e:		
		logging.error('Error while plotting the size growth graph and the error is {}'.format(traceback.format_exc()))
		tkmsg.showinfo(title='Size Growth Grpah', message='Error while plotting the graph. Please check the logs for more details')
	
	
	#return the creat_grpah_indicator

	return creat_grpah_indicator