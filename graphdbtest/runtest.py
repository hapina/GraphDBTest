import time
import sys
import getopt

from orientdb.main import GraphDB
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

    if __debug__:
        print (">> start in debug mode")      
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

    if (verbose): 
        print ("---\nVerbose: " + str(verbose) )
        print ("Repetition: " + str(repetition) )
        print ("Logging: " + str(logging) )
        print ("Experiment: " + str(experiment) )
        print ("Database: " + str(database) + "\n---" )
    #----------------------------- runExper(dbname, exper.conf)
    print (dbConf)
    print (exConf)
    
    exper = Configuration(exConf)
    exper.setupConf()  
    
    if dbConf=="orientdb":
        g = GraphDB()
        s = convert_bytes(g.size())
        print(s)
    
    
    #------------------------------ Nacitani konfigu
    #db = Configuration(dbConf)
    #db.setupConf()    
    #exper = Configuration(exConf)
    #exper.setupConf()
    #------------------------------ Spusteni testu

    #g = GraphDB(db)
    #s = convert_bytes(g.size())
    #print (s) 
    #g.dbCreate()
    #result = g.read(exper.get('command'))
    #print("result: ")
    #for item in result:
    #	print(" >" + str(item))
    
    print(" --- %s seconds ---" % (time.time()-start_time))
    #------------------------------

if __name__ == "__main__":
    main()
