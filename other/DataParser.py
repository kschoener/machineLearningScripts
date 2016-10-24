from datetime import datetime
import json
import sys
import os
import matplotlib
import pickle

deviceIDDict = {}
minYear = 2013
maxYear = 2016

#$ 	python3 	DataParser.py 	pathToData	pathForPicklesToBeSaved
def main():
	givenPath = sys.argv[1]
	savePath = sys.argv[2]
	setUpPickles(givenPath, savePath)
	saveToPickle(savePath)
#enddef main


def saveCurrentID(savePath, deviceID):
	global deviceIDDict
	with open(savePath+deviceID+'.pickle', "wb") as handle:
		pickle.dump(deviceIDDict[deviceID], handle)
	handle.close()
	del deviceIDDict[deviceID]
#enddef saveCurrentID


def setUpPickles(givenPath, savePath):
	global deviceIDDict
	deviceIDDict = {}
	tempID = None
	#if a pickle for the device was already made (in the save pickle )directory, skip everything with its name
	skipIds = []
	for(dirpath, dirnames, filenames) in os.walk(savePath):
		for filename in filenames:
			skipIds.append(filename.split('.')[0])
		#endfor
	#endfor
	#this is for each device
	for(dirpath, dirnames, filenames) in os.walk(givenPath):
		if(tempID == None):
			print(dirpath)
			tempID = dirpath.split('/')[1]
			print("Setting up device "+tempID+" ...")
		if(tempID != dirpath.split('/')[1]):
			print("Finished setting up device "+tempID+" ...")
			print("Saving "+tempID+" ...")
			if(tempID in deviceIDDict ):
				saveCurrentID(savePath, tempID)
				print("Finished saving "+tempID)
			else:
				print("No data found for "+tempID+" ...")
			print(dirpath)
			tempID = dirpath.split('/')[1]
			print("\nSetting up device "+tempID+" ...")
		if(tempID in skipIds):
			continue
		#endif
		#this is for one month
		for filename in filenames:
			#this is for one day
			if(filename.endswith('.out')):
				input_file = os.sep.join([dirpath, filename])
				times = []
				with open(input_file) as handle:
					badYear = False
					for line in handle:
						if(badYear):
							break
						line = line.strip()
						lineSplit = line.split('\t')
						if(lineSplit[-2] == 'Power-Battery-PhoneLab'):
							try:
								jsonObj = json.loads(lineSplit[-1])
							except:
								continue
							if('BatteryProperties' not in jsonObj):
								continue
							batteryProperties = jsonObj['BatteryProperties']
							status = batteryProperties['Status']# if 'Status' in batteryProperties else "N/A"
							level = batteryProperties['Level']# if 'Level' in batteryProperties else "N/A"
							try:
								temp = datetime.strptime(lineSplit[3], '%Y-%m-%d %H:%M:%S.%f')
								if(temp.year < minYear or temp.year > maxYear):
									badYear = True
									break
								#endif
								times.append([lineSplit[3], status, level])
							except:
								for piece in lineSplit:
									try:
										temp = datetime.strptime(piece, '%Y-%m-%d %H:%M:%S.%f')
										if(temp.year < minYear or temp.year > maxYear):
											badYear = True
											break
										#endif
										times.append([piece, status, level])
										break
									except:
										continue
							#end try
						#endif
					#endfor
				#endwith
				handle.close()
				try:
					times.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S.%f'))
				except:
					print('Time format error at:\n'+dirpath+'\n')
					for entry in times:
						print(str(entry))
					sys.exit(1)
					return
				#end try block
				deviceID = dirpath.split('/')[1]
				if(deviceID not in deviceIDDict):
					deviceIDDict[deviceID] = []
				#endif
				deviceIDDict[deviceID].extend(times)
				deviceIDDict[deviceID].sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S.%f'))
			#endif
		#endfor filenames
	#endfor walk
#enddef setUpPickles


def saveToPickle(savePath):
	global deviceIDDict
	for deviceID in deviceIDDict:
		with open(savePath+deviceID+'.pickle', "wb") as handle:
			pickle.dump(deviceIDDict[deviceID], handle)
		handle.close()
#enddef saveToPickle





















if __name__ == '__main__':
	main()
