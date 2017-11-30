import time
import sys
import getopt

from orientdb.orientdb_api import GraphDB
from setupConfiguration import Configuration

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
    print("---")
    if __debug__:
        print (">>> start in debug mode")      
    start_time = time.time()
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
    
    if args:
        dbConf = args[0]
        exConf = args[1]

    if (verbose) or __debug__: 
        print (">>> Verbose: " + str(verbose) )
        print (">>> Repetition: " + str(repetition) )
        print (">>> Logging: " + str(logging) )
        print (">>> Experiment: " + str(experiment) )
        print (">>> Database: " + str(database))
    
    # Configuration
    if __debug__:
        print (">>> " + dbConf)
        print (">>> " + exConf)
        
    exper = Configuration(exConf)
    exper.setupConf()  
    gdbName = exper.get('dbname')
    experimentType = exper.get('name')
    commands = []
    commands = exper.get('commands').split("|")
    
    # Graph database inicialization
    if dbConf=="orientdb":
        g = GraphDB(gdbName)
        g.setup()
    elif dbConf=="titandb":
        print("Not implemented yet.")
    elif dbConf=="arangodb":
        print("Not implemented yet.")
    else:
        print("Not implemented yet.")
        
    # Choose the type of experiment 
    if experimentType == 'commands':
        if __debug__:
            print(">>> RUN COMMANDS")
        if not g.runCommand(commands):
            print("WARN: Failed runCommand for " + gdbName)
    elif experimentType == 'createdb':
        print("Not implemented yet.")
    elif experimentType == 'dropdb':
        print("Not implemented yet.")
    elif experimentType == 'importdb':
        print("Not implemented yet.")
    elif experimentType == 'exportdb':
        print("Not implemented yet.")
    else:
        print("Not implemented yet.")    
    
    if __debug__:    
        print(">>> %s seconds" % (time.time()-start_time))
    print("---")
    #------------------------------

if __name__ == "__main__":
    main()
