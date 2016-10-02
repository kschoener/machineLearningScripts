import sys
import pickle
from datetime import datetime
from sklearn import svm
import numpy as np

#python3 helpers/LevelPredict.py path_to/a_pickle.pickle




'''
2 people: habitual (creature of habit), spontaneous(no clear routine)
after finding the level related to time and day
try to increase accuracy by adding in season
after that go for day to day weather
'''

pickleData = []
givenPath = None
deviceID = None

classifier = None
data = []
save = False

testing = True
testX = None
testTarget = None
# meansAndMedians = None




#pickles: 
#‘2016-02-28 19:26:40.341018’ , ‘Charging//Discharging//Full’ , BatteryLevel
#or
#‘2016-02-28 19:26:40.341018’, 2 (charging)//3 (discharging)//5 (full) , BatteryLevel
def main(path=None):
	print('Started initialization...')
	initialize(path)
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
		saveCLF(path)
		print('Finished saving.')
	#endif
#enddef main






#python3 helpers/LevelPredict.py path/To/Pickle.pickle
def initialize(path=None):
	global pickleData
	global givenPath
	global deviceID
	givenPath = sys.argv[1] if path == None else path
	pickleData = []
	deviceID = givenPath.split('/')[-1].split('.')[0]
	with open(givenPath, "rb") as handle:
		pickleData = pickle.load(handle)
	handle.close()
#enddef initialize







def getData():
	import datetime
	global pickleData
	global data
	# global meansAndMedians


	monthDayHourLevels = {}
	for tup in pickleData:
		currentDay = (datetime.datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f'))
		
		# minuteFrac = (currentDay.time().minute/60)
		# timeStr = str(currentDay.time().hour)+'.'+str(minuteFrac)
		# time = float(timeStr)

		minute = currentDay.time().minute
		hour = currentDay.time().hour

		weekdayNum = int(currentDay.weekday())
		dayType = None

		if(weekdayNum == 6):
			dayType = 2
		elif(weekdayNum == 5):
			dayType = 1
		elif(weekdayNum >= 0 and weekdayNum <= 4):
			dayType = 0
		#endif

		#Experiment with the accuracies
		# data.append([[weekdayNum, hour, minute],int(tup[-1])])
		data.append([[dayType, hour, minute],int(tup[-1])])

		# #this converts the hour.minute to hour.0
		# compCurrDay = (str(dayType) +' '+ str(hour)+' '+str(minute))
		# if(compCurrDay not in monthDayHourLevels):
		# 	monthDayHourLevels[compCurrDay] = []
		# monthDayHourLevels[compCurrDay].append(int(tup[-1]))
	#endfor

	# meansAndMedians = {}
	# for key in monthDayHourLevels:
	# 	temp = monthDayHourLevels[key]
	# 	temp = sorted(temp)
	# 	mean = (sum(temp)/float(len(temp)))
	# 	median = temp[int(len(temp)/2)]
	# 	meansAndMedians[key] = [mean, median]
	# #endfor
#enddef getData







'''
X = [dayType, hour, minute]
Y = batteryPercent

where dayType is 0 for weekday, 1 for saturday, 2 for sunday or holiday
'''
def fitClassifier():
	global classifier
	global data
	global testing
	global testX
	global testTarget

	testSize = int(len(data)*0.1)

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
	# varianceList = list([])
	differenceList = list([])
	for index in range(len(predictOutput)):
		# meanAndMedian = getAverageAndMedian((str(dayType) +' '+ str(hour)+' '+str(minute)))

		# meanVariance = (abs(predictOutput[index]-meanAndMedian[0])/meanAndMedian[0])*100
		# medianVariance = (abs(predictOutput[index]-meanAndMedian[1])/meanAndMedian[1])*100
		
		# meanDifference = (abs(predictOutput[index]-meanAndMedian[0]))
		# medianDifference = (abs(predictOutput[index]-meanAndMedian[1]))

		# tempVariance = meanVariance if meanVariance < medianVariance else medianVariance
		# varianceList.append(tempVariance)

		# tempDifference = meanDifference if meanDifference < medianDifference else medianDifference
		# differenceList.append(tempDifference)

		# print('Prediction: '+str(predictOutput[index])+'. Target: '+str(testTarget[index])+
		# 	'. Input: '+str(list(testX[index]))+'. Variance: '+str(tempVariance)+' percent'+
		# 	'. Difference: '+str(tempDifference)+' percent'+
		# 	'\nMean, Median (respectively): '+str(meanAndMedian))


		tempDifference = abs( predictOutput[index] - testTarget[index] )
		differenceList.append(tempDifference)
		# print('Input: ' + str(testX[index]) + '. Prediction: ' + str(predictOutput[index]) 
		# 	+ '. Target: ' + str(testTarget[index]) + '. Difference: ' + str(tempDifference) + ' perecent')
	#endfor
	# varianceList = sorted(varianceList)
	# medianVariance = varianceList[int(len(varianceList)/2)]
	# avgVariance = (sum(varianceList))/float(len(varianceList))
	# print('\nsum of variances = '+str(sum(varianceList)))
	# print('length of varianceList = '+str(len(varianceList)))
	# print('\nAverage variance = '+str(avgVariance)+' percent')
	# print('Median variance = '+str(medianVariance)+' percent')

	differenceList = sorted(differenceList)
	medianDifference = differenceList[int(len(differenceList)/2)]
	avgDifference = (sum(differenceList))/float(len(differenceList))
	# avgDifference = np.mean(np.array(differenceList))
	print('\nsum of differences = '+str(sum(differenceList)))
	print('length of differenceList = '+str(len(differenceList)))
	print('\nAverage difference = '+str(avgDifference)+' percent')
	print('Median difference = '+str(medianDifference)+' percent')
#enddef randomPredict





# def getAverageAndMedian(key):
# 	global meansAndMedians

# 	split = key.split(' ')
# 	dayType = int(split[0])
# 	hour = int(split[1])
# 	minute = int(split[2])

# 	if(minute > 59):
# 		minute -= 59
# 		hour += 1
# 	elif(minute < 0):
# 		minute += 59
# 		hour -= 1
# 	#endif

# 	if(hour > 23):
# 		hour -= 23
# 	elif(hour < 0):
# 		hour += 23
# 	#endif

	
# 	# key = str(dayType) +' '+ str(hour)
# 	key = str(dayType) +' '+ str(hour) + ' ' + str(minute)

# 	if(key in meansAndMedians):
# 		return meansAndMedians[key]
# 	else:
# 		# top = getAverageAndMedian((str(dayType) +' '+ str(hour+1)))
# 		# bottom = getAverageAndMedian((str(dayType) +' '+ str(hour-1)))
# 		top = getAverageAndMedian((str(dayType) +' '+ str(hour)+' '+ str(minute+1)))
# 		bottom = getAverageAndMedian((str(dayType) +' '+ str(hour)+' '+ str(minute-1)))
# 		return [(top[0]+bottom[0])/2, (top[1]+bottom[1])/2]
# #enddef getAverageAndMedian






def saveCLF():
	global deviceID
	with open(givenPath.split('.')[0]+'CLF_'+deviceID+'.pickle', "wb") as handle:
			pickle.dump(classifier, handle)
	handle.close()
#enddef saveCLF






if __name__ == '__main__':
	main()