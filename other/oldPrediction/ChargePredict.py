import sys
import pickle
from datetime import datetime
from sklearn import svm
import numpy as np


'''
2 people: habitual (creature of habit), spontaneous(no clear routine)
after finding the level related to time and day
try to increase accuracy by adding in season
after that go for day to day weather
'''

pickleData = []
path = None
deviceID = None

classifier = None
data = []
save = False

testing = True
testX = None
testTarget = None



#python3 NewPredict.py path_to/a_pickle.pickle
#currently checking pickles/coh/7699f2734f85c463db41faee43c6964abafed605.pickle
#pickles: 
#‘2016-02-28 19:26:40.341018’ , ‘Charging//Discharging//Full’ , BatteryLevel
#or
#‘2016-02-28 19:26:40.341018’, 2 (charging)//3 (discharging)//5 (full) , BatteryLevel
def main():
	global data
	global save
	global testing

	print('Started initialization...')
	initialize()
	print('Finished initialization.\n')

	print('Starting data setup...')
	getData()
	print('Finished setting up data.\n')

	print('Beginning fit...')
	fitClassifier()
	print('Finished fitting\n')

	if(testing):
		print('Beginning random prediction...\n')
		randomPredict()
		print('\nFinished random prediction.\n')
	#endif

	if(save):
		#this saves the classifier (will do once the predictions are accurate)
		print('Saving classifier...')
		saveCLF()
		print('Finished saving.')
	#endif
#enddef main







def initialize():
	global pickleData
	global path
	global deviceID
	global separatePlots
	path = sys.argv[1]
	pickleData = []
	deviceID = path.split('/')[-1].split('.')[0]
	with open(path, "rb") as handle:
		pickleData = pickle.load(handle)
	handle.close()
#enddef initialize







def getData():
	import datetime
	global pickleData
	global separatePlots
	global data

	weHaveVisited = -1
	#todo find a way to determine charging sessions
	#find a way to store the entries and charging sessions start/end
	#find a way to add this data to the database properly
	for x in range(len(pickleData)):
		if(x < weHaveVisited):
			continue
		#endif

		tup = pickleData[x]
		checkDay = (datetime.datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f'))

		#want to know duration of charge and level change
		chargeSessions = []
		chargeStartTime = None
		chargeEndTime = None
		chargeStartLevel = None
		chargeEndLevel = None
		for y in range(x, len(pickleData)):
			currentDay = (datetime.datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f'))
			if(checkDay.date() != currentDay.date()):
				break
			#endif
			
			#this represents the time as hour.minute
			# minute = str(currentDay.time().minute) if currentDay.time().minute >= 10 
			# 	else ('0'+str(currentDay.time().minute))
			minute = (currentDay.time().minute/60)
			timeStr = str(currentDay.time().hour)+'.'+str(minute)
			time = float(timeStr)

			month = int(currentDay.month)
			dayOfMonth = int(currentDay.day)
			weekdayNum = int(currentDay.weekday())

			dayType = None
			if(weekdayNum == 6):
				dayType = 2
			elif(weekdayNum == 5):
				dayType = 1
			elif(weekdayNum >= 0 and weekdayNum <= 4):
				dayType = 0
			#endif

			batteryLevel = int(tup[2])
			#'Charging','Discharging','Full'
			#'3','2','5'
			chargeStatus = tup[1]
			charging = (chargeStatus == 'Charging' or chargeStatus == '3'
				or chargeStatus == 'Full' or chargeStatus == '5')
			if(chargeStartTime == None and charging):
				chargeStartTime = time
				chargeEndTime = time
				chargeStartLevel = batteryLevel
				chargeEndLevel = batteryLevel
			#endif
			elif(chargeStartTime != None and charging):
				chargeEndTime = time
				chargeEndLevel = batteryLevel
			elif(chargeStartTime != None and not charging):
				if(abs(chargeEndTime-chargeStartTime) > )


			if(y > weHaveVisited):
				weHaveVisited = y
		#endfor

		#todo update this:
		data.append([[month, dayType, time],int(tup[-1])])

		if(x > weHaveVisited):
			weHaveVisited = x
		#endif
	#endfor
#enddef getData







'''
X = [month, dayType, hour.minute, batteryLevel]
Y = nextChargeSession

where dayType is 0 for weekday, 1 for saturday, 2 for sunday or holiday
'''
def fitClassifier():
	global classifier
	global data
	global testing
	global testX
	global testTarget

	testSize = int(len(data)*0.02)
	print('\tAssigning classifier...')
	classifier = svm.SVC()
	# classifier = svm.SVC(kernel='linear', C=10)
	# classifier = svm.SVC(kernel='poly')
	# classifier = svm.LinearSVC()
	# classifier = svm.SVR()
	print('\tFinished assigning classifier.')

	print('\tSeparating data...')
	x = []
	target = []
	for datum in data:
		x.append(np.array(datum[0]))
		target.append(int(datum[1]))
	#endfor
	x = np.array(x)
	target = np.array(target)
	print('\tx length: ',str(len(x)),' target length: ',str(len(target)))
	print('\tData separated...')

	print('\tFitting data...')
	if(testing):
		indices = np.random.permutation(len(x))
		trainX = x[indices[:-testSize]]
		trainTarget = target[indices[:-testSize]]
		testX = x[indices[-testSize:]]
		testTarget = target[indices[-testSize:]]
		classifier.fit(trainX, trainTarget)
	else:
		classifier.fit(x,target)
	print('\tData fitted...')
#enddef fitAndPredict





def randomPredict():
	global classifier
	global testX
	global testTarget

	print('\nRandom selection test:')
	predictOutput = list(classifier.predict(testX))
	varianceList = []
	for index in range(len(predictOutput)):
		month = int(testX[index][0])
		dayType = int(testX[index][1])
		hour = int(testX[index][2])

		# tempTarget = getAverageAndMedian((str(month) +' '+ str(dayType) +' '+ str(hour)))
		tempTarget = testTarget[index]

		variance = (abs(predictOutput[index]-tempTarget[0])/tempTarget[0])*100

		varianceList.append(variance)
		print('Prediction: '+str(predictOutput[index])+'. Target: '+str(testTarget[index])+
			'. Input: '+str(list(testX[index]))+'. Variance: '+str(variance)+' percent')
	#endfor
	avgVariance = 0
	for var in varianceList:
		avgVariance += var
	avgVariance /= len(varianceList)
	print('Average variance = '+str(avgVariance)+' percent')
#enddef randomPredict








def saveCLF():
	daynums = ''
	isolatedDays = sorted(isolatedDays)
	for dayNum in isolatedDays:
		daynums += dayNum
	with open(path.split('.')[0]+'CLF_'+daynums+'.pickle', "wb") as handle:
			pickle.dump(classifier, handle)
	handle.close()
#enddef saveCLF






if __name__ == '__main__':
	main()