import time
import sys
import getopt

from lib.graphdatabases import GraphDB

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

def main():
    #------------------------------ Zpracovani vstupnich argumentu
	print ("start")
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
    
    #------------------------------ Nacitani konfigu
    
		
	#------------------------------ Spusteni testu
	start_time = time.time()
	
	g = GraphDB()
	s = convert_bytes(g.dbSize())
	print ( s) 
	result = g.dbQuery("select * from Animal")
	print(result)
	
	print(" --- %s seconds ---" % (time.time()-start_time))
	#------------------------------

if __name__ == "__main__":
	main()