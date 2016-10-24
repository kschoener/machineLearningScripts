import sys
import os
import threading
# $python3 helpers/Multithreading.py pickles/123456.pickle helpers/LevelGather.py path/to/results/
# or
# $python3 helpers/Multithreading.py pickles/123456.pickle helpers/LevelGather.py
# or
# $python3 helpers/Multithreading.py pickles/path/ helpers/LevelGather.py
# or
# $python3 helpers/Multithreading.py pickles/path/ helpers/LevelGather.py path/to/results/
def main():
	#path to all of the pickled data
	picklePath = sys.argv[1]
	#path to where the results will be saved
	resultPath = sys.argv[3] if len(sys.argv) >= 4 else None
	#path to the script to be used for prediction
	dataGatherPath = sys.argv[2]
	dataGatherDir = '/'.join(dataGatherPath.split('/')[:-1])
	#LevelGather or ChargeGather
	dataGatherFilename = dataGatherPath.split('/')[-1].split('.')[0]
	#add the directory of the file to the system path
	sys.path.insert(0,dataGatherDir)
	#assign the import to a variable
	predict = __import__(dataGatherFilename, globals(), locals(), [])
	#delete the directory from the system path - it is no longer needed
	del sys.path[0]

	if(picklePath.endswith('.pickle')):
		print('File given, not Directory')
		predict.main(path=picklePath, testing=True, log=True, saveOverride=False, resultPath=resultPath)
	else:
		skipIds = []
		if(resultPath != None):
			for item in os.listdir(resultPath):
				if (os.path.isfile(os.path.join(resultPath, item)) and str(item).endswith('.pickle')):
					# print(str(item) + ' <-- this will be skipped')
					skipIds.append(str(item)) # saves '2834756438.pickle'
		# print('SkipIds = '+str(skipIds))
		print('Length of skipIds = '+str(len(skipIds)))
		print('A directory was given, going through all of the pickles in the directory')
		skipSize = 0
		for (dirpath, dirnames, filenames) in os.walk(picklePath):
			newFilenames = []
			for filename in filenames:
				if(filename not in skipIds):
					newFilenames.append(filename)
				else:
					skipSize += 1
					#print('Skipping '+str(filename)+' -- already in save path')
			#endfor
			del skipIds
			print('Skipped '+str(skipSize)+' out of '+str(skipSize+len(newFilenames)))
			threadCount = 2

			increment = int(len(newFilenames)/threadCount)
			previousIndex = 0
			iterations = (threadCount-1)
			#if there's a higher thread count than the number of files, make each file its own thread
			if (increment <= 1):
				iterations = (int(len(newFilenames)))
				increment = 1
			for num in range(iterations):
				newIndex = (previousIndex + increment)
				t = threading.Thread(target=predictFiles, args=(dirpath, newFilenames[previousIndex:newIndex], predict, resultPath))
				# t.daemon = True
				t.start()
				previousIndex = newIndex
			#endfor
			finalT = threading.Thread(target=predictFiles, args=(dirpath, newFilenames[previousIndex:], predict, resultPath))
			# finalT.daemon = True
			finalT.start()
		#endfor
#enddef main

def predictFiles(dirpath, fileNameList, predict, resultPath):
	for filename in fileNameList:
		if(filename.endswith('.pickle')):
			if(resultPath == None):
				predict.main(path=os.sep.join([dirpath, filename]),testing=True, log=False, saveOverride=False, resultPath=resultPath)
			else:
				predict.main(path=os.sep.join([dirpath, filename]),testing=True, log=False, saveOverride=True, resultPath=resultPath)
		#endif
	#endfor
#enddef predictFiles


if __name__ == '__main__':
	main()
