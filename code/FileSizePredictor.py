import pandas as pd
import numpy as np
import logging
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter.messagebox as tkmsg
from datetime import datetime, date
from tkinter import *
import os
from statsmodels.tsa.arima_model import ARIMA
import warnings
warnings.filterwarnings("ignore")


'''
Description : Function to create a size growth grapah and save it inside the images folder.
Input       : List of all the files and its details in the System Path..
Return      : Success Indicator
'''
def predictSizeGrowthGraph(file_df):

	creat_grpah_indicator = False

	try:
		# Delete if the predicted size grwoth graph is already present
		if os.path.isfile('..\\report\\images\\pred_size_growth_graph.png'):
			os.remove('..\\report\\images\\pred_size_growth_graph.png')		

		# Group by on Created Date to find the size of the file on each day.
		ts_size_in_mb_df = pd.DataFrame(file_df.groupby('Created Date').sum()['Size in MB'])

		# Create a dataframe with the last 5 years date from current month, e.g., if the current month is Oct-2020 then start date  will be 01-Oct-2015 and end date is 01-Oct-2020
		current_date =date.today()
		current_month = datetime(current_date.year, current_date.month, 1).strftime('%Y-%m-%d')
		five_years_ago = datetime(current_date.year-5, current_date.month, 1).strftime('%Y-%m-%d')	
		
		#Create a dataframe using the dates created above.
		size_5yrs_df = pd.DataFrame(index=pd.date_range(start=five_years_ago,end=current_month))


		# Merge both Dataframes and get Size in MB and Aggregated Size in MB for each day in the lat five years.
		size_5yrs_df = pd.merge(size_5yrs_df, ts_size_in_mb_df, left_index=True,right_index=True, how='left')
		size_5yrs_df['Size in MB'].fillna(0, inplace=True)

		# Create the total size added for each month for the last 5 years
		mon_size_5yrs_df = size_5yrs_df['Size in MB'].resample('MS').sum()

		
		# Create a ARIMA model
		model = ARIMA(mon_size_5yrs_df, order=(1,1,1))
		model_fit = model.fit(disp=-1)

		#Predict the size for the next 1 year, e.g., if the current mont his Oct-2020 then predict the size growth from Nov-2020 to Oct-2021.
		pred_start_month = datetime(current_date.year, current_date.month+1, 1).strftime('%Y-%m-%d')
		pred_end_month = datetime(current_date.year+1, current_date.month, 1).strftime('%Y-%m-%d')
		# Predict the size
		pred_ds = model_fit.predict(start=pred_start_month, end=pred_end_month, dynamic=False)


		# Create a new dataframe for calcuating the aggregated size using the data series 'mon_size_5yrs_df'
		mon_agg_size_5yrs_df = pd.DataFrame(mon_size_5yrs_df)
		# Reset datetime index to default index as the index '0' is required for the below logic to calcualte the aggregated size.
		mon_agg_size_5yrs_df.reset_index(level=0, inplace=True)#
		#Rename the index column to Created Date.
		mon_agg_size_5yrs_df.rename(columns={"index": "Created Date"}, inplace=True)

		# Add the last month size with current month to create the aggregated size.
		for i in range(1, len(mon_agg_size_5yrs_df)):
			mon_agg_size_5yrs_df.loc[i, 'Size in MB'] = mon_agg_size_5yrs_df.loc[i-1, 'Size in MB'] + mon_agg_size_5yrs_df.loc[i, 'Size in MB']


		# Last month aggregated size from 'mon_agg_size_5yrs_df' 
		last_month_size = mon_agg_size_5yrs_df.loc[len(mon_agg_size_5yrs_df)-1, 'Size in MB']
		
		# Create a DataFrame using the Predicted Data Series.
		pred_df = pd.DataFrame(pred_ds, columns =['Size in MB'] )
		# Reset datetime index to default index as the index '0' is required for the below logic to calcualte the aggregated size.
		pred_df.reset_index(level=0, inplace=True)
		#Rename the index column to Created Date.
		pred_df.rename(columns={"index": "Created Date"}, inplace=True)
		#Set the first value of pred_df by adding the last month size assigned earlier and predicted size for the month.
		pred_df.loc[0, 'Size in MB'] = last_month_size + pred_df.loc[0, 'Size in MB']
		
		# Calculate the aggregated size using the predict size for each month.
		for i in range(1, len(pred_df)):
			pred_df.loc[i, 'Size in MB'] = pred_df.loc[i-1, 'Size in MB'] + mon_agg_size_5yrs_df.loc[i, 'Size in MB']

		# Plot monthly aggregated size data frame into a graph
		#ax = mon_agg_size_5yrs_df.plot(x='Created Date', y = 'Size in MB', kind = 'line', label='Actual Size (MB)')
		# Plot monthly predicted size data frame on the plot above
		#pred_df.plot(x='Created Date', y = 'Size in MB', kind = 'line', ax=ax, label='Predicted Size (MB)')		
		plt.figure(figsize=(10, 6))
		pred_df.plot(x='Created Date', y = 'Size in MB', kind = 'line',  label='Predicted Size (MB)')		
		
		plt.title('Predicted Size Growth Graph')
		plt.xlabel('Date')
		plt.ylabel('Size (MB)')	

		plt.savefig('..\\report\\images\\pred_size_growth_graph.png')
		logging.info('Graph has been created and stored succuessfull under \\report\\image folder')

		# Set the indicator to True
		creat_grpah_indicator = True

		# Aggregate the size of the files created every day
	except Exception as e:		
		logging.error('Error while plotting the predicted size growth graph and the error is {}'.format(str(e)))
		tkmsg.showinfo(title='Predicted Size Growth Grpah', message='Error while plotting the graph. Please check the logs for more details')
	
	
	#return the creat_grpah_indicator

	return creat_grpah_indicator