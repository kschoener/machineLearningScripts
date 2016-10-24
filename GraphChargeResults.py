import sys
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

'''
this will take the test results from a device
plot it as time of day vs accuracy

need separate plots for different daytypes
'''
#inputs (LevelPredict) -> dayType, hour, minute

inputpath = None
save = False
show = False
outputpath = None
deviceId = None

graphTitle = None

resultData = None

testSize = None


#python3 GraphResults.py path/to/pickle(s) level(or)charge optional:show optional:save if save: path/to/output(optional)
def main():
	global inputpath
	global testSize
	path = sys.argv[1]

	if(not path.endswith('pickle')):
		paths = []
		for item in os.listdir(path):
			if (os.path.isfile(os.path.join(path, item)) and str(item).endswith('.pickle')):
				paths.append(os.path.join(path, item))
				#endif
			#endfor
		#endfor
		#if you want to test random n devices, add the number at the end of the command
		specificSize = False
		try:
			testSize = int(sys.argv[-1])
			specificSize = True
		except:
			testSize = len(paths)
	else:
		inputpath = path
		execute(sys.argv)
	#endif
#enddef main

def execute(args):
	global deviceId
	global save
	global show
	global outputpath
	global resultData
	global graphTitle
	deviceId = inputpath.split('/')[-1].split('.')[0]
	graphTitle = deviceId
	#if you want to save the graph
	save = (args[-2] == 'save')
	#if you want to see the graph
	show = ('show' in args[1:])
	#endif
	if(save):
		try:
			outputpath = args[-1]
		except:
			outputpath = inputpath
		#end try block
	#endif
	getData()
	# print(str(resultData)+'\n')
	if(resultData != None and len(resultData)>1):
		print('Valid data')
		resultData = resultData[1:]
		setUpComparisonPlot()
		# setUpDifferenceVsTime()
		# setUpDifferenceVsBatteryLevel()
		# setUpDifferenceVsDay()
		if(show and not save):
			plt.show()
		elif(show and save):
			savePlot()
			plt.show()
		elif(save and not show):
			savePlot()
	else:
		print('Invalid data was given')
	#endif
#enddef execute

#x1 is time of day, y1 is expected
#x2 is time of day, y2 is expected
#only for charge session
def setUpComparisonPlot():
	global graphTitle
	#resultData[0] == deviceId
	#resultData[1:] == [inputList, target, prediction]
	#inputs (ChargeSession) -> dayType, batteryLevel, timeInMinutes
	x = []
	yTarget = []
	yPrediction = []
	for test in resultData:
		inputs = test[0]
		inputs = list(test[0])
		target = test[1]
		prediction = test[2]
		x.append(inputs[2]) #time in minutes
		yTarget.append(target)
		yPrediction.append(prediction)
	#endfor
	fig = plt.figure()
	graphTitle = "Comparative results for "+str(deviceId)
	fig.suptitle(graphTitle)
	ax1 = fig.add_subplot(111)

	#set yTarget to red
	ax1.scatter(x, yTarget, s=10, c='r', marker='s', label='Targets')
	#set yPrediction to green
	ax1.scatter(x, yPrediction, s=10, c='g', marker='o', label='Predictions')

	ax1.set_xlabel('Time of Day (mins)')#.set_rotation(-45)
	ax1.set_ylabel('Time to Next Charge (mins)')

	plt.legend(loc='upper left')
	plt.gcf().canvas.set_window_title(graphTitle)
#enddef setUpCompPlot

def setUpDifferenceVsTime():
	global graphTitle
	#inputs (ChargeSession) -> dayType, batteryLevel, timeInMinutes
	x = []
	yDifference = []
	for test in resultData:
		inputs = np.array(test[0])
		target = test[1]
		prediction = test[2]
		x.append(inputs[2]) #time in minutes
		yDifference.append(prediction-target)
	#endfor
	fig = plt.figure()
	graphTitle = "DifferenceVsTime results for "+str(deviceId)
	fig.suptitle(graphTitle)
	ax1 = fig.add_subplot(111)

	ax1.scatter(x, yDifference, s=10, c='r', marker='s', label='Differences')

	ax1.set_xlabel('Time of Day (mins)')#.set_rotation(-45)
	ax1.set_ylabel('Difference Between Prediction and Actual (mins)')

	plt.legend(loc='upper left')
	plt.gcf().canvas.set_window_title(graphTitle)
#enddef setUpDifferenceVsTime

#x is the batteryLevel, y is accuracy (difference)
def setUpDifferenceVsBatteryLevel():
	global graphTitle
	#inputs (ChargeSession) -> dayType, batteryLevel, timeInMinutes
	x = []
	yDifference = []
	for test in resultData:
		inputs = np.array(test[0])
		target = test[1]
		prediction = test[2]
		x.append(inputs[1]) #batteryLevel
		yDifference.append(prediction-target)
	#endfor
	fig = plt.figure()
	graphTitle = "DifferenceVsLevel results for "+str(deviceId)
	fig.suptitle(graphTitle)
	ax1 = fig.add_subplot(111)

	ax1.scatter(x, yDifference, s=10, c='r', marker='s', label='Differences')

	ax1.set_xlabel('Battery Level')#.set_rotation(-45)
	ax1.set_ylabel('Difference Between Prediction and Actual (mins)')

	plt.legend(loc='upper left')
	plt.gcf().canvas.set_window_title(graphTitle)
#enddef setUpAccuracyPlot

#x is daytype//time, y is accuracy
def setUpDifferenceVsDay():
	global graphTitle
	#inputs (ChargeSession) -> dayType, batteryLevel, timeInMinutes
	xs = [[],[],[]]
	ys = [[],[],[]]
	for test in resultData:
		inputs = np.array(test[0])
		dayType = int(inputs[0])
		target = test[1]
		prediction = test[2]

		xs[dayType].append(inputs[2]) #timeInMinutes
		ys[dayType].append(prediction-target)
	#endfor
	fig = plt.figure()
	graphTitle = "DifferenceVsLevel results for "+str(deviceId)
	fig.suptitle(graphTitle)
	ax1 = fig.add_subplot(111)

	ax1.scatter(xs[0], ys[0], s=10, c='r', marker='s', label='DayType 0')
	ax1.scatter(xs[1], ys[1], s=10, c='b', marker='s', label='DayType 1')
	ax1.scatter(xs[2], ys[2], s=10, c='g', marker='s', label='DayType 2')

	ax1.set_xlabel('Time of Day (mins)')#.set_rotation(-45)
	ax1.set_ylabel('Difference Between Prediction and Actual (mins)')

	plt.legend(loc='upper left')
	plt.gcf().canvas.set_window_title(graphTitle)
#enddef setUpDayAccuracyPlot

#TODO:
'''
--draw a line for when the device is charging -- actually  can't because different days
'''


def savePlot():
	global graphTitle
	graphTitle = graphTitle.replace(" ","_")
	graphTitle = graphTitle.lower()
	plt.savefig(outputpath+graphTitle+'.png', bbox_inches='tight')
#enddef save


def getData():
	global resultData
	resultData = []
	with open(inputpath, "rb") as handle:
		resultData = pickle.load(handle)
	handle.close()
#enddef getData




if __name__ == '__main__':
	main()
