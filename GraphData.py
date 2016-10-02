import sys
import os
import pickle
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from numpy import arange

pickleData = []
path = None
isolatedDay = None
deviceID = None
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dates = None
levels = None
autonomous = False



#python3 thisFile.py path_to/a_pickle.pickle weekdays(numbers 0-6 Monday-Sunday)
def main():
	global pickleData
	global autonomous
	global deviceID
	#start initialization
	initialize()
	#finished initialization
	
	#start setting up data
	if(autonomous):
		for(dirpath, dirnames, filenames) in os.walk(path):
			for filename in filenames:
				if(filename.endswith('.pickle')):
					deviceID = filename.split('.')[0]
					#get pickle data
					print('Loading pickle of '+str(filename))
					try:
						with open(os.sep.join([dirpath, filename]), "rb") as handle:
							pickleData = pickle.load(handle)
						handle.close()
					except:
						print('There was a problem loading: '+str(filename))
						continue
					#only save relevant data
					getData()
					#set up the plot
					setUpPlot()
					#show the plot
					plt.show()
				#endif
			#endfor
		#endfor walk
	else:	
		getData()
		#finished setting up data

		#start setting up plot
		setUpPlot()
		#finished setting up plot

		#show plot
		plt.show()
	#end if else
#enddef main



def initialize():
	global pickleData
	global path
	global isolatedDay
	global deviceID
	global weekdays
	global autonomous
	
	path = sys.argv[1]
	autonomous = False if path.split('.')[-1]=='pickle' else True
	
	isolatedDay = []
	if(len(sys.argv) > 2):
		for arg in sys.argv[2:]:
			try:
				isolatedDay.append(int(arg))
			except:
				continue
	else:
		isolatedDay = [dayNum for dayNum in range(7)]
	#endif else

	pickleData = []
	if not autonomous:
		deviceID = path.split('/')[-1].split('.')[0]
		with open(path, "rb") as handle:
			pickleData = pickle.load(handle)
		handle.close()
	#endif
#enddef initialize



def setUpPlot():
	global deviceID
	global weekdays
	global isolatedDay
	global dates
	global levels
	days = ''
	for dayNum in isolatedDay:
		if(days == ''):
			days += (weekdays[dayNum]+'s')
		else:
			days += (', '+weekdays[dayNum]+'s')
	plt.figure().suptitle(days+"'s for: "+str(deviceID))
	plt.gcf().canvas.set_window_title(days+"'s for: "+str(deviceID))
	print('We have '+str(len(dates))+' data points')
	plt.scatter(x=dates, y=levels, s=4)
	locations = []
	for x in range(25):
		locations.append(x*60*60*1000000)
	plt.xticks(locations, range(25))
	# plt.tick_params(axis='x',which='both', labelbottom='off')

	plt.xlabel('Hour of the Day')
	plt.ylabel('Battery Percentage (%)')

	axes = plt.gca()
	axes.set_xlim([0,(25*60*60*1000000)])
	axes.set_ylim([0,105])
#enddef setUpPlot



def getData():
	global dates
	global levels
	global pickleData
	global isolatedDay
	dates = []
	levels = []
	currentDay = None
	numberOfDays = 0
	for tup in pickleData:
		if(datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').weekday() in isolatedDay):
			# print(str(datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').weekday()))
			# print(str(datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f')))

			timeInMilli = 0
			timeInMilli += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().hour*60*60*1000000)
			timeInMilli += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().minute*60*1000000)
			timeInMilli += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().second*1000000)
			timeInMilli += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().microsecond)
			dates.append(timeInMilli)
			levels.append(tup[-1])
			if(currentDay == None):
				currentDay = datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f')
			elif(currentDay.date() != datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').date()):
				currentDay = datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f')
				numberOfDays += 1
		#endif
	#endfor
	days = ''
	for dayNum in isolatedDay:
		if(days == ''):
			days += (weekdays[dayNum]+'s')
		else:
			days += (', '+weekdays[dayNum]+'s')
	#endfor
	print('There were '+str(numberOfDays)+' '+days)
#enddef getData



if __name__ == '__main__':
	main()