import time
import os
import sys
import getopt

def usage():
	print ( sys.argv[0] + " -h -v !!!UPRAVIT!!!")

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hr:l:e:d:v", ["help", "repetition=", "logging=", "experiment=", "database=", "verbose"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print (err)
		usage()
		sys.exit(2)
	verbose = False
	repetition = None
	logging = None
	experiment = None
	database = None
	for o, a in opts:
		if o in ("-v", "verbose"):
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-r", "--repetition"):
			repetition = a
		elif o in ("-l", "--logging"):
			logging = a
		elif o in ("-e", "--experiment"):
			experiment = a
		elif o in ("-d", "--database"):
			database = a
		else:
			assert False, "unhandled option."

	if (verbose): 
		print ("---\nVerbose: " + str(verbose) )
		print ("Repetition: " + str(repetition) )
		print ("Logging: " + str(logging) )	
		print ("Experiment: " + str(experiment) )	
		print ("Database: " + str(database) + "\n---" )	
		
		print file_size(str(experiment) + ".conf")

	start_time = time.time()

	file_path = sys.argv[0]
	print os.path.getsize(file_path)
	print file_size(file_path)

	print (file_path)
	print file_size(file_path)
	print(" --- %s seconds ---" % (time.time()-start_time))

if __name__ == "__main__":
	main()
