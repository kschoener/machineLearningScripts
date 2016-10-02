import Predict as predict
import sys
import pickle

'''
found out that you cant have an array of targets
only one value may be predicted from any given input
ex. cant predict [timeTillNextChargeSession, chargeDuration]
also can't use floats, must use ints
'''


# $python3 helpers/LevelGather.py path/to/pickle
def main(path=None,testing=True, log=True, saveOverride=False, resultPath=None):
	if(path == None):
		path = sys.argv[1]
	#load the pickle data
	pickleData = predict.initialize(path=path)
	#store the necessary data in the proper format
	data = getData(pickleData)
	#fit, predict, test, and save
	(avgDifference, medianDifference, saveList) = predict.main(path,testing,data,log)
	if((saveOverride) or (resultPath!=None and input('Save results? y/n') == 'y')):
		saveResults(saveList, resultPath)
#enddef main

def saveResults(saveList, resultPath):
	with open(resultPath+str(saveList[0])+'.pickle', "wb") as handle:
		pickle.dump(saveList, handle)
	handle.close()
#enddef saveResults

#pickles: 
#‘2016-02-28 19:26:40.341018’ , ‘Charging//Discharging//Full’ , BatteryLevel
# or
#‘2016-02-28 19:26:40.341018’, 2 (charging)//3 (discharging)//5 (full) , BatteryLevel
def getData(pickleData):
	import datetime

	data = []
	xData = []
	chargeSessions = []
	#todo find a way to determine charging sessions
	#find a way to map each entry with the next charging session

	'''
	X = [dayType, time, batteryLevel]
	Y = [timeToNextCharge, chargeDuration]
	while looping, add each x (dayType, hour, level) to data
	when a charging session and it's length is determined, add it to a y list (chargeStart, chargeDuration)

	at the end loop through mapping them together like a zipper
	'''
	#want to know duration of charge and level change
	previousLevel = None
	chargeStartTime = None
	chargeEndTime = None
	# chargeStartLevel = None
	# chargeEndLevel = None
	for tup in (pickleData):
		currentDay = (datetime.datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f'))
		
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
			chargeStartTime = currentDay
			chargeEndTime = currentDay
			# chargeStartLevel = batteryLevel
			# chargeEndLevel = batteryLevel
		elif(chargeStartTime != None and (charging or previousLevel > batteryLevel)):
			chargeEndTime = currentDay
			# chargeEndLevel = batteryLevel
		elif(chargeStartTime != None and ((not charging) or previousLevel > batteryLevel)):
			dif = chargeEndTime - chargeStartTime
			chargeDuration = (dif.days * 24 * 60)+(dif.seconds/60) #in minutes
			if(chargeDuration > 5):
				# chargeSessions.append([chargeStartTime, chargeDuration])
				chargeSessions.append(chargeStartTime)
			chargeStartTime = None
			chargeEndTime = None
		#endif

		previousLevel = batteryLevel
		xData.append([dayType, currentDay, batteryLevel])
	#endfor


	'''
	now that we have xData and chargeSessions, we need to put them together
	xData -> [dayType, currentDatetime, batteryLevel]
	chargeSessions -> chargeStartDatetime
	currentDatetime needs to be converted to hour, minute OR timeInMinutes
	chargeStartDatetime needs to be converted to minutesToNextCharge
	'''
	for tup in xData:
		dayType = tup[0]
		currentDay = tup[1]
		batteryLevel = tup[2]

		# chargeStart = chargeSessions[0][0]
		if(chargeSessions):
			chargeStart = chargeSessions[0]
		else:
			break
		while(chargeStart < currentDay and chargeSessions):
			del chargeSessions[0]
			if(chargeSessions):
				# chargeStart = chargeSessions[0][0]
				chargeStart = chargeSessions[0]
			#endif
		#endwhile

		dif = chargeStart - currentDay # time delta object
		timeToNextCharge = int((dif.days * 24 * 60)+(dif.seconds/60)) #time to next charge in minutes

		timeInMinutes = int((currentDay.time().hour*60) + currentDay.time().minute)
		data.append([[dayType, batteryLevel, timeInMinutes],int(timeToNextCharge)])
		# data.append([[dayType, int(currentDay.time().hour), int(currentDay.time().minute), batteryLevel],int(timeToNextCharge)])
	#endfor
	return data
#enddef getData





if __name__ == '__main__':
	main()