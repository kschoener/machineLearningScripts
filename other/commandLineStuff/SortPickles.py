import sys
import os
import pickle
import datetime


pathToPickles = None

'''
This file sorts the pickles of each deviceID by the number of days of data we have for that device
At this point I am using 10 as the increment for sorting

$ python3 helpers/SortPickles.py path/to/pickles
'''
def main():
	global pathToPickles
	pathToPickles = sys.argv[1]
	for (dirpath, dirnames, filenames) in os.walk(pathToPickles):
		if(pathToPickles != dirpath):
			print(str(pathToPickles) + ' != ' +str(dirpath))
			print('Skipping...')
			continue
		#endif
		print(str(pathToPickles) + ' == '+str(dirpath))
		print('Moving to files...')
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

				numOfDays = dayCount(pickleData)
				'''
				depending on what you want to do, leave the correct definition uncommented and the
				others commented
				'''
				# moveByMultipleOf10(numOfDays, dirpath, filename)
				removeLessThanX(x=150, numOfDays=numOfDays, 
					dirpath=dirpath, filename=filename)
			#endif
		#endfor
	#endfor walk
#enddef main

'''
os.remove(path/to/file) removes a file
os.rmdir(path/to/directory) removes an empty directory
shutil.rmtree(path/to/directory) removes a directory and all its contents
'''
def removeLessThanX(x, numOfDays, dirpath, filename):
	if(numOfDays < x):
		print('Removing '+str(filename))
		os.remove( os.sep.join( [ dirpath[:-1] ,filename ] ) )
#enddef removeLessThanX


def moveByMultipleOf10(numOfDays, dirpath, filename):
	newDirectoryNumber = numOfDays + (10 - numOfDays % 10)
	newPath = pathToPickles + str(newDirectoryNumber)
	if not os.path.exists(newPath):
		os.makedirs(newPath)
	#endif
	move(os.sep.join([dirpath[:-1], filename]), os.sep.join([newPath,filename]))
#enddef moveByMultipleOf10



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





def move(oldPath, newPath):
	#python3 MovePickles.py pathToPickles
	line = oldPath.split('/')[-1]
	try:
		os.rename(oldPath, newPath)
		print('Moved '+line+' from '+oldPath+' to '+newPath)
	except Exception as e:
		print(str(e))
		print('AN ERROR OCCURED moving '+str(line)+' from '+str(oldPath)+' to '+str(newPath))
	#end try block
#enddef move





if __name__ == '__main__':
	main()