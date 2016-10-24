import Predict as predict
import sys
import pickle



# $python3 helpers/LevelGather.py path/to/pickle
def main(path=None,testing=True, log=True, saveOverride=False, resultPath=None):
	if(path == None):
		path = sys.argv[1]
	#load the pickle data
	pickleData = predict.initialize(path=path)
	#store the necessary data in the proper format
	data = getData(pickleData)
	#fit, predict, test, and save
	(avgDifference, medianDifference, saveList) = predict.main(path,testing,data,log=log)
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

	monthDayHourLevels = {}
	data = []
	for tup in pickleData:
		currentDay = (datetime.datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f'))
		
		# minuteFrac = (currentDay.time().minute/60)
		# timeStr = str(currentDay.time().hour)+'.'+str(minuteFrac).split('.')[-1]
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
	#endfor
	return data
#enddef getData





if __name__ == '__main__':
	main()