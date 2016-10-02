import sys
import os
import pickle

def main():
	path = sys.argv[1]
	length = (len(sys.argv)>2 and sys.argv[2] == '--length')
	if(path.endswith('.pickle')):
		printPickle(path, length)
	else:
		tempID = None
		for(dirpath, dirnames, filenames) in os.walk(path):
			for filename in filenames:
				print('')
				if(filename.endswith('.pickle')):
					tempID = filename.split('.')[0]
					printPickle(os.sep.join([dirpath, filename]), length)
			#endfor
		#endfor
#enddef main

def printPickle(path, length):
	with open(path, "rb") as handle:
		deviceID = path.split('/')[-1].split('.')[0]
		allData = pickle.load(handle)
	handle.close()

	print(deviceID + ':')
	print(str(len(allData)))
	if(not length):
		for tup in allData:
			print(str(tup))
		#endfor
	del allData
#enddef printPickle





if __name__ == '__main__':
	main()