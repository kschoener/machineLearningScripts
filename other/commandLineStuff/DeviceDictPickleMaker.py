import os
import pickle
import sys
import datetime

# {deviceId : daysOfData}
deviceIdDict = {}

# $ python3 helpers/misc/DeviceDictPickleMaker.py
def main():
	global deviceIdDict
	path_to_pickles = sys.argv[1]
	savePath = sys.argv[2] if len(sys.argv) >= 3 else path_to_pickles

	for (dirpath, dirnames, filenames) in os.walk(path_to_pickles):
		for filename in filenames:
			pickleData = None
			if(filename.endswith('.pickle')):
				deviceID = filename.split('.')[0]
				#get pickle data
				print('Loading pickle of '+str(filename))
				try:
					with open(os.sep.join([dirpath, filename]), "rb") as handle:
						pickleData = pickle.load(handle)
					handle.close()
				except Exception as e:
					print('There was a problem loading: '+str(filename))
					print(str(e))
					continue
				#end try
				numOfDays = dayCount(pickleData)
				print(str(deviceID) + ' had '+str(numOfDays)+' days of data')
				deviceIdDict[deviceID] = numOfDays
			#endif	
		#endfor
	#endfor

	saveDict(savePath)
#enddef main



def dayCount(data):
	count = 0
	dayHolder = None
	for tup in data:
		currentDay = (datetime.datetime.strptime(tup[0], '%Y-%m-%d %H:%M:%S.%f'))
		if((dayHolder == None) or (dayHolder.date() != currentDay.date())):
			dayHolder = currentDay
			count += 1
		#endif
	#endfor
	return count
#enddef dayCount



def saveDict(savePath):
	global deviceIdDict
	with open(savePath+'deviceIdDictNumOfDays.pickle', "wb") as handle:
			pickle.dump(deviceIdDict, handle)
	handle.close()
#endcef saveDict






if __name__ == '__main__':
	main()