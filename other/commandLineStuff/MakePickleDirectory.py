import sys
import os

'''
I made this script to make a directory for each deviceID pickle and then place
said pickle inside the new directory
'''
def main():
	originalPath = sys.argv[1]
	for (dirpath, dirnames, filenames) in os.walk(originalPath):
		currentDirectory = dirpath.split('/')[-1]
		for filename in filenames:
			pickleData = None
			if(filename.endswith('.pickle')):
				deviceID = filename.split('.')[0]
				if (deviceID == currentDirectory):
					print('Path already created for '+str(deviceID)+'. At '+str(dirpath))
					print('Breaking...')
					break
				print('dirpath = '+str(dirpath))
				print('deviceID = '+str(deviceID))
				newPath = dirpath +'/'+ str(deviceID)
				if not os.path.exists(newPath):
					print('Made new directory for '+str(deviceID)+'. At '+str(newPath))
					os.makedirs(newPath)
				#endif
				move(os.sep.join([dirpath, filename]), os.sep.join([newPath,filename]))
			#endif
		#endfor
	#endfor walk
#enddef main




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