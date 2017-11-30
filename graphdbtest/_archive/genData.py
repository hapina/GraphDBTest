import sys
import getopt

def usage():
	print ( sys.argv[0] + " -f -e -d -v -h !!!UPRAVIT!!!")

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "f:e:d:vh", ["file=", "experiment=", "database=", "verbose", "help"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print (err)
		usage()
		sys.exit(2)
	
	outFile = None
	experiment = None
	database = None
	verbose = False

	for o, a in opts:
		if o in ("-v", "verbose"):
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-f", "--file"):
			outFile = a
		elif o in ("-e", "--experiment"):
			experiment = a
		elif o in ("-d", "--database"):
			database = a
		else:
			assert False, "unhandled option."

	if (verbose): 
		print ("---")
		print ("Verbose: " + str(verbose) )
		print ("outFile: " + str(outFile) )	
		print ("Experiment: " + str(experiment) )	
		print ("Database: " + str(database))
		print ("---")	

if __name__ == "__main__":
	main()
