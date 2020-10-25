import os
import logging
import math
import traceback
import time
from datetime import datetime


'''
Description : Function will write the size of all the files present in the input folder
Input       : System Path under which all the files need to be sized.
Output      : List of all the files and its details in the System Path.
'''

def extractFileDetails(system_path, file_df_list):		
	
    #List of all the files in the drive
	file_list = os.listdir(system_path)	
	
	# Loop through each item from the above list
	for file_name in file_list:
		try:
			file_path = system_path + file_name
            # Check whether the file is a folder or a file
			if os.path.isdir(file_path):				
				#if it is a folder, call the function again
				extractFileDetails(file_path + '\\', file_df_list)
			else:
				#find the file size in MB
				file_size = os.stat(file_path).st_size

				# If the file size is less than 1 KB then consider this as 1 KB.
				if file_size < 1024:
					file_size = 0.001
				else:
					file_size = round((file_size / 1048576), 3)
				
				# find the file type
				            	
				file_type = file_name.split('.')[-1]
				# If there is no file type or the file type has more than one word (if there is a space) then populate file type as ''Unknown
				if (file_type is None) or (' ' in file_type):
					file_type = 'Unknown'
				# Created Date
				file_created_date = time.strftime('%Y-%m-%d', time.localtime(os.stat(file_path).st_ctime))
				# Last Modified Date
				file_last_modified_date = time.strftime('%Y-%m-%d', time.localtime(os.stat(file_path).st_mtime))
				#Append the details into a list
				file_df_list.append([system_path, file_name, file_type, file_created_date, file_last_modified_date, file_size])
		except Exception as e:
				logging.error('Error while accessing the file {} and the error is {}'.format(file_path, str(e)))

	