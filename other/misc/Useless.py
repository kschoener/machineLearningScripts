from sklearn import svm
from sklearn import datasets
from sklearn import neighbors
import numpy as np
import GraphData
from datetime import datetime
def main():
	#testing the sorted function
	# sortedTest()
	#end testing

	#testing predictors on small datasets
	# predictorTest()
	#end testing

	#testing converting dict to list then sorting
	# dictToListTest()
	#end testing

	#testing comparison of list to empty list
	# listCompTest()
	#end testing

	#testing using another file and inputting args
	# gDataTest()
	#end testing

	#testing list splitting
	# listSplitTest()
	#end testing

	#testing fit/predict inputs
	# predictFitTest()
	#end testing

	#testing datetime things
	# datetimeTesting()
	#end testing

	#testing int to float and visa versa
	# intFloatTest()
	#end testing

	#testing delete and join
	joinDeleteTest()
	#end testing

#enddef main

def joinDeleteTest():
	path = '/kschoener6/Documents/Work/PhoneLab/Data/OldData/pickles/allPickles/ekadkhg47579ej.pickle'
	# split = path.split('/')
	# print('Split before delete: '+str(split))
	# del split[-1]
	# print('Split after delete: '+str(split))
	# directoryPath = '/'.join(split)
	directoryPath = '/'.join(path.split('/')[:-1])
	print(str(path))
	print(str(directoryPath))
#enddef joinDeleteTest

def intFloatTest():
	hour = 21
	minute = 99
	timeStr = str(hour) + '.' + str(minute)
	time = float(timeStr)
	print(str(time))
	print(str(int(time)))
	print('time (float) modulo 1 = '+str(time%1))
#enddef intFloatTest

def datetimeTesting():
	import datetime
	dayObj = datetime.date(2016,6,27)
	dayCompObj = datetime.date(2016,6,27)
	print('Comparison of the same day yields: '+str(dayObj == dayCompObj))
	print('Year: ',str(dayObj.year))
	print('Month: ',str(dayObj.month))
	print('Day: ',str(dayObj.day))
	print('Weekday num: ',str(dayObj.weekday()))
	weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	print('Weekday realization: ',str(weekdays[dayObj.weekday()]))
#enddef datetimetesting

def predictFitTest():
	iris = datasets.load_iris()
	iris_X = iris.data
	iris_y = iris.target

	iris_X_list = [list(arr) for arr in iris_X]
	print(str(iris_X_list)+'\n\n\n\n')

	np.random.seed(0)
	indices = np.random.permutation(len(iris_X))
	iris_X_train = iris_X[indices[:-10]]
	print(str(list(iris_X_train))+'\n')
	iris_y_train = iris_y[indices[:-10]]
	print(str(list(iris_y_train))+'\n')
	iris_X_test  = iris_X[indices[-10:]]
	print(str(list(iris_X_test))+'\n')
	iris_y_test  = iris_y[indices[-10:]]
	print(str(list(iris_y_train))+'\n\n')

	classifier = svm.SVC()
	classifier.fit(iris_X_train, iris_y_train)
	print(str(classifier.predict(iris_X_test)))
	print(str(iris_y_test))
#enddef predictFitTest


def listSplitTest():
	test = list(range(24))# 0 through 23
	print(str(test))
	test1 = test[3:-1] #3 through 22
	print(str(test1))

	num = '245.96'
	val = int(num)
	print(num)
	print(str(val))
#enddef listSplitTest

def gDataTest():
	# test = GraphData('../pickles/0031e78c899fbc79f2d44a0db30f30a8acdf8767.pickle', 'together', '0', '1', '2', '3', '4')
	test = GraphData
	return
#enddef gDataTest



def listCompTest():
	testList1 = ['a', 'b', 'c']
	testList2 = []
	print(str(testList1) + ' == []: ' + str(testList1==[]))
	print(str(testList2) + ' == []: ' + str(testList2==[]))
#enddef listCompTest



def dictToListTest():
	testDict = {}
	n = 10
	for x in range(n):
		testDict[x] = (n-x)

	print(str(testDict))
	testDict = list(testDict.items())
	print(str(testDict))
	print(str(sorted(testDict, key=lambda x: x[1])))
#enddef dictToListTest



def predictorTest():
	print('\nPrint test: ')
	print(str([tup[0] for tup in test]))
	print('Print test end.\n')

	X = [[0.,0.],[0.,0.],[10.,10.],[20.,20.],[30.,30.]]
	y = [20.,30.,20.,10.,0.]
	X = []
	y = []
	for x in range(200):
		X.append([0,0])
		y.append(x%7)

	for x in range(200):
		X.append([40,40])
		y.append((x%7)+14)

	#SVC accounts for outliers

	print('SVC fit prediction:')
	clf = svm.SVC()
	clf.fit(X,y)
	print(str(clf.predict([[0.,0.]])))
	print(str(clf.predict([[10.,10.]])))
	print(str(clf.predict([[20.,20.]])))
	print(str(clf.predict([[30.,30.]])))
	print(str(clf.predict([[40.,40.]])))

	print('k Nearest neighbors fit prediction:')
	knn = neighbors.KNeighborsClassifier()
	knn.fit(X,y)
	print(str(knn.predict([[0.,0.]])))
	print(str(knn.predict([[10.,10.]])))
	print(str(knn.predict([[20.,20.]])))
	print(str(knn.predict([[30.,30.]])))
	print(str(knn.predict([[40.,40.]])))
#enddef predictorTest



def sortedTest():
	test = []
	numList = range(75)
	for i in range(len(numList)):
		test.append([i, numList[-i]])
	# print(str(test))
	test = sorted(test, key=lambda x: x[1])
	# print(str(test))
#enddef sortedTest






if __name__ == '__main__':
	main()
