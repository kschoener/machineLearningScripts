import sys
import os
import pickle
import matplotlib.pyplot as plt

'''
this will take the test results from a device
plot it as time of day vs accuracy

need separate plots for different daytypes
'''

inputpath = None
save = False
show = False
outputpath = None
deviceId = None

formatType = 'level'

inputs = None
targets = None
predictions = None




#python3 GraphResults.py path/to/pickle(s) level(or)charge save path/to/output(optional)
def main():
	global inputpath
	path = sys.argv[1]

	if(not path.endswith('pickle')):
		for(dirpath, dirnames, filenames) in os.walk(path):
			for filename in filenames:
				if(filename.endswith('.pickle')):
					inputpath = os.sep.join([dirpath, filename])
					execute(sys.argv)
				#endif
			#endfor
		#endfor
	else:
		inputpath = path
		execute(sys.argv)

#enddef main



#TODO not finished lmao
def setUpPlot():
	#resultData[0] == deviceId
	#resultData[1:] == [inputList, target, prediction]
	#stored in inputs, targets, predictions respectively
	#inputs (LevelPredict) -> dayType, hour, minute
	#inputs (ChargeSession) -> dayType, batteryLevel, timeInMinutes
	plt.figure().suptitle("Test results for "+str(deviceId))
	plt.gcf().canvas.set_window_title("Test results for "+str(deviceId))
	if(formatType == 'level'):
		x = [((tup[1]*60)+(tup[2])) for tup in inputs]


#enddef setUpPlot




def save():
	plt.savefig(outputpath+deviceId+'.png', bbox_inches='tight')
#enddef save




def getData():
	global inputs
	global targets
	global predictions
	inputs, targets, predictions = [[],[],[]], [[],[],[]], [[],[],[]]
	resultData = None
	with open(inputpath, "rb") as handle:
		resultData = pickle.load(handle)
	for tup in resultData[1:]:
		#adds the data based on dayType
		inputs[tup[0][0]].append(tup[0])
		targets[tup[0][0]].append(tup[1])
		predictions[tup[0][0]].append(tup[2])
	handle.close()
#enddef getData




def execute(args):
	global deviceId
	global save
	global show
	global formatType
	global outputpath
	deviceId = inputpath.split('/')[-1].split('.')[0]
	if('save' in args[1:]):
		save = True
	if('show' in args[1:]):
		show = True
	if('charge' in args[1:]):
		formatType = 'charge'

	#endif
	if(save):
		try:
			outputpath = args[-1]
		except:
			outputpath = inputpath
		#end try block
	#endif
	getData()
	setUpPlot()
	if(save):
		save()
	#endif
#enddef execute

if __name__ == '__main__':
	main()