import sys
import os
import gzip

#given a path, uncompress all .out.gz files in directory
#$: python3 UncompressGZ.py pathToGZippedFiles/ '.outputExtension'
def main():
	givenPath = sys.argv[1]
	if(len(sys.argv) > 2):
		outputExtension = sys.argv[2]
	else:
		outputExtension = '.out'

	for(dirpath, dirnames, filenames) in os.walk(givenPath):
		print('Starting uncompressing on '+str(dirpath))
		for filename in filenames:
			if(filename.endswith('.gz')):
				input_file = gzip.open(os.sep.join([dirpath, filename]), 'rb')
				
				output_file = filename.split('.')[0]+outputExtension
				output_file = os.sep.join([dirpath, output_file])

				with open(output_file, "w") as handle:
					handle.write(input_file.read().decode("utf-8"))
				#endwith
				handle.close()
			#endif
		#endfor
	#endfor walk
#enddef main
# $find . -name *gz -type f -delete
#this deletes all files of type gz in all subdirectories of the current directory

if __name__ == '__main__':
	main()
