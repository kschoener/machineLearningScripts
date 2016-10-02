import sys
import pickle
from datetime import datetime
from sklearn import svm
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

import statistics
from sklearn.preprocessing import Imputer

'''
2 people: habitual (creature of habit), spontaneous(no clear routine)
after finding the level related to time and day
try to increase accuracy by adding in season
after that go for day to day weather
'''


pickleData = []
path = None
isolatedDays = None
deviceID = None
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
timeOfDayMicro = None
levels = None
separatePlots = False

classifier = None
timeHolder = None
finalDb = []

#python3 thisFile.py path_to/a_pickle.pickle weekdays(numbers 1-7)
def main():
	global timeOfDayMicro
	global levels

	machineLearning = True
	graph = True
	save = False

	print('Started initialization...')
	initialize()
	print('Finished initialization.\n')

	print('Starting data setup...')
	getData(machineLearning)
	print('Finished setting up data.\n')

	if(machineLearning):
		print('Beginning fit and predict...')
		fitAndPredict()
		print('Finished predicting')
	else:
		print('Beginning line of best fit...')
		lineOfBestFit()
		print('Line of best fit finished.')

	#this is for graphing predictions for the entire day
	print('Graphing predictions for the entire day')
	if(machineLearning and graph):
		graphDayPrediction(machineLearning)
	elif(not machineLearning and graph):
		graphDayPrediction(machineLearning)
	print('Graphing finished (or never happened)')

	if(machineLearning and save):
		#this saves the classifier (will do once the predictions are accurate)
		print('Saving classifier...')
		saveCLF()
		print('Finished saving.')

#enddef main

#currently checking $ python3 helpers/Testing.py pickles/7699f2734f85c463db41faee43c6964abafed605.pickle 0 1 2 3 4
def initialize():
	global pickleData
	global path
	global isolatedDays
	global deviceID
	global weekdays
	global separatePlots
	path = sys.argv[1]
	isolatedDays = []
	if(len(sys.argv) > 2):
		for arg in sys.argv[2:]:
			try:
				isolatedDays.append(int(arg))
			except:
				continue
	pickleData = []
	deviceID = path.split('/')[-1].split('.')[0]
	with open(path, "rb") as handle:
		pickleData = pickle.load(handle)
	handle.close()
#enddef initialize

def getData(machineLearning):
	global timeOfDayMicro
	global levels
	global pickleData
	global isolatedDays
	global separatePlots
	global timeHolder
	timeOfDayMicro = []
	levels = []
	currentDay = None
	numberOfDays = 0

	dataHolder = []
	timeHolder = {}

	for tup in pickleData:
		#each tup is formatted [datetime, batteryLevel, dis(charging)]
		if(datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').weekday() in isolatedDays):
			if(machineLearning):
			# if(True):
				timeInMilli = 0
				timeInMilli += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().hour*60*60*1000000)
				timeInMilli += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().minute*60*1000000)
				timeInMilli += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().second*1000000)
				timeInMilli += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().microsecond)
				dataHolder.append([timeInMilli, int(tup[-1])])
			else:
			# if(True):
				timeInSeconds = 0
				timeInSeconds += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().hour*60) #removed *60
				timeInSeconds += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().minute) # removed *60
				# timeInSeconds += (datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f').time().second)
				if(timeInSeconds not in timeHolder):
					timeHolder[timeInSeconds] = []
				timeHolder[timeInSeconds].append(int(tup[-1]))
			numberOfDays += 1
		#endif
	#endfor

	if(machineLearning):
	# if(True):
		dataHolder = sorted(dataHolder, key=lambda x: x[0])
		print(str(dataHolder[0]))
		print(str(dataHolder[int(len(dataHolder)/2)]))
		print(str(dataHolder[-1]))
		# levelsInBounds = []
		for tup in dataHolder:
			timeOfDayMicro.append([tup[0],tup[0]])
			levels.append(tup[1])
			# if(tup[0] >= (18.5*60*60*1000000) and tup[0] <= (19.5*60*60*1000000)):
			# 	levelsInBounds.append(tup[1])

		# print(str(levelsInBounds))
	days = ''
	for dayNum in isolatedDays:
		if(days == ''):
			days += (weekdays[dayNum]+'s')
		else:
			days += (', '+weekdays[dayNum]+'s')
	#endfor
	print('There were '+str(numberOfDays)+' '+days)
#enddef getData


'''
It was a big mistake to split the machine learning up by days
This needs to be redone and tried again to test its accuracy against the line of best fit

X = [month, dayType, hour]
Y = batteryPercent

where dayType is 0 for weekday, 1 for saturday, 2 for sunday or holiday
'''
def fitAndPredict():
	global timeOfDayMicro
	global levels
	global classifier
	# classifier = svm.SVC(kernel='linear', C=10)
	# classifier = svm.SVC(kernel='poly')
	# classifier = svm.LinearSVC()
	classifier = svm.SVR()
	print('Finished assigning classifier.\n')

	print('Length of time of day list: '+str(len(timeOfDayMicro)))
	print('Length of battery level list: '+str(len(levels)))
	print('')
	print('Fitting data...')
	classifier.fit(timeOfDayMicro, levels)
	print('Finished fitting.\n')
	print('Running prediction of 7pm...')
	prediction = classifier.predict([[19*60*60*1000000,19*60*60*1000000]])
	print('Predicted level for 7pm: '+str(prediction)+'\n')
	print('Predicted level for 12pm: '+str(classifier.predict([[12*60*60*1000000,12*60*60*1000000]])))
	print('\n\nThe score of the fit is: '+ str(classifier.score(timeOfDayMicro, levels)) + '\n')
#enddef fitAndPredict







def graphDayPrediction(machineLearning):
	global classifier
	global finalDb
	allTimesOfDay = range(24*60) if not machineLearning else range(24*60*60)
	predictedLevels = []
	print('Length of allTimesOfDay: '+str(len(allTimesOfDay)))
	for time in allTimesOfDay:
		if(finalDb == []):
			predictedLevels.append(classifier.predict([[((time*1000000)+(24*60*60)),((time*1000000)+(24*60*60))]]))
		else:
			predictedLevels.append(finalDb[time][1])
	#endfor
	print('Length of predictedLevels: '+str(len(predictedLevels)))
	plt.scatter(x=allTimesOfDay, y=predictedLevels, s=4)


	locations = []
	for x in range(25):
		locations.append(x*60*60)
	#endfor
	plt.xticks(locations, range(25))
	# plt.tick_params(axis='x',which='both', labelbottom='off')

	plt.xlabel('Hour of the Day')
	plt.ylabel('Battery Percentage (%)')

	axes = plt.gca()
	axes.set_xlim([0,(25*60*60)])
	axes.set_ylim([0,105])

	plt.show()
#enddef graphDayPrediction

def saveCLF():
	daynums = ''
	isolatedDays = sorted(isolatedDays)
	for dayNum in isolatedDays:
		daynums += dayNum
	with open(path.split('.')[0]+'CLF_'+daynums+'.pickle', "wb") as handle:
			pickle.dump(classifier, handle)
	handle.close()
#enddef saveCLF

def lineOfBestFit():
	global timeHolder
	global finalDb
	finalDb = []
	for x in range(24*60): #removed *60
		if(x in timeHolder):
			finalDb.append([x, statistics.median(timeHolder[x])])
		else:
			finalDb.append([x, np.nan])
	#endfor

	imp = Imputer(missing_values='NaN', strategy='median')#axis=0
	imp.fit(finalDb)
	finalDb = imp.transform(finalDb)

	# print('Levels around 7pm:')
	# print(str(finalDb[((19*60)-(15)):((19*60)+(15))])) #removed *60 from each

	finalDb = np.array(finalDb)

	x = finalDb[:,0]
	y = finalDb[:,1]

	#the number should probably be dynamic
	#3 and 5 are very accurate for the test
	z = np.polyfit(x, y, 3)
	f = np.poly1d(z)

	x_new = np.linspace(start=x[0], stop=x[-1],num=len(finalDb))
	y_new = f(x_new)

	plt.plot(x,y,'.',x_new,y_new)
	plt.xlim(0, 24*60)
	plt.show()
#enddef lineOfBestFit

if __name__ == '__main__':
	main()

