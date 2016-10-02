import pickle
from sklearn import svm
import numpy as np
import sys




def main(path,testing,data, log=False):
	deviceID = path.split('/')[-1].split('.')[0]
	(classifier, testX, testTarget, clean) = fitClassifier(data, testing, deviceID=deviceID)

	avgDifference = -1
	medianDifference = -1
	saveList = [str(deviceID)]
	if(testing and clean):
		(avgDifference, medianDifference, saveList) = randomPredict(classifier, testX, testTarget, deviceID, log)
	#endif

	# if(save):
	# 	#this saves the classifier (will do once the predictions are accurate)
	# 	saveCLF(path, deviceID, classifier, avgDifference, medianDifference)
	# #endif
	if(not clean):
		print('Not clean finsih with '+str(deviceID))
	else:
		print('Finished '+str(deviceID))
	return (avgDifference, medianDifference, saveList)
#enddef




def initialize(path):
	# print('Started initialization...')
	pickleData = []
	with open(path, "rb") as handle:
		pickleData = pickle.load(handle)
	handle.close()
	# print('Finished initialization.\n')
	return pickleData
#enddef initialize




def fitClassifier(data, testing=True, deviceID='null'):
	# print('Beginning fit...')
	testSize = int(len(data)*0.1)
	testX = None
	testTarget = None

	# print('\tAssigning classifier...')
	classifier = svm.SVC()
	# classifier = svm.SVC(kernel='linear', C=10)
	# classifier = svm.SVC(kernel='poly')
	# classifier = svm.LinearSVC()
	# classifier = svm.SVR()
	# print('\tFinished assigning classifier.')

	# print('\tSeparating data...')
	x = []
	target = []
	for datum in data:
		x.append(np.array(datum[0]))
		target.append((datum[1]))
	#endfor
	x = np.array(x)
	target = np.array(target)
	# print('\tx length: ',str(len(x)),' target length: ',str(len(target)))
	# print('\tData separated...')

	# print('\tFitting data...')
	if(testing):
		indices = np.random.permutation(len(x))
		trainX = x[indices[:-testSize]]
		trainTarget = target[indices[:-testSize]]
		testX = x[indices[-testSize:]]
		testTarget = target[indices[-testSize:]]
		try:
			classifier.fit(trainX, trainTarget)
		except Exception as e:
			print(str(e))
			print('Testing with device '+str(deviceID))
			print('Failed to fit with x and Target sizes of: '+str(len(trainX))+' and '+str(len(trainTarget)))
			return (None, [], [], False)
			# sys.exit(1)
	else:
		try:
			classifier.fit(x, target)
		except Exception as e:
			print(str(e))
			print('Fit without testing device '+str(deviceID))
			print('Failed to fit with x and Target sizes of: '+str(len(x))+' and '+str(len(target)))
			return (None, [], [], False)
			# sys.exit(1)
	# print('\tData fitted...')
	# print('Finished fitting\n')
	return (classifier, testX, testTarget, True)
#enddef fitAndPredict




def randomPredict(classifier, testX, testTarget, deviceID, log=False):
	# print('Beginning random prediction...\n')
	# print('\nRandom selection test:')
	# print('Predicting...')
	predictOutput = list(classifier.predict(testX))
	# print('Prediction complete')
	# print('Calculating error...')
	differenceList = list([])
	#for saving for results
	saveList = list([])
	saveList.append(deviceID)
	for index in range(len(predictOutput)):
		#for saving input, output, expected output
		saveList.append([testX[index], testTarget[index], predictOutput[index]])
		#for calculating differences
		tempDifference = abs( predictOutput[index] - testTarget[index] )
		differenceList.append(tempDifference)
		if(log):
			print('Input: ' + str(testX[index]) + '. Prediction: ' + str(predictOutput[index]) 
				+ '. Target: ' + str(testTarget[index]) + '. Difference: ' + str(tempDifference))
	#endfor
	# print('Finished calculating error.')

	differenceList = sorted(differenceList)
	medianDifference = differenceList[int(len(differenceList)/2)]
	avgDifference = (sum(differenceList))/float(len(differenceList))
	# printStr = ('\nFor device '+str(deviceID))
	# printStr += ('\n\tsum of differences = '+str(sum(differenceList)))
	# printStr += ('\n\tlength of differenceList = '+str(len(differenceList)))
	# printStr += ('\n\tAverage difference = '+str(avgDifference))
	# printStr += ('\n\tMedian difference = '+str(medianDifference))
	# print(str(printStr))
	differenceList = sorted(differenceList)
	while(len(differenceList) > 1000):
		differenceList = differenceList[0::2] #every 2nd item of the list
	# print(str(sorted(differenceList)))

	# print('\nFinished random prediction.\n')
	return (avgDifference, medianDifference, saveList)
#enddef randomPredict










# def saveCLF(givenPath, deviceID, classifier, avgDifference=None, medianDifference=None):
# 	print('Saving classifier...')
# 	with open(givenPath.split('.')[0]+'CLF_'+deviceID+'.pickle', "wb") as handle:
# 		if(avgDifference == None or medianDifference == None):
# 			pickle.dump(classifier, handle)
# 		else:
# 			pickle.dump([classifier, avgDifference, medianDifference], handle)
# 	handle.close()
# 	print('Finished saving.')
# #enddef saveCLF