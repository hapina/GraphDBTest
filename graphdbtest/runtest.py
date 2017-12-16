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
    try:
        opts, args = getopt.getopt(sys.argv[1:], "r:l:me:d:", ["repetition=", "logging=", "monitoring", "experiment=", "database="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print (err)
        usage()
        sys.exit(2)
        
    repetition = logging = None
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

    record = dict()
    record['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    record['exper_config_file'] = experiment[(experiment.rfind('/') + 1):]
    record['gdb_name'] = database
    record['repetition'] = exper.get('repetition')
    
    # Graph database inicialization
    if database=="orientdb":
        g = GraphDB(gdbName)
        g.setup()
    else:
        print("WARN: Not implemented yet.")
        return 3
    
    # Choose the type of experiment 
    if experimentType == 'select':
        for i in range(int(repetition)):
            start_time = time.time()
            commands = []
            commands = exper.get('commands').split("|")
            if __debug__:
                print(">>> " + str(i) + ". RUN COMMANDS")
            if not g.runCommand(commands):
                print("WARN: Failed runCommand for " + gdbName)
            else:
                status = "OK"
            record['status'] = status
            record['run_time'] = (time.time()-start_time)
            record['size_before'] = 0.0
            record['size_after'] = 0.0 
            if monitoring:
                if __debug__:
                    print(">>> Monitoring")
                mon = Monitoring()
                mon.insertRecord(record)
    else:
        print("WARN: Not implemented yet.")  
        return 3
 
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
