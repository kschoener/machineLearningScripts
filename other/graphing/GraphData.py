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
separatePlots = False
autonomous = False

#python3 thisFile.py path_to/a_pickle.pickle separate/together(subplots) weekdays(numbers 0-6 Monday-Sunday)
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
	#endif autonomous
	else:
		if(separatePlots):
			getSeparateData()
		else:
			getData()
		#finished setting up data

		#start setting up plot
		setUpPlot()
		#finished setting up plot

		#show plot
		plt.show()
#enddef main

def initialize():
	global pickleData
	global path
	global isolatedDay
	global deviceID
	global weekdays
	global separatePlots
	global autonomous
	path = sys.argv[1]
	autonomous = False if path.split('.')[-1]=='pickle' else True
	separatePlots = (sys.argv[2] == 'separate') if (len(sys.argv) > 2) else False
	#isolatedDay = int(sys.argv[3]) if (len(sys.argv) > 3 and int(sys.argv[3]) in range(len(weekdays))) else 1
	isolatedDay = []
	if(len(sys.argv) > 3):
		for arg in sys.argv[3:]:
			try:
				isolatedDay.append(int(arg))
			except:
				continue
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
	global separatePlots
	days = ''
	for dayNum in isolatedDay:
		if(days == ''):
			days += (weekdays[dayNum]+'s')
		else:
			days += (', '+weekdays[dayNum]+'s')
	plt.figure().suptitle(days+"'s for: "+str(deviceID))
	plt.gcf().canvas.set_window_title(days+"'s for: "+str(deviceID))
	if(separatePlots):
		print('Number of '+days+': '+str(len(dates)))
		numberOfPlots = len(dates) if len(dates) <= 20 else 20
		print('numberOfPlots is: '+str(numberOfPlots))
		for x in range(numberOfPlots):
			ax1 = plt.subplot(1, numberOfPlots, x+1)
			ax1.plot(dates[x][1:], levels[x][1:])
			if(x != 0):
				plt.gca().axes.get_yaxis().set_visible(False)
			ax1.set_xticklabels([])
			ax1.set_xlabel(str(dates[x][0])).set_rotation(-45)
		#endfor
	else:
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

def getSeparateData():
	global dates
	global levels
	global pickleData
	global isolatedDay
	global separatePlots
	dates = None
	levels = None
	for tup in pickleData:
		if(datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').weekday() in isolatedDay):
			if(dates == None and levels == None):
				dates = []
				tempDates = []
				tempDates.append(str(datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').date()))
				tempDates.append(datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f'))
				dates.append(tempDates)
				levels = []
				tempLevels = []
				tempLevels.append(-1)
				tempLevels.append(tup[-1])
				levels.append(tempLevels)
			elif(dates[-1][1].date() == datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').date()):
				dates[-1].append(datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f'))
				levels[-1].append(tup[-1])
			else:
				tempDates = []
				tempDates.append(str(datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').date()))
				tempDates.append(datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f'))
				dates.append(tempDates)
				tempLevels = []
				tempLevels.append(-1)
				tempLevels.append(tup[-1])
				levels.append(tempLevels)
			#endif else
		#endif
	#endfor
#enddef getSeparateData

def getData():
	global dates
	global levels
	global pickleData
	global isolatedDay
	global separatePlots
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