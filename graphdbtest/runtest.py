import time
import sys
import getopt

from orientdb.orientdb_api import GraphDB
from setupConf import Configuration

def usage():
    print ( sys.argv[0] + " hr:l:me:d:v !!!UPRAVIT!!!")

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
        opts, args = getopt.getopt(sys.argv[1:], "hr:l:me:d:v", ["help", "repetition=", "logging=", "monitoring", "experiment=", "database=", "verbose"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print (err)
        usage()
        sys.exit(2)
    verbose = False
    repetition = None
    logging = None
    monitoring = False
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
        elif o in ("-m", "--monitoring"):
            experiment = True
        elif o in ("-e", "--experiment"):
            experiment = a
        elif o in ("-d", "--database"):
            database = a
        else:
            assert False, "unhandled option."

    if (verbose) or __debug__: 
        print (">>> Verbose: " + str(verbose) )
        print (">>> Repetition: " + str(repetition) )
        print (">>> Logging: " + str(logging) )
        print (">>> Monitoring: " + str(monitoring) )
        print (">>> Experiment: " + str(experiment) )
        print (">>> Database: " + str(database))
    
    # Configuration
    exper = Configuration(experiment)
    exper.setupConf()  
    gdbName = exper.get('db_name')
    experimentType = exper.get('experiment_type')

    
    # Graph database inicialization
    if database=="orientdb":
        g = GraphDB(gdbName)
        g.setup()
    elif database=="titandb":
        print("Not implemented yet.")
        sys.exit(3)
    elif database=="arangodb":
        print("Not implemented yet.")
        sys.exit(3)
    else:
        print("Not implemented yet.")
        sys.exit(3)
        
    # Choose the type of experiment 
    if experimentType == 'commands':
        commands = []
        commands = exper.get('commands').split("|")
        if __debug__:
            print(">>> RUN COMMANDS")
        if not g.runCommand(commands):
            print("WARN: Failed runCommand for " + gdbName)
    elif experimentType == 'createdb':
        print("Not implemented yet.")
        sys.exit(3)
    elif experimentType == 'dropdb':
        print("Not implemented yet.")
        sys.exit(3)
    elif experimentType == 'importdb':
        print("Not implemented yet.")
        sys.exit(3)
    elif experimentType == 'exportdb':
        print("Not implemented yet.")
        sys.exit(3)
    else:
        print("Not implemented yet.")  
        sys.exit(3)
    
    print("---")
    # Monitoring
    if monitoring:
        print("Not implemented yet.")
                
    if __debug__:    
        print(">>> time: %s seconds" % (time.time()-start_time))
        print(">>> database: %s" % (gdbName))
        print(">>> experiment type: %s" % (experimentType))
        print(">>> experiment: %s" % (experiment))
        print(">>> repetition: %s" % (repetition))
        print(">>> log settings: %s" % (logging))

if __name__ == "__main__":
    main()
