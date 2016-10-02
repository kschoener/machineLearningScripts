import sys
import os


def main():
	#-move for move
	op = sys.argv[1]
	if(op == '-move'):
		move(sys.argv)
	else:
		return

#enddef main

def move(args):
	#python3 recursiveFuncs.py -move fileOfFilenames.txt path/To/CurrentDir/ path/To/NewDir/
	#python3 helpers/RecursiveFuncs.py -move pickles/keepers.txt pickles/unvisited pickles/coh
	path_to_file = args[2]
	path_to_inputDir = args[3]
	path_to_outputDir = args[4]
	with open(path_to_file) as handle:
		for line in handle:
			line = line.strip()
			try:
				os.rename(path_to_inputDir+line, path_to_outputDir+line)
				print('Moved '+line+' from '+path_to_inputDir+' to '+path_to_outputDir)
			except:
				print('\t'+line+" already moved. Either way it isn't here...")
				continue
			#end try block
		#endfor
	#end with
#enddef move







if __name__ == '__main__':
	main()