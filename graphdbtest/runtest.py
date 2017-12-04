import time
import sys
import getopt

from orientdb.orientdb_api import GraphDB
from setupConf import Configuration
from monitoring.monitoring import Monitoring

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
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:l:me:d:", ["repetition=", "logging=", "monitoring", "experiment=", "database="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print (err)
        usage()
        sys.exit(2)
        
    repetition = None
    logging = None
    monitoring = False
    experiment = None
    database = None
    status = "ERR"
    
    for o, a in opts:
        if o in ("-r", "--repetition"):
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
    
    # Configuration
    exper = Configuration(experiment)
    exper.setupConf()  
    gdbName = exper.get('db_name')
    experimentType = exper.get('experiment_type')
    if not repetition:
        repetition = exper.get('repetition')
    if not logging:
        logging = exper.get('logging')
    if not monitoring:
        monitoring = True if exper.get('monitoring')=='yes' else False

    start_time = time.time()
    record = dict()
    record['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    record['exper_config_file'] = 'e_select_001.conf' #experiment
    record['gdb_name'] = exper.get('db_name')
    record['repetition'] = exper.get('repetition')

    if __debug__: 
        print (">>> Repetition: " + str(repetition) )
        print (">>> Logging: " + str(logging) )
        print (">>> Monitoring: " + str(monitoring) )
        print (">>> Experiment: " + str(experiment) )
        print (">>> Database: " + str(database))
    
    # Graph database inicialization
    if database=="orientdb":
        g = GraphDB(gdbName)
        g.setup()
    elif database=="titandb":
        print("WARN: Not implemented yet.")
        sys.exit(3)
    elif database=="arangodb":
        print("WARN:  Not implemented yet.")
        sys.exit(3)
    else:
        print("WARN: Not implemented yet.")
        sys.exit(3)
    
    # Choose the type of experiment 
    if experimentType == 'commands':
        commands = []
        commands = exper.get('commands').split("|")
        if __debug__:
            print(">>> RUN COMMANDS")
        if not g.runCommand(commands):
            print("WARN: Failed runCommand for " + gdbName)
        else:
            status = "OK"
    elif experimentType == 'createdb':
        print("WARN: Not implemented yet.")
        sys.exit(3)
    elif experimentType == 'dropdb':
        print("WARM: Not implemented yet.")
        sys.exit(3)
    elif experimentType == 'importdb':
        print("WARM: Not implemented yet.")
        sys.exit(3)
    elif experimentType == 'exportdb':
        print("WARN: Not implemented yet.")
        sys.exit(3)
    else:
        print("WARN: Not implemented yet.")  
        sys.exit(3)
 
    record['status'] = status
    record['run_time'] = (time.time()-start_time)
    record['size_before'] = 0.0
    record['size_after'] = 0.0
    print("---")
    
    # Monitoring
    if monitoring:
        if __debug__:
            print(">>> Monitoring")
            print(">>> data = " + str(record))
        mon = Monitoring()
        mon.insertRecord(record)
        print(mon.select("select * from records"))
    
    #record_id		BIGSERIAL PRIMARY KEY,
    #timestamp	    timestamp NOT NULL,
    #exper_id	    char(10),
    #gdb_id	        char(10),
    #status	        varchar(50) NOT NULL,
    #repetition	    integer,
    #exper_run_time  bigint,
    #db_size_before  bigint,
    #db_size_after
                
    if __debug__:    
        print(">>> experiment type: %s" % (experimentType))
        print(">>> timestamp: %s" % (record['timestamp'] ))
        print(">>> experiment: %s" % (experiment))
        print(">>> database: %s" % (gdbName))
        print(">>> status: %s" % (record['status'] ))
        print(">>> repetition: %s" % (record['repetition'] ))
        print(">>> run_time: %s seconds" % record['run_time'] )
        print(">>> log settings: %s" % (logging))

if __name__ == "__main__":
    main()
