
#https://towardsdatascience.com/time-series-forecasting-predicting-stock-prices-using-facebooks-prophet-model-9ee1657132b5#:~:text=1.1.&text=Time%2Dseries%20forecasting%20models%20are,used%20for%20non%2Dstationary%20data.&text=Some%20examples%20of%20time%2Dseries,a%20house%20over%20time%20etc.
#https://towardsdatascience.com/an-end-to-end-project-on-time-series-analysis-and-forecasting-with-python-4835e6bf050b
# https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/

'''
Space Analyser - Functionalities:
1. List down all the files from the given path and also present the folder level view
2. Analyse the user's file creation and modifiy behaviour
3. Delete unwanted files or folders to free up some quick space.
'''

import pandas as pd
import numpy as np
import os
import math
#import seaborn as sns
#import matplotlib.pyplot as pltimport os
import logging
from tkinter import *
#import tkinter as tk
import tkinter.messagebox as tkmsg
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from PIL import ImageTk,Image  
from FileDetailsExtractor import extractFileDetails
from FileDetailsAnalyzer import createFolderDataFrame, downloadReport, createGrowthGraph
from FileSizePredictor import predictSizeGrowthGraph
import sys


# List of frames that need to be deleted
delete_frame_list = []
delete_panel_list = []
delete_top10_frame_list = []

'''
Description : Close the Tkinter window and exit the Python program.
Input       : None
Return      : None
'''
def quit_window():    
    window.quit()
    window.destroy()
    sys.exit()


'''
Description : Function to create a folder level daraframe by aggregating the file level datafram created.
Input       : List of all the files and its details in the System Path..
Return      : File level dataframe.
'''
def showGrowthGraph(file_df, window):

	# Delete the top 10 big files frame if it is already present
	for frame in delete_top10_frame_list:
		frame.destroy()
	
	# Delete the graph if it is present already
	for panel in delete_panel_list:
		panel.destroy()
	

	try:

		creat_grpah_indicator = createGrowthGraph(file_df)

		#Show the graph if the graph was created successfully
		if creat_grpah_indicator:
			# Show the image in Tkinter panel
			img = ImageTk.PhotoImage(Image.open('..\\report\\images\\size_growth_graph.png'))  
			panel = Label(window, image = img)
			delete_panel_list.append(panel)
			panel.pack(side=LEFT)
			window.mainloop()

		# Aggregate the size of the files created every day
	except Exception as e:		
		logging.error('Error while plotting the size growth graph and the error is {}'.format(str(e)))
		tkmsg.showinfo(title='Size Growth Grpah', message='Error while plotting the graph. Please check the logs for more details')



'''
Description : Function to create a folder level daraframe by aggregating the file level datafram created.
Input       : List of all the files and its details in the System Path..
Return      : File level dataframe.
'''
def showPredictGrowthGraph(file_df, window):

	# Delete the top 10 big files frame if it is already present
	for frame in delete_top10_frame_list:
		frame.destroy()
	
	# Delete the graph if it is present already
	for panel in delete_panel_list:
		panel.destroy()
	

	try:

		creat_grpah_indicator = predictSizeGrowthGraph(file_df)

		#Show the graph if the graph was created successfully
		if creat_grpah_indicator:
			# Show the image in Tkinter panel
			img = ImageTk.PhotoImage(Image.open('..\\report\\images\\pred_size_growth_graph.png'))  
			panel = Label(window, image = img)
			delete_panel_list.append(panel)
			panel.pack(side=LEFT)
			window.mainloop()

		# Aggregate the size of the files created every day
	except Exception as e:		
		logging.error('Error while plotting the size growth graph and the error is {}'.format(str(e)))
		tkmsg.showinfo(title='Size Growth Grpah', message='Error while plotting the graph. Please check the logs for more details')

'''
Description : Function to export the file and folder level details into an excel.
Input       : File and Folder level dataframes.
Return      : None
'''
def exportExcel(file_df, folder_df):

	export_success_indc = True

	file_df_excel = '..\\export\\FileAndFolderDetails.xlsx'
	try:
		with pd.ExcelWriter(file_df_excel) as writer:
			file_df.to_excel(writer, sheet_name='File Level')
			logging.info('File level details have been exported successfully into an excel sheet at {}'.format(file_df_excel)) 
			folder_df.to_excel(writer, sheet_name='Folder Level')
			logging.info('Folder level aggregation has been xtracted successfully into an excel sheet at {}'.format(file_df_excel))
			
	except Exception as e:
		export_success_indc = False
		logging.error('Error while exporting the file details and the error is {}'.format(str(e)))

	if export_success_indc:
		tkmsg.showinfo(title='Export File Details', message='Successfully exported files and folders details into the \'export\' folder')
	else:
		tkmsg.showerror(title='Export File Details', message='Error while exporting the files. Please check the logs')


'''
Description : Delete the files selected
Input       : File Data Frame and the position of the file.
Return      : Success Indicator
'''
def deleteAllFiles(top_10_files_df):
	delete_success_indc = True
	# Loop through all the check boxes 
	for index, file_details in top_10_files_df.iterrows():
		file_path_arr = file_details[['Folder Name', 'File Name']].values
		file_path = file_path_arr[0]+file_path_arr[1]
		
		try:
			os.remove(file_path)
			logging.info('Deleted the file'+ file_path)	
		except Exception as e:
			delete_success_indc = False
			logging.error('Error while deleting the file the file {} and the error is {}'.format(file_path, str(e)))			


	if delete_success_indc:
		tkmsg.showinfo(title='Delete Selected File', message='Successfully Deleted All Files')
	else:
		tkmsg.showerror(title='Delete Selected File', message='Error while deleting the files. Please check the logs')


'''
Description : Delete the files selected
Input       : File Data Frame and the position of the file.
Return      : Success Indicator
'''
def deleteFiles(top_10_files_df, chk_button_name_dict):
	delete_success_indc = True
	# Loop through all the check boxes 
	for chk_button_name in chk_button_name_dict:
		# Delete the file
		if chk_button_name_dict[chk_button_name].get() == 1:						
			chk_s_no = int(chk_button_name.split('_')[1])
			file_path_arr = top_10_files_df[top_10_files_df['S_No'] ==1][['Folder Name', 'File Name']].values
			file_path = file_path_arr[0][0]+file_path_arr[0][1]			
			
			try:
				os.remove(file_path)
				logging.info('Deleted the file'+ file_path)	
			except Exception as e:
				delete_success_indc = False
				logging.error('Error while deleting the file the file {} and the error is {}'.format(file_path, str(e)))			


	if delete_success_indc:
		tkmsg.showinfo(title='Delete Selected File', message='Successfully Deleted Selected Files')
	else:
		tkmsg.showinfo(title='Delete Selected File', message='Error while deleting the files. Please check the logs')



'''
Description : Display the top 10 big files.
Input       : List of top 10 big files
Return      : System path
'''
def showTop10BigFiles(file_df):

	# Delete the graph if it is present

	for panel in delete_panel_list:
		panel.destroy()
	
	
	# Create a list of top 10 big files 
	top_10_files_list_columns = ['S.No', 'Folder Name', 'File Name', 'Created Date', 'Last Modified Date', 'Size in MB', 'Delete']

	top_10_files_df = file_df.sort_values('Size in MB',ascending=False).head(10).drop('File Type', axis=1)

	# Show a message if the
	
	if len(file_df) < 10:		
		tkmsg.showinfo(title='Show Top 10 Big Files ', message='Less than 10 files to show')	
	
	s_no = list(range(1, len(top_10_files_df)+1))
	
	# List to store serial no of top 10 files.

	
	

	top_10_files_df.insert(0, column='S_No', value=s_no)

	# Add S.No into top_10_files_df

	top_10_files_list = [top_10_files_list_columns] + top_10_files_df.values.tolist()

	#dictionary to hold the check buttons name
	chk_button_name_dict = {}
	
	# Loop through the top 10 big files list and display the same
	for file_index in range(0, len(top_10_files_list)):#Row
		frame_file = Frame(master=window)
		# Add the frame into delete frame list
		delete_top10_frame_list.append(frame_file)
		frame_file.pack(fill=X)	

		for file_detail in top_10_files_list[file_index]: # Column				
			entry_file_detail = Entry(font =body_font, master =frame_file)
			entry_file_detail.insert(0,file_detail)
			entry_file_detail.pack(side=LEFT)

		# Disply the delete button for all the files except the header row.	
		if file_index != 0:
			chk_button_name = 'chk_'+str(file_index)
			chk_button_name_dict[chk_button_name] = IntVar()
			check_delete = Checkbutton(master=frame_file, variable=chk_button_name_dict[chk_button_name], onvalue=1, offvalue=0)			
			check_delete.pack(side=LEFT)


	# Display Delete Button after each row

	frame_delete = Frame(master=window)
	#Add the frame into delete frame list
	delete_top10_frame_list.append(frame_delete)
	frame_delete.pack(fill=X)	
	# Export All Files and Folders Button
	button_delete = Button( text="Delete All 10 Files", fg="purple",  font = body_font, master =frame_delete, command=lambda: deleteAllFiles(top_10_files_df))		
	# Attach Export All Files and Folders Button
	button_delete.pack(side=LEFT, padx=10, pady=10)
	button_delete_selected = Button( text="Delete Selected Files", fg="purple",  font = body_font, master =frame_delete, command = lambda: deleteFiles(top_10_files_df, chk_button_name_dict))		
	# Attach Export All Files and Folders Button
	button_delete_selected.pack(side=LEFT, padx=10, pady=10)
       



'''
Description : Get the system path to analyze from the user.
Input       : None
Return      : System path
'''

def analyzeSystemPath():
	
	#Delete all the frames for new Analyze function
	for frame in delete_frame_list:
		frame.destroy()

	# Delete the top 10 big files frame if it is already present
	for frame in delete_top10_frame_list:
		frame.destroy()

	# Delete the graph if it is present
	for panel in delete_panel_list:
		panel.destroy()
	
	# User entered system path
	system_path = path_entry.get()

	

	# Add '\' at the end of the system path if it is present. This is required to analyze all the subfolders as well.	
	if system_path[-1] !='\\':
		logging.info('Added \\ at the end of the system path.')
		system_path = system_path+'\\'
		
	# Check whether the path is a folder
	if os.path.isdir(system_path):
		logging.info('User has entered {}'.format(system_path))		
			
		# If the System Path is valid then call the function 'extractFileDetails() to get the details of all the files in the input folder/drive' 

		# List to hold all the file details in the user shared system path.
		file_df_list = []
		
		extractFileDetails(system_path, file_df_list)

		logging.info('File list and size have been extracted successfully')

		# Create File level datframe
		file_df = pd.DataFrame(file_df_list, columns=["Folder Name", "File Name", "File Type", "Created Date", "Last Modified Date", "Size in MB"])
		
		logging.info('File level dataframe has been created successfully')

		# Create folder level dataframe
		folder_df = createFolderDataFrame(file_df)
		logging.info('Folder level dataframe has been created successfully')

		# Analyse the file and list down the Report Highlights

		# Report Highlights Section Creation Starts
	
		# Create a list of Report Highlights
		report_highlights_list = []
		# Append size of the shared path
		report_highlights_list.append('Report Highlights:')
		#report_highlights_list.append('1. The total size of the system path is '+ str(file_df['Size in MB'].sum())+'MB.')
		report_highlights_list.append('1. The total size of the system path is '+ str(round(file_df['Size in MB'].sum(),3))+' MB.')
		# Append number off files and folders in the shared path
		report_highlights_list.append('2. There are totally '+ str (folder_df['Folder Name'].count())+ ' folders and '+ str(file_df['File Name'].count())+' files in the shared path.')
		# Append top 10 file size 	
		report_highlights_list.append('3. Deleteing the top 10 big files can save you ~ '+ str(round(file_df.sort_values('Size in MB',ascending=False).head(10) ['Size in MB'].sum(),3))+ ' MB.')

		# Loop through the highlights list and create a frame and a label for each highlight.
		for highlights_text in report_highlights_list:			
			frame_text = Frame(master=window)
			delete_frame_list.append(frame_text)
			frame_text.pack(fill=X)
			label_text = Label(	
			    text=highlights_text,
			    foreground="purple",  # Set the text color to white
			    #background="white",  # Set the background color to black
			    #width=10, # Tkinter uses text units for width and height measurements
			    #height=3,
			    font = body_font,
			    master =frame_text    
			)
			label_text.pack(side=LEFT)

		# Report Download Section Creation Starts
		frame_download = Frame(master=window)
		# Add the from to the delete from list
		delete_frame_list.append(frame_download)
		frame_download.pack(fill=X)	

		# Download Report Button
		button_download_report = Button(
		    text="Download Report",
		    #width=25,
		    #height=1,    
		    fg="purple",
		    font = body_font,
		    master =frame_download,
		    command = lambda: downloadReport(report_highlights_list, file_df)
		)
		# Attach Download Report Button
		button_download_report.pack(side=LEFT, padx=10, pady=10)

			
		# Show Top 10 Big Files Button
		button_top_10_files = Button(
		    text="Show Top 10 Big Files",
		    #width=25,
		    #height=1,    
		    fg="purple",
		    font = body_font,
		    master =frame_download,
		    command = lambda: showTop10BigFiles (file_df)
		)
		# Attach Show Top 10 Big Files Button
		button_top_10_files.pack(side=LEFT, padx=10, pady=10)

		# Export All Files and Folders Button
		button_export = Button(
		    text="Export File Details", fg="purple", font = body_font, master =frame_download, command = lambda: exportExcel(file_df, folder_df))		
		# Attach Export All Files and Folders Button
		button_export.pack(side=LEFT, padx=10, pady=10)

		# Show Growth Chart Button
		button_growth_graph = Button(
		    text="Show Size Growth Graph", fg="purple", font = body_font, master =frame_download, command = lambda: showGrowthGraph(file_df, window))		
		# Attach Export All Files and Folders Button
		button_growth_graph.pack(side=LEFT, padx=10, pady=10)

		# Show Growth Chart Button
		button_predict_growth_graph = Button(
		    text="Predict Size Growth", fg="purple", font = body_font, master =frame_download, command = lambda: showPredictGrowthGraph(file_df, window))		
		# Attach Export All Files and Folders Button
		button_predict_growth_graph.pack(side=LEFT, padx=10, pady=10)
		
	else:
		# Report Download Section Creation Starts		
		tkmsg.showerror(title='System File Analyzer', message='Invalid System Path. Please enter a valid path')
		logging.error('User did not provide a valid path')
		logging.info('Process ended')
		

'''
Description : Main Function
'''
if __name__ == "__main__":
   
	# Initialize Log Files
	logging.basicConfig(
   		filename="..\\logs\\SystemSpaceAnalyzer.log",
   		level=logging.INFO,
   		format="%(asctime)s:%(levelname)s:%(message)s"
    )
	logging.info('Process started')

	# Create a new window
	window = Tk()

	window.title("System File Analyzer")  
	# Create a label to great the user
	# Title font
	title_font = tkFont.Font(family="Lucida Grande", size=20)

	title_label = Label(	
	    text="System File Analyzer",
	    foreground="purple",  # Set the text color to white
	    #background="white",  # Set the background color to black
	    #width=10, # Tkinter uses text units for width and height measurements
	    #height=3,
	    font = title_font
	    
	)
	# Attach the label to the window
	title_label.pack()

	

	# Frame for getting input
	frame_input = Frame(master=window)
	frame_input.pack(fill=X)

	# Font for all the content in the body
	body_font = title_font = tkFont.Font(family="Lucida Grande", size=10)

	path_label = Label(	
	    text="Enter the system path to analyze:",
	    foreground="purple",  # Set the text color to white
	    #background="white",  # Set the background color to black
	    #width=10, # Tkinter uses text units for width and height measurements
	    #height=3,
	    font = body_font,
	    master =frame_input    
	)
	# Attach the path label
	path_label.pack(side=LEFT)
	#path_label.place(x=0,y=0)

	# Entry box for getting the system path
	path_entry = Entry(width=50, font = body_font, master =frame_input)
	# Attach path_entry
	path_entry.pack(side=LEFT)

	# Analyze button for getting Sytem Path
	button_analyze = Button(
	    text="Analyze",
	    #width=25,
	    #height=1,    
	    fg="purple",
	    font = body_font,
	    master =frame_input,
	    command = analyzeSystemPath
	)
	# Attach Analyze button
	button_analyze.pack(side=LEFT, padx=5, pady=5)

	
	# Report Download Section Creation Ends
	window.protocol("WM_DELETE_WINDOW", quit_window)
			
	# Show the window
	window.mainloop()